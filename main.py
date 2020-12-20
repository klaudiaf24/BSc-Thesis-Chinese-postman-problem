#!/usr/bin/python3

import Visualization as vis
import OsmHelper as osmh
import RandomGraph as rg
import networkx as nx

import HierholzerAlgorithm as ha
import FleuryAlgorithm as fa
import GraphHelper
import time

def showPath(path, graph):
    edgesToHighlight = []
    visitedEdge = dict()
    for node in graph.nodes():
        for neighbour in list(graph.neighbors(node)):
            for level in list(graph[node][neighbour]):
                visitedEdge[(node, neighbour, level)] = False

    for id in range(1, len(path)):
        level = 0
        while visitedEdge[((path[id - 1], path[id], level))]:
            level += 1
        visitedEdge[((path[id - 1], path[id], level))] = True

        edgesToHighlight.append((path[id - 1], path[id], level))
        vis.draw(graph, edgesToHighlight, False)


if __name__ == "__main__":
    startNode = 0
    # graph = osmh.getGraphFromOsm(left=19.92514, bottom=50.07657, right=19.93317, top=50.07974) #krk
    # graph = osmh.getGraphFromOsm(left=19.92435, bottom=50.07992, right=19.92837, top=50.08150) #poznanska
    # graph = osmh.getGraphFromOsm(left=22.08252, bottom=49.56268, right=22.09859, top=49.56908) #osiedlowa
    # graph = osmh.getGraphFromOsm(left=22.20569, bottom=49.55288, right=22.21033, top=49.55448) #Lipińskiego
    #
    # graph = osmh.getGraphFromOsm(left=22.03886, bottom=49.57915, right=22.04288, top=49.58075)  # długie
    #
    # graph = osmh.getGraphFromOsm(left=19.9152, bottom=50.0722, right=19.9270, top=50.0802)  #
    # graph = osmh.getGraphFromOsm(left=19.9208, bottom=50.0777, right=19.9259, top=50.0814)  #
    # graph = osmh.getGraphFromOsm(left=19.91389, bottom=50.06919, right=19.91725, top=50.07131)  #
    # graph = osmh.getGraphFromOsm(left=19.92046, bottom=50.07634, right=19.92297, top=50.07858)  #

    # graph = osmh.getGraphFromOsm(left=19.92397, bottom=50.07764, right=19.92595, top=50.07924)  #

    # graph = rg.getRandomGraphWithBarabasiAlbertModel(8, 4)
    # graph = rg.getRandomGraphWithWattsStrogatzModel(7, 4, 0.2)
    # listt = []
    # for k in range(10, 500, 20):
    #     listt.append((k, k * 10))

    # for l in listt:
    # graph = rg.getRandomDiGraph(50, 0.8)

    graph = rg.getRandomGraphWithWattsStrogatzModel(1000, 50, 0.6)

    print(nx.is_eulerian(graph))

    # vis.draw(graph, printFakeEdges=True)
    # path = fa.FleuryAlgorithm(graph)
    start = time.time()
    path2 = ha.HierholzerAlgorithm(graph, False, startNode)
    print(time.time() - start)
    # # # print(path)
    # print(path2)
    # #
    # # # showPath(path, graph)
    # showPath(path2, graph)
