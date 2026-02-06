
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from queue import PriorityQueue

def array_eq(arr1, arr2):
  return (isinstance(arr1, np.ndarray) and
          isinstance(arr2, np.ndarray) and
          arr1.shape == arr2.shape and
          (arr1 == arr2).all())
  
@dataclass
class State:
  grid: np.array

  def __eq__(self, other):
    if not isinstance(other, State):
      return NotImplemented
    return array_eq(self.grid, other.grid) 

  def __hash__(self):
    return hash(str(self.grid))

  def __str__(self) -> str:
      return str(self.grid)

@dataclass
class Node:

    state: State
    parent: Node
    action: Node
    path_cost: float

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __str__(self) -> str:
      return str(self.state) + "\n\n" + str(self.parent)


@dataclass
class Problem:
    initial_state: Node

    def result(self, state: State, action: State):
      return action

    def action_cost(self, s: State, action: Node, s_prime: State):
      return 1

    def actions(self, state : Node):
      position_empty = np.where(state.grid == None)

      all_movements = [
        (np.array([+1]), np.array([0])),
        (np.array([0]), np.array([+1])),
        (np.array([-1]), np.array([0])),
        (np.array([0]), np.array([-1]))
    ]
      def swap(state, position_empty, next_movement):
        next_state = state.copy()
        next_state[position_empty] = state[next_movement]
        next_state[next_movement] = state[position_empty]
        return next_state

      possible_movements = []
      for movement in all_movements:
        candidate_moviment = tuple(map(sum, zip(position_empty, movement)))
        is_possible = 0 <= candidate_moviment[0] < 3 and 0 <= candidate_moviment[1] < 3
        if (is_possible):
          next_movement = swap(state.grid, position_empty, candidate_moviment)
          possible_movements.append(next_movement)
          next_state = State(grid=next_movement)
          yield next_state
  
    def is_goal(self, current_state: State):
      
      goal_state_grid =  np.array(
          [[1, 2, 3],
           [4, 5, 6],
           [7, 8, None]
           ])
      
      return array_eq(current_state.grid, goal_state_grid)

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

