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
pos = {x1: (-7.5, 7.5), fa: (-4, 7.5), x2: (0, 7.5), fb: (4, 7.5), x3: (7.5, 7.5), fc: (0, 3), x4: (0, 0)}
fg.save_graph_fig(num=1, pos=pos, fig_name='tree-1')

fg.sum_product(x3)
# fg.max_product(x3)
# fg.max_sum(x3)
# fg.loopy_sum_product(iterations=5, plot_errors=True)
# fg.loopy_max_product(iterations=5)
# fg.loopy_max_sum(iterations=5)

beliefs = fg.get_beliefs()
for k in beliefs:
    print(f"marginal prob. of node {k}:{beliefs[k]}")

fg.max_sum(x3)
map_beliefs = fg.get_beliefs()
for k in map_beliefs:
    print(f"conf. of node {k} for max joint prob.:{np.argmax(map_beliefs[k])}")


fg.loopy_sum_product(iterations=20, epsilon=1e-5, plot_errors=True)
lbp_beliefs = fg.get_beliefs()
error = [np.linalg.norm(b-lb) for b, lb in zip(beliefs.values(), lbp_beliefs.values())]
error = sum(error) / len(error)
print(f"the error of approximation using lbp for sum_product: {error}")
fg.loopy_max_sum(iterations=20, epsilon=1e-5, plot_errors=True)
lbp_map_beliefs = fg.get_beliefs()

error_map = [np.linalg.norm(b-lb) for b, lb in zip(map_beliefs.values(), lbp_map_beliefs.values())]
error_map = sum(error_map) / len(error_map)
print(f"the error of approximation using lbp for max_sum: {error}")
