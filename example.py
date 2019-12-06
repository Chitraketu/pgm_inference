from factor_graph import FactorGraph
from node import VarNode, FactorNode
import numpy as np

fg = FactorGraph()

params = {'graph': fg}
x1 = VarNode(name='x1', **params)
x2 = VarNode(name='x2', **params)
x3 = VarNode(name='x3', **params)
x4 = VarNode(name='x4', **params)

cpd_a = np.array([[3, 4],
                  [3, 9]])
cpd_b = np.array([[3, 4],
                  [5, 1]])
cpd_c = np.array([[7, 8],
                  [3, 9]])
fa = FactorNode(cpd_a, (x1, x2), name='fa', **params)
fb = FactorNode(cpd_b, (x2, x3), name='fb', **params)
fc = FactorNode(cpd_c, (x2, x4), name='fc', **params)

fg.add_var_nodes([x1, x2, x3, x4])
fg.add_factor_nodes([fa, fb, fc])

fg.add_edge(x1, fa)
fg.add_edge(fa, x2)
fg.add_edge(x2, fb)
fg.add_edge(fb, x3)
fg.add_edge(x2, fc)
fg.add_edge(fc, x4)

print(fg.nodes)
print(fg.neighbors(x4))
fg.sum_product(x3)
fg.max_product(x3)
fg.max_sum(x3)
