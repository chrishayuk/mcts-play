def best_policy(children):
    """ Selects the child with the highest average reward. """
    return max(children, key=lambda c: c.reward / (c.visits + 1e-6))
