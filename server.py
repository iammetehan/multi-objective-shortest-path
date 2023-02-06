from config.config_parser import parser
from utils.obstacle_generator import generate_obstacles
from utils.path_point_generator import generate_path_points
from genetic_algorithm import start_algorithm

import socket
import struct

path_points = []
threats = []

src = (0, 0)
dst = (0, 0)

mapPointSocket = socket.socket(type=socket.SOCK_DGRAM)
mapPointSocket.bind(('localhost', 4651))

threatsPointSocket = socket.socket(type=socket.SOCK_DGRAM)
threatsPointSocket.bind(('localhost', 4652))

srcDstSocket = socket.socket(type=socket.SOCK_DGRAM)
srcDstSocket.bind(('localhost', 4653))

startSimSocket = socket.socket(type=socket.SOCK_DGRAM)
startSimSocket.bind(('localhost', 4654))


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


def set_src_dst(data):
    global src
    global dst

    temp_src_dst_points = struct.unpack(">4d", data)
    src = (temp_src_dst_points[0], temp_src_dst_points[1])
    dst = (temp_src_dst_points[2], temp_src_dst_points[3])


def find_paths():
    global threats
    global path_points

    path_points.insert(0, src)
    path_points.append(dst)

    print("Algorithm started!")
    send_results(start_algorithm(threats, path_points))


def send_results(data):

    # route = convert_to_int_indices(data[1])

    # print(route)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(data), ('localhost', 4655))

    print("send_results - success!")


def convert_to_int_indices(indices):
    intIndices = []
    index = 0
    while index < len(indices):
        if indices[index]:
            intIndices.append(index)
        index = index + 1

    return intIndices


def main():
    while True:
        mapPointsData = mapPointSocket.recv(80000)
        threatPointsData = threatsPointSocket.recv(8000)
        srcDstData = srcDstSocket.recv(1024)
        startSimData = startSimSocket.recv(1024)

        if 0 != mapPointsData:
            set_map_points(mapPointsData)

        if 0 != threatPointsData:
            set_threats_points(threatPointsData)

        if 0 != srcDstData:
            set_src_dst(srcDstData)

        if 0 != startSimData:
            if "FindPath" == startSimData.decode():
                find_paths()


if __name__ == '__main__':
    main()
