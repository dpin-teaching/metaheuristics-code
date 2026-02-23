import numpy as np
from typing import Tuple
from dataclasses import dataclass

def to_tuple(array_grid: np.ndarray):
    return tuple(tuple(row) for row in array_grid)

def swap(tuple_grid, p1, p2):
    # array_grid = np.array(tuple_grid)
    # temp = array_grid[p1[0]][p1[1]]
    # array_grid[p1[0]][p1[1]] = array_grid[p2[0]][p2[1]]
    # array_grid[p2[0]][p2[1]] = temp
    # return to_tuple(array_grid)
    
    array_grid = np.array(tuple_grid)
    temp = array_grid[p1]
    array_grid[p1] = array_grid[p2]
    array_grid[p2] = temp
    return to_tuple(array_grid)


@dataclass(frozen=True)
class State:

    grid: Tuple

    def empty_pos(self):
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value is None:
                    return i,j
        raise RuntimeError("Invalid State: None inexistent")

    @classmethod
    def from_array(cls, grid: np.ndarray) -> State:
        return cls(to_tuple(grid))

@dataclass(frozen=True)
class Problem:

    state_initial: State
    state_final: State

    def is_goal(self, state_current):
        return state_current == self.state_final
    
    def actions(self, state_current: State):
        all_actions = [
            (1, 0), #down
            (-1, 0), #up
            (0, 1), #right
            (0, -1), #left
        ]
        # allowed_actions = []
        position_empty = state_current.empty_pos()
        for action in all_actions:
            position_candidate = tuple(map(sum, zip(position_empty, action)))
            row, column = position_candidate
            is_allowed = 0 <= row < 3 and 0 <= column < 3
            if is_allowed:
                # allowed_actions.append(action)
                yield action
        # return all_actions
            
    def result(self, state_current: State, action: Tuple) -> State:
        position_empty_current = state_current.empty_pos()
        position_empty_next = tuple(map(sum, zip(position_empty_current, action)))
        grid_next = swap(state_current.grid, position_empty_current, position_empty_next)
        state_next = State(grid_next)
        return state_next
    
    def action_cost(self, state_current: State, action: Tuple, state_next: State):
        return 1

@dataclass
class Node:
    state: State
    action: Tuple
    parent: Node
    cost: float

    def __lt__(self, other):
        if not isinstance(other, Node):
            return False
        return self.cost < other.cost


    def expand(self, problem: Problem):
        state_current = self.state
        for action in problem.actions(state_current):
            state_next = problem.result(state_current, action)
            cost = self.cost + problem.action_cost(state_current, action, state_next)
            next_node = Node(state=state_next, 
                             action=action, 
                             parent=self,
                             cost=cost
                             )
            yield next_node

from queue import PriorityQueue
def best_first_search(problem: Problem):
    frontier = PriorityQueue()
    reached = dict()
    state_initial = problem.state_initial
    node = Node(state=state_initial,
                parent=None,
                action=None,
                cost=0
    )
    frontier.put(node)
    def is_lower_cost(child, reached):
        state_child = child.state
        if child.cost < reached[state_child].cost:
            print("USEFUL")
            return True
        return False
    
    while not frontier.empty():
        node: Node
        node = frontier.get()
        if problem.is_goal(node.state):
            return node
        for child in node.expand(problem):
            state_child = child.state
            if state_child not in reached or is_lower_cost(child, reached):
                reached[state_child] = child
                frontier.put(child)
    return None