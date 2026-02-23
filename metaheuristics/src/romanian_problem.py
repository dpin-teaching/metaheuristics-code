from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from queue import PriorityQueue
import networkx as nx

@dataclass
class State:
   pass
  # def __eq__(self, other):
  #   pass

  # def __hash__(self):
  #   pass

  # def __str__(self) -> str:
  #   pass

@dataclass
class Node:
    state: State
    parent: Node
    action: Node
    path_cost: float

    def __lt__(self, other):
      return self.path_cost < other.path_cost


    # def __str__(self) -> str:
    #   return str(self.state) + "\n\n" + str(self.parent)
    
    def __repr__(self):
       return f'{self.state} ({self.path_cost})'


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
    cost = node.path_cost + problem.action_cost(source, action, target)
    if np.isinf(cost):
       continue
    next_node = Node(state=target, parent=node, action=action, path_cost=cost)
    yield next_node

def best_first_search(problem : Problem):
  frontier = PriorityQueue()
  initial_state = problem.initial_node
  reached = dict()
  reached[initial_state.state] = initial_state
  frontier.put(initial_state)
  def is_lower_cost(child, reached):
    state_child = child.state
    if child.path_cost < reached[state_child].path_cost:
        print(f"Shorter path {child.state} {child.path_cost} < {reached[state_child].path_cost}" )
        return True
    return False
  while not frontier.empty():
    node = frontier.get()
    if problem.is_goal(node.state):
      return node
    for child in expand(problem, node):
      s = child.state
      # if s not in reached or child.path_cost < reached[s].path_cost:
      if s not in reached or is_lower_cost(child, reached):
        reached[s] = child
        frontier.put(child)
  return None




from dataclasses import dataclass
import numpy as np
import networkx as nx

@dataclass
class RomaniaState(State):
    visited_nodes: list
    unvisited_nodes: list

    def __eq__(self, other):
      if not isinstance(other, State):
        """1. Implemente a verificação de igualdade entre estados em `def __eq__(self, other)"""
        return False
      return self.visited_nodes[-1 ]== other.visited_nodes[-1]
      

    def __hash__(self):
        return hash(str(self.visited_nodes[-1]))

    # def __str__(self) -> str:
    #     return str(self.visited_nodes[-1])

    def __repr__(self):
       return str(self.visited_nodes[-1])
@dataclass
class RomaniaProblem(Problem):
    graph: nx.Graph

    def action_cost(self, source: State, action: Node, target: State):
      cost = 0
      if len(source.visited_nodes) > 0:
        cost = float("inf")
        source_last_id = source.visited_nodes[-1]
        target_last_id = target.visited_nodes[-1]
        if self.graph.has_edge(source_last_id, target_last_id):
          """2. Implemente o cáculo do custo em `def action_cost(self, source: State, action: Node, target: State)"""
          cost = self.graph.get_edge_data(source_last_id, target_last_id)['weight']
      return cost

    def actions(self, state : Node):
      """3. Implemente a geração de ações em `def actions(self, state : Node)`"""
      for node_id in state.unvisited_nodes:
          unvisited_nodes = list(state.unvisited_nodes)
          unvisited_nodes.remove(node_id)
          next_node = RomaniaState(visited_nodes=state.visited_nodes + [node_id], unvisited_nodes=unvisited_nodes)
          yield next_node

    def is_goal(self, current_state: State):
        """4. Implemente a verificação do estado final em `def is_goal(self, current_state: State)`"""
        return current_state.visited_nodes[-1] == 'Bucharest'

