import networkx as nx
import matplotlib.pyplot as plt


class Visualisation:

    def __init__(self, cities):
        self.cities = cities
        self.old_data = list()
        self.G = nx.Graph()

    def initialize_graph_with_nodes(self):
        plt.figure(0, (10, 8))
        plt.ion()

        for index, city in enumerate(self.cities[1]):
            self.G.add_node(self.cities[0][index], pos=city, label=self.cities[0][index])

        pos = nx.get_node_attributes(self.G, 'pos')
        labels = nx.get_node_attributes(self.G, 'label')
        nx.draw_networkx_nodes(self.G, pos, node_color='b', alpha=0.8, label=labels)
        nx.draw_networkx_labels(self.G, pos, labels, font_size=12, font_color='white')

        plt.plot()
        plt.ylim([-55, 55])
        plt.xlim([-55, 55])

    def draw_path(self, data, shortest_iteration, iteration, shortest_path_length, avg_path_length):
        plt.pause(0.25)
        plt.clf()
        plt.suptitle("Iteration: " + str(iteration) + "       Shortest iteration: " + str(shortest_iteration) +
                     "\nShortest path length: " + str(shortest_path_length) +
                     "      Average path length: " + str(avg_path_length))

        if self.old_data:
            for elem, next_elem in zip(self.old_data, self.old_data[1:] + [self.old_data[0]]):
                self.G.remove_edge(self.cities[0][elem], self.cities[0][next_elem])

            self.old_data = []

        for elem, next_elem in zip(data, data[1:] + [data[0]]):
            self.G.add_edge(self.cities[0][elem], self.cities[0][next_elem])

        pos = nx.get_node_attributes(self.G, 'pos')
        labels = nx.get_node_attributes(self.G, 'label')
        nx.draw_networkx_nodes(self.G, pos, node_color='b', alpha=0.8, label=labels)
        nx.draw_networkx_labels(self.G, pos, labels, font_size=12, font_color='white')
        nx.draw_networkx_edges(self.G, pos)

        self.old_data = data

        plt.plot()
        plt.ylim([-55, 55])
        plt.xlim([-55, 55])

    def final_show_plot(self):
        plt.ylim([-55, 55])
        plt.xlim([-55, 55])
        plt.ioff()
        plt.show()
