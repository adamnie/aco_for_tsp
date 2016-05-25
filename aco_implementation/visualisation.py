import networkx as nx
import matplotlib.pyplot as plt


class Visualisation:

    def __init__(self, cities):
        self.cities = cities
        self.old_data = list()
        self.G = nx.MultiGraph()
        self.iteration = 0
        self.shortest_iteration = 0
        self.repetition = 1
        self.shortest_path_length = 0
        self.avg_path_length = 0
        self.best_path = []
        self.old_best_path = []

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

    def draw_path(self, data, shortest_iteration, iteration, shortest_path_length, avg_path_length, last=False):
        self.shortest_iteration = shortest_iteration
        self.iteration = iteration
        self.shortest_path_length = shortest_path_length
        self.avg_path_length = avg_path_length

        plt.pause(0.25)
        plt.clf()
        plt.suptitle("Iteration: " + str(iteration) + "       Shortest iteration: " + str(shortest_iteration) +
                     "         Repetition: " + str(self.repetition) + "\nShortest path length: " +
                     str(shortest_path_length) + "      Average path length: " + str(avg_path_length))

        pos = nx.get_node_attributes(self.G, 'pos')
        labels = nx.get_node_attributes(self.G, 'label')
        nx.draw_networkx_nodes(self.G, pos, node_color='b', alpha=0.8, label=labels)
        nx.draw_networkx_labels(self.G, pos, labels, font_size=12, font_color='white')

        if not last:

            for elem, next_elem in zip(data, data[1:] + [data[0]]):
                self.G.add_edge(self.cities[0][elem], self.cities[0][next_elem])

            nx.draw_networkx_edges(self.G, pos, edge_color='b')

            for elem, next_elem in zip(data, data[1:] + [data[0]]):
                self.G.remove_edge(self.cities[0][elem], self.cities[0][next_elem])

        if self.best_path:
            for elem, next_elem in zip(self.best_path, self.best_path[1:] + [self.best_path[0]]):
                self.G.add_edge(self.cities[0][elem], self.cities[0][next_elem])
            self.old_best_path = self.best_path

            if last:
                nx.draw_networkx_edges(self.G, pos, edge_color='r', width=2, alpha=1)
            else:
                nx.draw_networkx_edges(self.G, pos, edge_color='r', width=2, alpha=0.2)

            for elem, next_elem in zip(self.best_path, self.best_path[1:] + [self.best_path[0]]):
                self.G.remove_edge(self.cities[0][elem], self.cities[0][next_elem])

        self.old_data = data

        plt.plot()
        plt.ylim([-55, 55])
        plt.xlim([-55, 55])

    def save_best_path(self, data):
        self.best_path = data

    def save_repetition(self, repetition):
        self.repetition = repetition

    def final_show_plot(self):
        plt.ylim([-55, 55])
        plt.xlim([-55, 55])
        plt.ioff()
        plt.show()
