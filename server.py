from config.config_parser import parser
from utils.obstacle_generator import generate_obstacles
from utils.path_point_generator import generate_path_points
from genetic_algorithm import start_algorithm

import socket
import struct

path_points = []
threats = []

mapPointSocket = socket.socket(type=socket.SOCK_DGRAM)
mapPointSocket.bind(('localhost', 4651))

threatsPointSocket = socket.socket(type=socket.SOCK_DGRAM)
threatsPointSocket.bind(('localhost', 4652))


def set_map_points(data):
    global path_points

    numOfPoints = int.from_bytes(data[:8], "big")
    fmt = ">" + str(numOfPoints) + "d"
    temp_path_points = struct.unpack(fmt, data[8:])

    i = 0
    k = 0

    while i < numOfPoints / 2:
        path_points.append((temp_path_points[k],
                            temp_path_points[k + 1]))
        i += 1
        k += 2

    print("fmt : ", fmt)
    print(len(path_points))
    print(path_points)


def set_threats_points(data):
    global threats

    numOfThreats = int.from_bytes(data[:8], "big")
    numOfThreatsPoints = numOfThreats * 4 * 2

    fmt = ">" + str(numOfThreatsPoints) + "d"
    temp_threat_points = struct.unpack(fmt, data[8:])

    i = 0
    k = 0
    while i < numOfThreats:
        threats.append([(temp_threat_points[k],
                         temp_threat_points[k + 1]),
                        (temp_threat_points[k + 2],
                         temp_threat_points[k + 3]),
                        (temp_threat_points[k + 4],
                         temp_threat_points[k + 5]),
                        (temp_threat_points[k + 6],
                         temp_threat_points[k + 7])])
        i += 1
        k += 8

    print("fmt : ", fmt)
    print(len(threats))
    print(threats)

    path_points.append((150, 50))
    path_points.insert(0, (1000, 550))

    start_algorithm(threats, path_points)



def main():
    while True:
        mapPointsData = mapPointSocket.recv(80000)
        threatPointsData = threatsPointSocket.recv(8000)

        if 0 != mapPointsData:
            set_map_points(mapPointsData)

        if 0 != threatPointsData:
            set_threats_points(threatPointsData)


if __name__ == '__main__':
    main()
