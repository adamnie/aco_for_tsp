from string import ascii_uppercase
from random import randrange
from math import hypot


def get_random_data(n):
    result = []
    cities_map = {}

    for index, c in enumerate(ascii_uppercase):
        if index < n:
            while True:
                random = (randrange(-50, 50), randrange(-50, 50))
                if random not in cities_map.values():
                    cities_map[c] = random
                    break

    cities_distances = []

    for city1 in list(cities_map.keys()):
        local_list = []
        for city2 in list(cities_map.keys()):
            local_list.append(int((hypot(cities_map[city1][0] - cities_map[city2][0],
                                         cities_map[city1][1] - cities_map[city2][1])))*10)
        cities_distances.append(local_list)

    result.append(list(cities_map.keys()))
    result.append(list(cities_map.values()))
    result.append(cities_distances)

    return result
