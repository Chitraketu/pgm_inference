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
            node.reset_belief()
            node.clear_messages()

    def _init_messages(self):
        for node in self.var_nodes:
            for factor in node.get_neighbors():
                node.messages_out[factor] = node.belief

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

        for var in self.var_nodes:
            var.update_belief()
        print(f"The beliefs :")
        for var in self.var_nodes:
            print(f"variable: {var.name} has prob: {var.belief}")

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

        for var in self.var_nodes:
            var.update_belief()
        print(f"The beliefs :")
        for var in self.var_nodes:
            print(f"variable: {var.name} has prob: {var.belief}")
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
        for var in self.var_nodes:
            var.update_log_belief()
        print(f"The beliefs :")
        for var in self.var_nodes:
            print(f"variable: {var.name} has prob: {var.belief}")
        pass

    def loopy_sum_product(self, iterations=10, epsilon=1e-2):
        self._clear_messages()
        self._init_messages()
        for i in range(iterations):
            # updating factor to variable message
            for factor in self.factor_nodes:
                adj_variables = factor.get_neighbors()
                for var in adj_variables:
                    factor.sum_product(var, normalize=True)

            # updating variable to factor message
            for var in self.var_nodes:
                adj_factors = var.get_neighbors()
                for factor in adj_factors:
                    var.sum_product(factor, normalize=True)
            for var in self.var_nodes:
                var.update_belief()
            '''
            print("The messages are as follows:")
            for var in self.var_nodes:
                for factor in var.messages_out:
                    print(f"{var.name} -> {factor.name}: {var.messages_out[factor]}")
                for factor in var.messages_in:
                    print(f"{factor.name} -> {var.name}: {var.messages_in[factor]}")
            print(f"The beliefs after iteration {i}:")
            for var in self.var_nodes:
                print(f"variable: {var.name} has prob: {var.belief}")
            print()
            '''
        pass

    def loopy_max_product(self, iterations=10, epsilon=1e-2):
        self._clear_messages()
        self._init_messages()
        for i in range(iterations):
            # updating factor to variable message
            for factor in self.factor_nodes:
                adj_variables = factor.get_neighbors()
                for var in adj_variables:
                    factor.max_product(var, normalize=True)

            # updating variable to factor message
            for var in self.var_nodes:
                adj_factors = var.get_neighbors()
                for factor in adj_factors:
                    var.max_product(factor, normalize=True)
            for var in self.var_nodes:
                var.update_belief()
            '''
            print("The messages are as follows:")
            for var in self.var_nodes:
                for factor in var.messages_out:
                    print(f"{var.name} -> {factor.name}: {var.messages_out[factor]}")
                for factor in var.messages_in:
                    print(f"{factor.name} -> {var.name}: {var.messages_in[factor]}")
            print(f"The beliefs after iteration {i}:")
            for var in self.var_nodes:
                print(f"variable: {var.name} has prob: {var.belief}")
            print()
            '''

    def loopy_max_sum(self, iterations=10, epsilon=1e-2):
        self._clear_messages()
        self._init_messages()
        for i in range(iterations):
            # updating factor to variable message
            for factor in self.factor_nodes:
                adj_variables = factor.get_neighbors()
                for var in adj_variables:
                    factor.max_sum(var, normalize=True)

            # updating variable to factor message
            for var in self.var_nodes:
                adj_factors = var.get_neighbors()
                for factor in adj_factors:
                    var.max_sum(factor, normalize=True)
            for var in self.var_nodes:
                var.update_log_belief()
            print("The messages are as follows:")
            for var in self.var_nodes:
                for factor in var.messages_out:
                    print(f"{var.name} -> {factor.name}: {var.messages_out[factor]}")
                for factor in var.messages_in:
                    print(f"{factor.name} -> {var.name}: {var.messages_in[factor]}")
            print(f"The beliefs after iteration {i}:")
            for var in self.var_nodes:
                print(f"variable: {var.name} has prob: {var.belief}")
            print()
        pass

    def transform_junction(self):
        raise NotImplementedError("WIP: not implemented yet")



