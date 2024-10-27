import random
import logging
from policy.best_policy import best_policy

# Initialize logger (assumes it's configured in main)
logger = logging.getLogger(__name__)

def traverse_all_nodes(node):
    """ Recursively gather all nodes in the subtree rooted at 'node'. """
    nodes = [node]
    for child in node.children:
        nodes.extend(traverse_all_nodes(child))
    return nodes

def mcts_search(root, evaluate, iterations=50, selection_policy=None, discount_factor=0.9, win_threshold=1.0, debug=False):
    """ Performs MCTS search with immediate win termination and depth-based exploration adjustments. """
    
    # Set logging level based on debug flag
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Use a default policy if none is provided
    selection_policy = selection_policy or best_policy

    for _ in range(iterations):
        # Selection
        node = root
        
        # Immediate win check before expanding
        if evaluate(node.state) >= win_threshold:
            logger.debug("Winning state found during initial selection.")
            return node.state
        
        # Selection phase to find a fully expanded node
        while node.is_fully_expanded():
            node = node.best_child(policy_func=selection_policy)
            if node is None:
                logger.debug("No valid child available during selection.")
                break

        # Expansion
        if node is not None:
            children = node.expand()
            if children:
                node = random.choice(children)
                logger.debug(f"Expanded Node State:\n{node.state}\n")

            # Simulation with depth-based discounting for rewards
            depth = 0
            current = node
            while current.parent is not None:
                depth += 1
                current = current.parent
            depth_discount = discount_factor ** depth
            
            # Evaluate the reward
            reward = evaluate(node.state) * depth_discount if node else 0
            logger.debug(f"Evaluated State:\n{node.state}\nReward: {reward}")

            # Backpropagation
            if node:
                node.backpropagate(reward)
                logger.debug(f"Backpropagated reward: {reward} to parent nodes.")

    # Traverse all nodes and find the best one
    all_nodes = traverse_all_nodes(root)
    for node in all_nodes:
        logger.debug(f"Node State:\n{node.state}\nReward: {node.reward}")

    # Select the node with the highest reward
    best_node = max(all_nodes, key=lambda n: n.reward, default=root)
    final_state = best_node.state
    logger.debug(f"Best Node State after search:\n{final_state}")
    
    return final_state if final_state else None
