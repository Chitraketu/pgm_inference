from factor_graph import FactorGraph
from node import VarNode, FactorNode
import numpy as np

fg = FactorGraph()
a = VarNode(name='a', graph=fg)
b = VarNode(name='b', graph=fg)
c = VarNode(name='c', init=[1., 1., 1.], graph=fg)

f1_cpd = np.array([[2, 3],
                   [6, 4]])

f2_cpd = np.array([[7, 2, 3],
                   [1, 5, 2]])
f3_cpd = np.array([[7, 9, 3],
                   [6, 4, 2]])

f1 = FactorNode(cpd=f1_cpd, graph=fg, name='f1', ordered_variables=(a, b))
f2 = FactorNode(cpd=f2_cpd, graph=fg, name='f2', ordered_variables=(a, c))
f3 = FactorNode(cpd=f3_cpd, graph=fg, name='f3', ordered_variables=(b, c))

fg.add_var_nodes([a, b, c])
fg.add_factor_nodes([f1, f2, f3])
fg.add_edge(a, f1)
fg.add_edge(f1, b)
fg.add_edge(b, f3)
fg.add_edge(f3, c)
fg.add_edge(a, f2)
fg.add_edge(f2, c)
pos = {a: (-3, 0), b: (0, 3), c: (3, 0), f1: (-1.5, 1.5), f2: (0, 0), f3: (1.5, 1.5)}
fg.save_graph_fig(num=1, pos=pos)
# fg.sum_product(node=b)
fg.loopy_sum_product(iterations=20, epsilon=1e-5, plot_errors=True)


beliefs = fg.get_beliefs()
for k in beliefs:
    print(f"marginal prob. of node {k}:{beliefs[k]}")

print()
fg.loopy_max_sum(iterations=20, epsilon=1e-5, plot_errors=True)
map_beliefs = fg.get_beliefs()
for k in map_beliefs:
    print(f"conf. of node {k} for max joint prob.:{np.argmax(map_beliefs[k])}")


print(fg.get_beliefs())
