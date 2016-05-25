import math
from threading import *
import random


class Ant(Thread):
    def __init__(self, id, start_node, colony, alpha=0.1):
        Thread.__init__(self)
        self.id = id
        self.start_node = start_node
        self.colony = colony

        self.current_node = start_node
        self.graph = self.colony.graph

        self.path = []
        self.path.append(start_node)
        self.path_length = 0

        self.go_pheromone_probability = 0.9

        #parameters
        self.Alpha = alpha
        self.Beta = 5
        self.evaporation_coefficient = 0.90

        self.remaining_nodes = {}

        for i in range(self.graph.nodes_count):
            if i != self.current_node:
                self.remaining_nodes[i] = i

        self.path_matrix = []

        for i in range(0, self.graph.nodes_count):
            self.path_matrix.append([0] * self.graph.nodes_count)

    def run(self):
        graph = self.graph
        while self.remaining_nodes:
            graph.lock.acquire()
            next_node = self.choose_next_node()
            self.path_length += graph.get_distance(self.current_node, next_node)
            print(self.path_length)
            self.path.append(next_node)
            self.path_matrix[self.current_node][next_node] = 1

            print("Ant %s: %s, %s" % (self.id, self.current_node, next_node))

            self.update_pheromone_trail(self.current_node, next_node)

            self.current_node = next_node

            graph.lock.release()

            del self.remaining_nodes[next_node]

        #closing the path
        self.path_length += graph.get_distance(self.path[-1], self.path[0])

        self.colony.update(self)

        print ("Ant %s finished." % (self.id,))

        self.__init__(self.id, self.start_node, self.colony)

    def choose_next_node(self):

        chosen_node = None
        probability_of_being_chosen = 0
        pheromone_sum = 0

        for node in self.remaining_nodes.values():
            pheromone = self.graph.get_pheromone(self.current_node, node)
            distance = self.graph.get_distance(self.current_node, node)
            pheromone_sum += math.pow(pheromone, self.Alpha) * math.pow(distance, -1 * self.Beta)

        avg_path_probability = pheromone_sum / len(self.remaining_nodes)

        rand_or_pheronome = random.random();

        if rand_or_pheronome < self.go_pheromone_probability:

            for node in self.remaining_nodes.values():
                pheromone = self.graph.get_pheromone(self.current_node, node)
                distance = self.graph.get_distance(self.current_node, node)
                probability = self.calculate_path_probability(distance, pheromone, pheromone_sum)

                if probability > probability_of_being_chosen:
                    probability_of_being_chosen = probability
                    chosen_node = node
        else:
            for node in self.remaining_nodes.values():
                pheromone = self.graph.get_pheromone(self.current_node, node)
                distance = self.graph.get_distance(self.current_node, node)
                probability = 1 / distance

                if probability > probability_of_being_chosen:
                    probability_of_being_chosen = probability
                    chosen_node = node

        if chosen_node is None:
            raise Exception("No node has been chosen for ant %s and node %s" % (self.id, self.current_node))

        return chosen_node

    def update_pheromone_trail(self, current_node, next_node):
        pheromone_value = (1 - self.evaporation_coefficient) * self.graph.get_pheromone(
            current_node, next_node) + self.evaporation_coefficient * self.graph.pheromone_constant

        self.graph.update_phermomene(current_node, next_node, pheromone_value)

    def calculate_path_probability(self, pheromone, distance, pheromone_sum):
        return (math.pow(pheromone, self.Alpha) * math.pow(distance, -1 * self.Beta) ) / pheromone_sum
