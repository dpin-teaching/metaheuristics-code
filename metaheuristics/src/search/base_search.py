# from abc import ABC, abstractmethod
from typing import Protocol, Hashable
from dataclasses import dataclass
class State(Protocol, Hashable):
    def __str__(self) -> str: ...
      
  
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

@dataclass()
class Problem:
    initial_node: Node

    def result(self, state: State, action: State):
      return action

    def action_cost(self, source: State, action: Node, target: State):
      pass

    def actions(self, state : Node):
      pass
  
    def is_goal(self, current_state: State):
      pass
      
def expand(problem: Problem, node: Node):
  source = node.state
  for action in problem.actions(source):
    target = problem.result(source, action)
   # if problem.action_cost(source, action, target) is None:
   #   cost = node.path_cost
    #else:
    cost = node.path_cost + problem.action_cost(source, action, target)
    next_node = Node(state=target, parent=node, action=action, path_cost=cost)
    yield next_node