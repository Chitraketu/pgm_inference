from abc import ABC
import networkx as nx
import numpy as np


class Node(ABC):

    def __init__(self, graph: nx.Graph, name: str, init=None):
        self.graph = graph
        self.name = name
        if init is None: # assume that this is a binary variable
            init = np.array([1., 1.])
        self.belief = init
        self.log_belief = np.log(init)

    def belief(self):
        return self.belief

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

    def sum_product(self, node: Node):
        neighbors = self.get_neighbors(exclude=node)
        if not neighbors:
            msg = self.belief
        else:
            msg = np.ones_like(self.belief)
        for nbd in neighbors:
            msg *= self.messages_in[nbd]
        self.messages_out[node] = msg

    def max_product(self, node: Node):
        self.sum_product(node)

    def max_sum(self, node: Node):
        neighbors = self.get_neighbors(exclude=node)
        if not neighbors:
            msg = self.belief
        else:
            msg = np.zeros_like(self.log_belief)
        for nbd in neighbors:
            msg += self.messages_in[nbd]
        self.messages_out[node] = msg


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

    def sum_product(self, node: Node):
        neighbors = self.get_neighbors(exclude=node)
        msg = self._get_init_msg(node)
        for nbd in reversed(neighbors):
            msg = np.dot(msg, nbd.messages_out[self])
        node.messages_in[self] = msg
        return msg

    def max_product(self, node: Node):
        neighbors = self.get_neighbors(exclude=node)
        msg = self._get_init_msg(node)
        for nbd in reversed(neighbors):
            msg = np.multiply(msg, nbd.messages_out[self]).max(-1)
        node.messages_in[self] = msg
        return msg

    def max_sum(self, node: Node):
        neighbors = self.get_neighbors(exclude=node)
        msg = self._get_init_msg(node)
        msg = np.log(msg)
        for nbd in reversed(neighbors):
            msg = (msg + nbd.messages_out[self]).max(-1)
        node.messages_in[self] = msg
        return msg
