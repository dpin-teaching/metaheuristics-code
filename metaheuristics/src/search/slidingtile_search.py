
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from queue import PriorityQueue
from typing import Optional

from .base_search import *

def array_eq(arr1, arr2):
  return (isinstance(arr1, np.ndarray) and
          isinstance(arr2, np.ndarray) and
          arr1.shape == arr2.shape and
          (arr1 == arr2).all())
  
def grid_to_tuple(grid: np.ndarray) -> tuple[int, ...]:
    return tuple(
        0 if x is None else int(x)
        for x in grid.flatten()
    )


@dataclass(frozen=True, slots=True)
class SlidingTileState:
  board: np.array

  # def __eq__(self, other):
  #   if not isinstance(other, SlidingTileState):
  #     return NotImplemented
  #   return array_eq(self.board, other.board) 

  # def __hash__(self):
  #   return hash(str(self.board))

  # def __str__(self) -> str:
  #     return str(self.board)

@dataclass
class Node:

    state: SlidingTileState
    parent: Optional[Node]
    action: Optional[Node]
    path_cost: float

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __str__(self) -> str:
      return str(self.state) + "\n\n" + str(self.parent)


@dataclass
class Problem:
    initial_state: Node

    def result(self, state: SlidingTileState, action: SlidingTileState):
      return action

    def action_cost(self, s: SlidingTileState, action: Node, s_prime: SlidingTileState):
      return 1

    def actions(self, state: Node):
      s = state.state  # SlidingTileState
      board = s.board
      # Board is stored as flat tuple (0 = empty); convert to 2D grid for moves
      grid = np.array(board).reshape(3, 3)
      row, col = np.where(grid == 0)
      position_empty = (int(row[0]), int(col[0]))

      all_movements = [(1, 0), (0, 1), (-1, 0), (0, -1)]

      def swap(g, pos_empty, pos_next):
        next_grid = np.array(g, copy=True)
        r0, c0 = pos_empty
        r1, c1 = pos_next
        next_grid[r0, c0], next_grid[r1, c1] = next_grid[r1, c1], next_grid[r0, c0]
        return next_grid

      for movement in all_movements:
        candidate = (position_empty[0] + movement[0], position_empty[1] + movement[1])
        if 0 <= candidate[0] < 3 and 0 <= candidate[1] < 3:
          next_grid = swap(grid, position_empty, candidate)
          next_board = grid_to_tuple(next_grid)
          yield SlidingTileState(board=next_board)
  
    def is_goal(self, current_state: SlidingTileState):
      # Board is stored as flat tuple with 0 for empty
      goal_board = (1, 2, 3, 4, 5, 6, 7, 8, 0)
      return current_state.board == goal_board

def expand(problem: Problem, node: Node):
  s = node.state
  for action in problem.actions(s):
    s_prime = problem.result(s, action)
    cost = node.path_cost + problem.action_cost(s, action, s_prime)
    next_node = Node(state=s_prime, parent=node, action=action, path_cost=cost)
    yield next_node


def best_first_search(problem : Problem):
  frontier = PriorityQueue()
  reached = dict()
  initial_state = problem.initial_state
  frontier.put((initial_state.path_cost, initial_state))
  while not frontier.empty():
    node = frontier.get()[1]
    if problem.is_goal(node.state):
      return node
    for child in expand(problem, node):
      s = child.state
      if s not in reached or child.path_cost < reached[s].path_cost:
        reached[s] = child
        frontier.put((child.path_cost, child))
  return None

