import networkx as nx
import matplotlib.pyplot as plt

plt.ion()

G = nx.Graph()

node1 = (0, 0)
node2 = (0, 2)
node3 = (1, 1)
node4 = (1, -1)
node5 = (3, 3)
node6 = (-3, 3)

G.add_node(node1, pos=node1)
G.add_node(node2, pos=node2)
G.add_node(node3, pos=node3)
G.add_node(node4, pos=node4)
G.add_node(node5, pos=node5)
G.add_node(node6, pos=node6)

G.add_edge(node6, node5)
G.add_edge(node5, node3)
G.add_edge(node3, node2)
G.add_edge(node2, node4)
G.add_edge(node4, node1)
G.add_edge(node1, node6)


pos = nx.get_node_attributes(G, 'pos')

nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.8)
nx.draw_networkx_edges(G, pos)

plt.plot()

plt.pause(2)

G.remove_edge(node6, node5)
G.remove_edge(node5, node3)
G.remove_edge(node3, node2)
G.remove_edge(node2, node4)
G.remove_edge(node4, node1)
G.remove_edge(node1, node6)

G.add_edge(node6, node3)
G.add_edge(node3, node5)
G.add_edge(node5, node2)
G.add_edge(node2, node4)
G.add_edge(node4, node1)
G.add_edge(node1, node6)

plt.clf()
nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.8)
nx.draw_networkx_edges(G, pos)


plt.plot()

plt.ioff()

plt.show()



