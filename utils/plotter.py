import matplotlib.pyplot as plt
from config.config_parser import parser


plt.ion()


def plot_population(obstacles, path_points, population, path_lengths, duration):
    for i, chromosome in enumerate(population):
        reset_plot(obstacles, path_points)
        plot_chromosome(obstacles, path_points, chromosome, path_lengths[i], duration)


def plot_chromosome(obstacles, path_points, chromosome, path_length, duration):
    reset_plot(obstacles, path_points)

    path_x = [path_points[j][0] for j, c in enumerate(chromosome) if c == True]
    path_y = [path_points[j][1] for j, c in enumerate(chromosome) if c == True]

    plt.plot(path_x, path_y, '-')
    plt.text(1, int(parser['Plot Axes']['y_end']) + 1, f"\nPath Length:{path_length}")

    plt.pause(duration)
    plt.gcf().canvas.draw_idle()
    plt.gcf().canvas.start_event_loop(duration)


def reset_plot(obstacles, path_points):
    plt.clf()

    axes = parser['Plot Axes']
    plt.axis([int(axes['x_start']),
              int(axes['x_end']),
              int(axes['y_start']),
              int(axes['y_end'])])

    plot_obstacles(obstacles)
    plot_path_points(path_points)


def plot_path_points(path_points):
    path_point_x = [path_point[0] for path_point in path_points]
    path_point_y = [path_point[1] for path_point in path_points]

    plt.plot(path_point_x[1:-1], path_point_y[1:-1], "k.")
    plt.plot(path_point_x[0], path_point_y[0], "bo", label='Source')
    plt.plot(path_point_x[-1], path_point_y[-1], "go", label='Goal')

    plt.legend(loc="upper left")


def plot_obstacles(obstacles):
    for obstacle in obstacles:
        x_values, y_values = [], []

        for vertex in obstacle:
            x_values.append(vertex[0])
            y_values.append(vertex[1])

        plt.fill(x_values, y_values, 'r')
