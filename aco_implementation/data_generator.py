from string import ascii_uppercase
from random import randrange
from math import hypot


def get_random_data(n):
    result = []
    cities_map = {}

    sample = (['Bergen',  'Hammerfest',  'Kirkenes',  'Kristiansand',  'Lillehammer',  'Oslo',  'Stavanger',  'Sosnowiec',  'Trondheim',  'Warszawa',  'Vinje',  'Krakow',  'Sogndal',  'Vang'],
     [[0, 2196, 2258, 439, 440, 496, 207, 1808, 662, 432, 274, 167, 219, 278],
      [2170,   0,   480,   2191,   1813,   1870,   2404,   377,   1537,   1834,   2100,   2034,   1951,   1918],
      [2232, 480,   0,   2222,   1844,   1901,   2435,   806,   1598,   1895,   2131,   2095,   2012,   1980],
      [439, 2193, 2224, 0, 503, 321, 231, 1962, 816, 820, 266, 487, 584, 521],
      [440, 1827, 1848, 505, 0, 184, 546, 1484, 338, 381, 363, 277, 279, 162],
      [496, 1872, 1903, 321, 181, 0, 535, 1640, 495, 562, 230, 333, 333, 236],
      [207, 2407, 2437, 231, 546, 534, 0, 1975, 830, 638, 250, 343, 395, 454],
      [1782,   378,   806,   1962,   1484,   1641,   1962,   0,   1148,   1445,   1820,   1645,   1562,   1530],
      [636, 1537, 1599, 817, 339, 496, 816, 1148, 0, 300, 674, 500, 417, 384],
      [432, 1834, 1896, 820, 381, 563, 638, 1445, 300, 0, 601, 347, 275, 355],
      [275, 2103, 2134, 244, 363, 230, 279, 1821, 675, 601, 0, 275, 327, 348],
      [167, 2033, 2095, 517, 277, 333, 348, 1645, 499, 347, 275, 0, 72, 115],
      [219, 1951, 2012, 585, 279, 334, 400, 1562, 417, 275, 327, 72, 0, 117],
      [278, 1918, 1980, 521, 162, 237, 459, 1529, 384, 355, 347, 115, 117, 0]])

    for index, c in enumerate(ascii_uppercase):
        if index < n:
            while True:
                random = (randrange(-50, 50), randrange(-50, 50))
                if random not in cities_map.values():
                    cities_map[c] = random
                    break

    cities_distances = []

    for city1 in cities_map.keys():
        local_list = []
        for city2 in cities_map.keys():
            if city1 == city2:
                local_list.append(0)
            else:
                local_list.append(int((hypot(cities_map[city1][0] - cities_map[city2][0],
                                             cities_map[city1][1] - cities_map[city2][1])))*10)
        cities_distances.append(local_list)

    result.append(cities_map.keys())
    result.append(cities_distances)

    return result


data = get_random_data(3)

for each in data:
    print each
