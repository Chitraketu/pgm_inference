import networkx as nx
import matplotlib.pyplot as plt
from random import choice
from typing import List
from node import Node, FactorNode
import numpy as np


class FactorGraph(nx.Graph):
    INF = 1

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
        '''
        print(f"The beliefs :")
        for var in self.var_nodes:
            print(f"variable: {var.name} has prob: {var.belief}")
        '''
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

    def loopy_sum_product(self, iterations=10, epsilon=1e-2, plot_errors=False):
        self._clear_messages()
        self._init_messages()
        mu = []
        errors = []
        for var in self.var_nodes:
            mu.append(np.full_like(var.belief, FactorGraph.INF))
        for i in range(iterations):
            print(f"iteration:{i}")
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
            new_mu = [var.belief.copy() for var in self.var_nodes]
            error = [np.linalg.norm(m - nm) for m, nm in zip(mu, new_mu)]
            error = sum(error) / len(error)
            errors.append(error)
            if error < epsilon:
                break
            mu = [var.copy() for var in new_mu]
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
        if plot_errors:
            FactorGraph.plot_errors(errors, 'sum_product_error')
        pass

    def loopy_max_product(self, iterations=10, epsilon=1e-2, plot_errors=False):
        self._clear_messages()
        self._init_messages()
        mu = []
        for var in self.var_nodes:
            mu.append(np.full_like(var.belief, FactorGraph.INF))
        errors = []
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
            new_mu = [var.belief.copy() for var in self.var_nodes]
            error = [np.linalg.norm(m - nm) for m, nm in zip(mu, new_mu)]
            error = sum(error) / len(error)
            errors.append(error)
            if error < epsilon:
                break
            mu = [var.copy() for var in new_mu]

        if plot_errors:
            FactorGraph.plot_errors(errors, 'max_product_error')

    @staticmethod
    def plot_errors(errors, fig_name="error"):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(211)
        ax.plot(errors)
        ax.set_xlabel('Num of iterations')
        ax.set_ylabel('convergence error')
        # plt.ylim(0, 0.01)
        # plt.show()

        ax2 = fig.add_subplot(212)
        ax2.plot(np.log(errors))
        ax2.set_xlabel('Num of iterations')
        ax2.set_ylabel('convergence error (log scale)')

        plt.savefig(fig_name)

    def loopy_max_sum(self, iterations=10, epsilon=1e-2, plot_errors=False):
        self._clear_messages()
        self._init_messages()
        mu = []
        errors = []
        for var in self.var_nodes:
            mu.append(np.full_like(var.belief, FactorGraph.INF))
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

            new_mu = [var.belief.copy() for var in self.var_nodes]
            error = [np.linalg.norm(m - nm) for m, nm in zip(mu, new_mu)]
            error = sum(error) / len(error)
            errors.append(error)
            if error < epsilon:
                break
            mu = [var.copy() for var in new_mu]

        if plot_errors:
            FactorGraph.plot_errors(errors, 'max_sum_error')
        pass

    def draw_graph(self, num=None, pos=None):
        # if position not provided get the positions of nodes from networkx spring_layout
        if pos is None:
            pos = nx.spring_layout(self, scale=10)
        fig = plt.figure(num=num)
        ax = fig.add_subplot(111)
        # drawing the variable nodes of the graph which are of shape 'circle'
        for node in self.var_nodes:
            ax.annotate(node.name, xy=(pos[node][0], pos[node][1] + .0045))
            plt.scatter(pos[node][0], pos[node][1], marker='o', s=800, facecolors='r', edgecolors='r')

        # drawing the factor nodes of the graph which are of shape 'square'
        for node in self.factor_nodes:
            ax.annotate(node.name, xy=(pos[node][0], pos[node][1] + .0045))
            # annotating the midpoint of the edge with the message provided as a list
            x1, y1 = pos[node]
            k = 0.5
            ax.annotate(node.cpd,
                        xy=(x1, y1),
                        xytext=(x1 + k, y1 + k),
                        # arrowprops=dict(arrowstyle="->")
                        )
            plt.scatter(pos[node][0], pos[node][1], marker='s', s=500, facecolors='r')

        # drawing the edges
        for (u, v) in self.edges.data(False):
            x, y = zip(*[tuple(pos[u]), tuple(pos[v])])
            plt.plot(x, y, 'r-', linewidth=2)

        plt.axis('off')
        return

    def save_graph_fig(self, num=None, pos=None, fig_name="graph"):
        self.draw_graph(num=num, pos=pos)
        plt.savefig(fig_name)
        pass

    def get_beliefs(self):
        return {node.name:node.belief for node in self.var_nodes}

    def transform_junction(self):
        raise NotImplementedError("WIP: not implemented yet")



