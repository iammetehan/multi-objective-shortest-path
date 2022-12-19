from config.config_parser import parser
from utils.obstacle_generator import generate_obstacles
from utils.path_point_generator import generate_path_points
from genetic_algorithm import start_algorithm

obstacles = []
path_points = []


def main():
    _init_obstacles()
    _init_path_points()

    print("obstacles :", obstacles)
    print("path_points :", path_points)

    start_algorithm(obstacles, path_points)


def _init_path_points():
    if parser['Path Points'].getboolean('generate_randomly'):
        generate_path_points(path_points, obstacles)

    else:
        # eval will create the list from the string representation of list in config.ini
        path_points.append((0, 0))
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            path_points.append(element)
        path_points.append((15, 15))


def _init_obstacles():
    if parser['Obstacles'].getboolean('generate_randomly'):
        number_of_obstacles = int(parser['Obstacles']['number_of_obstacles'])
        generate_obstacles(obstacles, number_of_obstacles)

    else:
        for i in range(int(parser['Hardcoded Obstacles']['number_of_hardcoded_obstacles'])):
            obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i + 1}"])
            obstacles.append(obstacle)


if __name__ == '__main__':
    main()
