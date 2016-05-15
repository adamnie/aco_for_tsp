from threading import Lock


class Graph:

    def __init__(self, nodes_count, distance_matrix, pheromone_matrix=None):
        self.nodes_count = nodes_count

        if len(distance_matrix) != nodes_count:
            raise Exception("Matrix length is: %s, but number of nodes is %s" % (len(distance_matrix), nodes_count))

        self.distance_matrix = distance_matrix
        self.lock = Lock()

        avg_dist = self.get_average_distance()
        self.pheromone_constant = 1.0 / (self.nodes_count * 0.5 * avg_dist)

        if pheromone_matrix is None:
            self.pheromone_matrix = []
            for i in range(nodes_count):
                self.pheromone_matrix.append([0] * nodes_count)
        else:
            self.pheromone_matrix = pheromone_matrix

    def get_distance(self, node_A, node_B):
        return self.distance_matrix[node_A][node_B]

    def get_pheromone(self, node_A, node_B):
        return self.pheromone_matrix[node_A][node_B]

    def update_phermomene(self, node_A, node_B, value):
        lock = Lock()
        lock.acquire()
        self.pheromone_matrix[node_A][node_B] = value
        lock.release()

    def reset_pheromone(self):
        lock = Lock()
        lock.acquire()
        for i in range(self.nodes_count):
            for j in range(self.nodes_count):
                self.pheromone_matrix[i][j] = self.pheromone_constant
        lock.release()

    def get_average_distance(self):
        return self.average(self.distance_matrix)

    def get_average_pheromone(self):
        return self.average(self.pheromone_matrix)

    def average(self, matrix):
        sum = 0
        for r in range(self.nodes_count):
            for s in range(self.nodes_count):
                sum += matrix[r][s]

        avg = sum / (self.nodes_count * self.nodes_count)
        return avg