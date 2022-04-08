import numpy as np

from models.state import State
from models.constants import *
from treelib import Tree


# Chip Color
# Red --> Model (MAXIMIZER)
# Blue --> User (MINIMIZER)


def maximize(board_state: State, k: int, tree, parent):  # boardState is state object, k is number of levels
    if not k or board_state.is_full_board():
        board_state.evaluate_set_cost()  # End of tree, get score using heuristics
        return board_state

    maxChild = None
    board_state.generate_children()
    i = 0
    for child in board_state.children:
        n = tree.create_node(child.cost, str(parent.identifier)+str(i), parent=parent)
        i += 1
        min_child = minimize(child, k - 1, tree, n)
        n.tag = min_child.cost
        if maxChild is None or min_child.cost > maxChild.cost:
            maxChild = child
            maxChild.cost = min_child.cost
            maxChild.pruning.alpha = max(maxChild.cost, maxChild.pruning.alpha) # Updating alpha

        # Break on pruning
        if maxChild.pruning.alpha > maxChild.pruning.beta:
            return maxChild

    return maxChild


def minimize(board_state: State, k: int, tree, parent):
    if not k or board_state.is_full_board():
        board_state.evaluate_set_cost()  # End of tree, get score using heuristics
        return board_state

    minChild = None
    board_state.generate_children()
    i = 1
    for child in board_state.children:

        n = tree.create_node(child.cost, str(parent.identifier)+str(i), parent=parent)
        i += 1
        max_child = maximize(child, k - 1, tree, n)
        n.tag = max_child.cost
        if minChild is None or max_child.cost < minChild.cost:
            minChild = child
            minChild.cost = max_child.cost
            minChild.pruning.beta = min(minChild.cost, minChild.pruning.beta)  # Update beta

        # Break on pruning
        if minChild.pruning.alpha > minChild.pruning.beta:
            return minChild

    return minChild


def decide(board_state: State, k: int, prune: bool, color: str):
    node = None
    tree = Tree()
    root = tree.create_node(board_state.cost, 0)
    if not prune:
        if color == red:
            node = maximize(board_state, k, tree, root)
        else:
            node = minimize(board_state, k, tree, root)
    root.tag = node.cost
    tree.show()
    return node
