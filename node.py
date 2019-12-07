from abc import ABC
import networkx as nx
import numpy as np


class Node(ABC):

    def __init__(self, graph: nx.Graph, name: str, init=None):
        self.graph = graph
        self.name = name
        if init is None: # assume that this is a binary variable
            init = np.array([1., 1.])
        self._init = init
        self.belief = init
        self.log_belief = np.log(init)

    def reset_belief(self):
        self.belief = self._init

    def get_neighbors(self, exclude=None):
        neighbors = self.graph.neighbors(self)
        if exclude is not None:
            neighbors = [x for x in neighbors if x != exclude]
        return neighbors

    def message(self, node):
        pass

    def sum_product(self, node):
        pass

    def max_product(self, node):
        pass

    def max_sum(self, node):
        pass


class VarNode(Node):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "variable"
        self.messages_in = {}
        self.messages_out = {}

    def clear_messages(self):
        self.messages_in = {}
        self.messages_out = {}

    def update_belief(self):
        msg = np.ones_like(self.belief)
        for factor in self.messages_in:
            msg *= self.messages_in[factor]
        self.belief = msg / np.linalg.norm(msg, 1)

    def update_log_belief(self):
        msg = np.zeros_like(self.log_belief)
        for factor in self.messages_in:
            msg += self.messages_in[factor]
        self.belief = np.exp(msg) / sum(np.exp(msg))
        self.log_belief = np.log(self.belief)

    def sum_product(self, node: Node, normalize=False):
        neighbors = self.get_neighbors(exclude=node)
        msg = np.ones_like(self.belief)
        for nbd in neighbors:
            msg *= self.messages_in[nbd]
        if normalize:
            msg = msg / (np.sum(msg) + 1e-10)
        self.messages_out[node] = msg

    def max_product(self, node: Node, normalize=False):
        self.sum_product(node, normalize=normalize)

    def max_sum(self, node: Node, normalize=False):
        neighbors = self.get_neighbors(exclude=node)
        msg = np.zeros_like(self.log_belief)
        for nbd in neighbors:
            msg += self.messages_in[nbd]
        if normalize:
            msg = msg - np.log(np.sum(np.exp(msg)))
        self.messages_out[node] = msg

    def loopy_sum_product(self, node: Node):
        self.sum_product(node)
        msg = self.messages_out[node]
        self.messages_out[node] = msg / np.linalg.norm(msg, 1)


class FactorNode(Node):

    def __init__(self, cpd, ordered_variables, **kwargs):
        super().__init__(**kwargs)
        self.cpd = cpd
        self.log_cpd = np.log(cpd)
        self.order_neighbors = {var: i for (i, var) in enumerate(ordered_variables)}
        self.type = "factor"

    def _get_init_msg(self, node):
        if node not in self.order_neighbors:
            raise IndexError("Node not the neighbor of this factor node")
        msg = self.cpd
        pos = self.order_neighbors[node]
        order = [x for x in range(len(self.cpd.shape)) if x != pos]
        order = tuple([pos]+order)
        msg = msg.transpose(order)
        return msg

    def sum_product(self, node: Node, normalize=False):
        neighbors = self.get_neighbors(exclude=node)
        msg = self._get_init_msg(node)
        for nbd in reversed(neighbors):
            msg = np.dot(msg, nbd.messages_out[self])
        if normalize:
            msg = msg / (np.sum(msg) + 1e-10)
        node.messages_in[self] = msg
        return msg

    def max_product(self, node: Node, normalize=False):
        neighbors = self.get_neighbors(exclude=node)
        msg = self._get_init_msg(node)
        for nbd in reversed(neighbors):
            msg = np.multiply(msg, nbd.messages_out[self]).max(-1)
        if normalize:
            msg = msg / (np.sum(msg) + 1e-10)
        node.messages_in[self] = msg
        return msg

    def max_sum(self, node: Node, normalize=False):
        neighbors = self.get_neighbors(exclude=node)
        msg = self._get_init_msg(node)
        msg = np.log(msg)
        for nbd in reversed(neighbors):
            msg = (msg + nbd.messages_out[self]).max(-1)
        if normalize:
            msg = msg - np.log(np.sum(np.exp(msg)))
        node.messages_in[self] = msg
        return msg
