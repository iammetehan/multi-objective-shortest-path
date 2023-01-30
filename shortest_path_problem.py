import math
import numpy as np

from pymoo.core.problem import ElementwiseProblem
from utils.plotter import plot_chromosome
from shapely.geometry import Polygon, LineString


class ShortestPath(ElementwiseProblem):
    def __init__(self, obstacles, path_points, **kwargs):
        self.path_points = path_points
        self.obstacles = obstacles
        n_points = len(path_points)

        super(ShortestPath, self).__init__(
            n_var=n_points - 2,
            n_obj=2,
            xl=np.full(n_points - 2, 0),
            xu=np.full(n_points - 2, 1),
            vtype=int,
            **kwargs
        )

    def _evaluate(self, x, out, *args, **kwargs):
        x = np.insert(x, 0, True)
        x = np.insert(x, len(x), True)

        validity = chromosome_valid(x, self.obstacles, self.path_points)
        route_length = calculate_path_length(x, self.path_points)

        penalty = 100
        if validity:
            penalty = 0

        # plot_chromosome(self.obstacles, self.path_points, x, route_length, 0.0025)
        out['F'] = [route_length, penalty]


def chromosome_valid(chromosome, obstacles, path_points):
    path_point_1, path_point_2 = (), ()

    for i, gene in enumerate(chromosome):
        if gene:
            if not path_point_1:
                path_point_1 = path_points[i]
            else:
                path_point_2 = path_points[i]

            if path_point_1 and path_point_2:

                if path_overlaps_obstacle(path_point_1, path_point_2, obstacles):
                    return False

                path_point_1 = path_point_2
                path_point_2 = ()

    return True


def path_overlaps_obstacle(path_point_1, path_point_2, obstacles):
    path = LineString([path_point_1, path_point_2])

    for obstacle in obstacles:

        obstacle = Polygon(obstacle)
        if path.intersects(obstacle):
            return True

    return False


def calculate_path_length(chromosome, path_points):
    path_point_1, path_point_2 = (), ()
    length = 0

    for i, gene in enumerate(chromosome):
        if gene:
            last_path_point = path_points[i]

            if not path_point_1:
                path_point_1 = path_points[i]
            else:
                path_point_2 = path_points[i]

            if path_point_1 and path_point_2:
                length += distance(path_point_1, path_point_2)

                path_point_1 = path_point_2
                path_point_2 = ()

    return length


def distance(path_point_1, path_point_2):
    return math.sqrt((path_point_2[0] - path_point_1[0]) ** 2 + (path_point_2[1] - path_point_1[1]) ** 2)
