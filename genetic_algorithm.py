import numpy as np

from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination
from shortest_path_problem import ShortestPath, calculate_path_length
from utils.plotter import plot_population


def start_algorithm(obstacles, path_points):
    problem = ShortestPath(obstacles, path_points)

    algorithm = NSGA2(
        pop_size=20,
        sampling=BinaryRandomSampling(),
        mutation=BitflipMutation(),
        crossover=TwoPointCrossover(),
        eliminate_duplicates=True
    )

    termination = DefaultMultiObjectiveTermination()

    res = minimize(
        problem,
        algorithm,
        termination,
        seed=1,
    )

    res.X = np.insert(res.X, 0, values=True, axis=1)
    res.X = np.insert(res.X, len(res.X[0]), values=True, axis=1)

    print(res.X)

    path_lengths = []

    for chromosome in res.X:
        path_lengths.append(calculate_path_length(chromosome, path_points))

    plot_population(obstacles, path_points, res.X, path_lengths, 5)
