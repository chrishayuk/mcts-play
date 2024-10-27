# mcts_node.py
class Node:
    def __init__(self, state, parent=None, action_func=None, evaluate_func=None):
        """ Initializes a Node in the MCTS tree. """
        # Set the state and parent
        self.state = state
        self.parent = parent

        # Initialize children, visits, and reward
        self.children = []
        self.visits = 0
        self.reward = 0

        # Functions for generating actions and evaluating states
        self.action_func = action_func
        self.evaluate_func = evaluate_func

    def is_fully_expanded(self):
        """ Check if the node has been expanded with any children. """
        return len(self.children) > 0

    def expand(self):
        """ Expands the current node by generating children based on possible states. """
        # check if we have an action function
        if self.action_func:
            # Generate possible child states directly
            child_states = self.action_func(self.state)

            # check for new state in child states
            for new_state in child_states:
                # Create a child node with each new state without modification
                child_node = Node(new_state, parent=self, action_func=self.action_func, evaluate_func=self.evaluate_func)

                # Evaluate the reward of this new state if evaluation function is provided
                if self.evaluate_func:
                    child_node.reward = self.evaluate_func(new_state)
                
                # Append the child node to children
                self.children.append(child_node)

                # Optional early stopping if maximum reward is achieved
                if self.evaluate_func and child_node.reward >= 1:
                    # Stop expanding if max reward reached
                    return self.children  
        
        # return the chilfren (if no childrem, return none)
        return self.children if self.children else None

    def best_child(self, policy_func):
        """ Selects the best child based on the provided policy function. """
        # check for children
        if not self.children:
            # No children, so no best child
            return None  
        
        # Apply policy function to select the best child
        return policy_func(self.children)  

    def backpropagate(self, reward):
        """ Updates reward and visit counts, propagating up the tree. """ 
        # Increment the number of visits
        self.visits += 1

        # Calculate the new average reward
        self.reward += (reward - self.reward) / self.visits

        # Propagate reward to the parent
        if self.parent:
            self.parent.backpropagate(reward)
