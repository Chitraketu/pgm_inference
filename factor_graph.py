import networkx as nx
from random import choice
from typing import List
from node import Node


class FactorGraph(nx.Graph):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.var_nodes = []
        self.factor_nodes = []

    def add_var_nodes(self, nodes: List[Node]):
        self.var_nodes = nodes
        super().add_nodes_from(nodes)

    def add_factor_nodes(self, nodes: List[Node]):
        self.factor_nodes = nodes
        super().add_nodes_from(nodes)

    def _clear_messages(self):
        for node in self.var_nodes:
            node.clear_messages()

    def sum_product(self, node=None):
        """
        This function runs the sum product algorithm
        on the graph and sets the message for every nodes.
        :param node: The root node in the graph
        :return: None
        """
        self._clear_messages()
        if node is None:
            node = choice(self.nodes)
        elif node not in self.nodes:
            raise IndexError("the requested node not found")
        backward = list(nx.dfs_edges(self, source=node))
        forward = reversed(backward)
        for (v, u) in forward:
            u.sum_product(v)
        for (u, v) in backward:
            u.sum_product(v)
        pass

    def max_product(self, node=None):
        self._clear_messages()
        if node is None:
            node = choice(self.nodes)
        elif node not in self.nodes:
            raise IndexError("the requested node not found")
        backward = list(nx.dfs_edges(self, source=node))
        forward = reversed(backward)
        for (v, u) in forward:
            u.max_product(v)
        for (u, v) in backward:
            u.max_product(v)
        pass

    def max_sum(self, node=None):
        self._clear_messages()
        if node is None:
            node = choice(self.nodes)
        elif node not in self.nodes:
            raise IndexError("the requested node not found")
        backward = list(nx.dfs_edges(self, source=node))
        forward = reversed(backward)
        for (v, u) in forward:
            u.max_sum(v)
        for (u, v) in backward:
            u.max_sum(v)
        pass

    def loopy_sum_product(self, iterations=10, epsilon=1e-2):
        pass

    def loopy_max_sum(self):
        pass

    def transform_junction(self):
        raise NotImplementedError("WIP: not implemented yet")



