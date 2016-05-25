from ant import Ant
from threading import Lock, Condition
import sys
import random


class AntColony:
    def __init__(self, graph, ants_count, max_number_of_iterations, visualisation, alpha=0.1):
        self.graph = graph
        self.ants_count = ants_count
        self.max_number_of_iterations = max_number_of_iterations
        self.Alpha = alpha
        self.visualisation = visualisation

        self.condition = Condition()
        self.reset()

    def reset(self):
        self.shortest_path_length = sys.maxsize
        self.shortest_path = None
        self.shortest_path_matrix = None
        self.shortest_path_convergence_iteration = 0

    def start(self):
        self.ants = self.create_ants()
        self.iteration_counter = 0

        while self.iteration_counter < self.max_number_of_iterations:
            self.iteration()

            self.visualisation.draw_path(self.shortest_path, self.shortest_path_convergence_iteration,
                                         self.iteration_counter, self.shortest_path_length, self.avg_path_length)

            self.condition.acquire()
            # self.condition.wait()

            lock = self.graph.lock

            lock.acquire()
            self.pheromone_evaporation()
            lock.release()

            self.condition.release()

        self.visualisation.draw_path(self.shortest_path, self.shortest_path_convergence_iteration,
                                     self.iteration_counter, self.shortest_path_length, self.avg_path_length, last=True)

    def create_ants(self):
        self.reset()

        ants = []

        for i in range(self.ants_count):
            ant = Ant(i, random.randint(0, self.graph.nodes_count - 1), self)  # , self.Alpha)
            ants.append(ant)

        return ants

    def iteration(self):
        self.avg_path_length = 0
        self.ants_count = 0
        self.iteration_counter += 1

        print("Starting %s iteration" % (self.iteration_counter,))

        for ant in self.ants:
            print("Starting ant %s" % (ant.id,))
            ant.run()

    def get_ants_count(self):
        return len(self.ants)

    def get_iteration_counter(self):
        return self.iteration_counter

    def get_max_number_of_iterations(self):
        return self.max_number_of_iterations

    def update_shortest_path(self, ant):
        self.shortest_path_length = ant.path_length
        self.shortest_path_matrix = ant.path_matrix
        self.shortest_path = ant.path
        self.shortest_path_convergence_iteration = self.iteration_counter

    def update(self, ant):
        lock = Lock()
        lock.acquire()

        print("Update called by ant %s" % (ant.id,))
        self.ants_count += 1

        self.avg_path_length += ant.path_length

        if ant.path_length < self.shortest_path_length:
            print("updating shortest path")
            self.update_shortest_path(ant)

        if self.ants_count == len(self.ants):
            self.avg_path_length /= self.ants_count

            print("Shortest path found: %s, %s, %s, %s" % (self.shortest_path,
                                                           self.shortest_path_length,
                                                           self.shortest_path_convergence_iteration,
                                                           self.avg_path_length))
            self.condition.acquire()
            self.condition.notify_all()
            self.condition.release()

        lock.release()

    def has_finished(self):
        return self.iteration_counter == self.max_number_of_iterations

    def pheromone_evaporation(self):
        evaporation, deposition = 0, 0

        for i in range(self.graph.nodes_count):
            for j in range(self.graph.nodes_count):
                if i != j:
                    pheromone = self.shortest_path_matrix[i][j] / self.shortest_path_length
                    evaporation = (1 - self.Alpha) * self.graph.get_pheromone(i, j)
                    deposition = self.Alpha * pheromone

                    self.graph.update_phermomene(i, j, evaporation + deposition)
