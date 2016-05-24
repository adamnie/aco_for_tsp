import sys

from ant_colony import AntColony
from data_generator import get_random_data
from graph import Graph

#default
from visualisation import *

num_nodes = 9

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])

    if num_nodes <= 10:
        num_ants = 20
        num_iterations = 10
        num_repetitions = 5
    else:
        num_ants = 30
        num_iterations = 40
        num_repetitions = 5

    stuff = get_random_data(num_nodes)
    cities = stuff[0]
    cost_mat = stuff[2]

    visualisation = Visualisation(stuff)
    visualisation.initialize_graph_with_nodes()

    if num_nodes < len(cost_mat):
        cost_mat = cost_mat[0:num_nodes]
        for i in range(0, num_nodes):
            cost_mat[i] = cost_mat[i][0:num_nodes]

    print(cost_mat)

    graph = Graph(num_nodes, cost_mat)
    best_path_vec = None
    best_path_cost = sys.maxsize
    for i in range(0, num_repetitions):
        graph.reset_pheromone()
        ant_colony = AntColony(graph, num_ants, num_iterations, visualisation, 0.1)
        ant_colony.start()
        visualisation.save_repetition(i+2)
        if ant_colony.shortest_path_length < best_path_cost:
            best_path_vec = ant_colony.shortest_path
            best_path_cost = ant_colony.shortest_path_length
            visualisation.save_best_path(best_path_vec)

    print("\n------------------------------------------------------------")
    print("                     Results                                ")
    print("------------------------------------------------------------")
    print("\nBest path = %s" % (best_path_vec,))
    for node in best_path_vec:
        print (cities[node] + " ")
    print("\nBest path cost = %s\n" % (best_path_cost,))

    visualisation.final_show_plot()

