import logging
from mcts.policy.random_policy import random_policy
from mcts.policy.best_policy import best_policy

# Initialize logger (assumes it's configured in main)
logger = logging.getLogger(__name__)

def traverse_all_nodes(node):
    """ Recursively gather all nodes in the subtree rooted at 'node'. """
    nodes = [node]

    # loop through each child
    for child in node.children:
        # traverse nodes
        nodes.extend(traverse_all_nodes(child))

    # return nodes
    return nodes

def mcts_search(root, evaluate, iterations=50, selection_policy=None, discount_factor=0.9, win_threshold=1.0, debug=False):
    """Performs MCTS search and returns the best immediate next move for the AI."""

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

        # Selection phase to find a leaf node
        while node.has_children():
            # find the best child, using the selection policy
            node = node.best_child(policy_func=selection_policy)

            # check we got a node
            if node is None:
                logger.debug("No valid child available during selection.")
                break

        # Expansion
        if node is not None and not node.has_children():
            # expand the children nodes
            children = node.expand()

            # check if we have children
            if children:
                # get the node, using random policy
                node = random_policy(children)
                logger.debug(f"Expanded Node State:\n{node.state}\n")

        # Simulation and backpropagation
        if node is not None:
            # Simulation (evaluate the node's state)
            reward = evaluate(node.state)
            logger.debug(f"Evaluated State:\n{node.state}\nReward: {reward}")

            # Backpropagation
            node.backpropagate(reward)
            logger.debug(f"Backpropagated reward: {reward} to parent nodes.")

    # After all iterations, select the best child of the root node
    if root.children:
        best_child = max(root.children, key=lambda c: c.reward)
        final_state = best_child.state
        logger.debug(f"Best Move State after search:\n{final_state}")
        return final_state
    else:
        # No moves available, return the root state
        return root.state

