from factor_graph import FactorGraph
from node import VarNode, FactorNode
import numpy as np

fg = FactorGraph()
a = VarNode(name='a', graph=fg)
b = VarNode(name='b', graph=fg)
c = VarNode(name='c', init=[1., 1., 1.], graph=fg)
d = VarNode(name='d', graph=fg)

f1_cpd = np.array([[2, 3],
                   [6, 4]])

f2_cpd = np.array([[[7, 2, 3],
                    [1, 5, 2]],
                   [[8, 3, 9],
                    [6, 4, 2]]
                   ])
f3_cpd = np.array([5, 1, 9])
f1 = FactorNode(cpd=f1_cpd, graph=fg, name='f1', ordered_variables=(a, b))
f2 = FactorNode(cpd=f2_cpd, graph=fg, name='f2', ordered_variables=(b, d, c))
f3 = FactorNode(cpd=f3_cpd, graph=fg, name='f3', ordered_variables=(c,))
fg.add_var_nodes([a, b, c, d])
fg.add_factor_nodes([f1, f2, f3])
fg.add_edge(a, f1)
fg.add_edge(f1, b)
fg.add_edge(b, f2)
fg.add_edge(f2, c)
fg.add_edge(f2, d)
fg.add_edge(c, f3)

fg.sum_product(node=b)

