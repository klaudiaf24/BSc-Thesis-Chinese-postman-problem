#!/usr/bin/python3

import Visualization as vis
import OsmHelper as osmh
import RandomGraph as rg
import networkx as nx

import HierholzerAlgorithm as ha
import FleuryAlgorithm as fa
import GraphHelper
import time


def showPath(path, graph, ranges = []):
    edgesToHighlight = []
    visitedEdge = dict()
    for node in graph.nodes():
        for neighbour in list(graph.neighbors(node)):
            for level in list(graph[node][neighbour]):
                visitedEdge[(node, neighbour, level)] = False

    number = 1
    for id in range(1, len(path)):
        level = 0
        while visitedEdge[((path[id - 1], path[id], level))]:
            level += 1
        visitedEdge[((path[id - 1], path[id], level))] = True

        edgesToHighlight.append((path[id - 1], path[id], level))
        vis.draw(graph, edgesToHighlight, True, ranges, number)
        number += 1


if __name__ == "__main__":
    startNode = 0
    # graph = osmh.getGraphFromOsm(left=19.92514, bottom=50.07657, right=19.93317, top=50.07974) #krk
    # graph = osmh.getGraphFromOsm(left=19.92435, bottom=50.07992, right=19.92837, top=50.08150) #poznanska
    # graph = osmh.getGraphFromOsm(left=22.08252, bottom=49.56268, right=22.09859, top=49.56908) #osiedlowa
    # graph = osmh.getGraphFromOsm(left=22.20569, bottom=49.55288, right=22.21033, top=49.55448) #Lipińskiego
    #
    # graph = osmh.getGraphFromOsm(left=19.9152, bottom=50.0722, right=19.9270, top=50.0802)  #
    # graph = osmh.getGraphFromOsm(left=19.9208, bottom=50.0777, right=19.9259, top=50.0814)  #
    # graph = osmh.getGraphFromOsm(left=19.91389, bottom=50.06919, right=19.91725, top=50.07131)  #
    # graph = osmh.getGraphFromOsm(left=19.92046, bottom=50.07634, right=19.92297, top=50.07858)  #
    # graph = osmh.getGraphFromOsm(left=19.92397, bottom=50.07764, right=19.92595, top=50.07924)  #

    ########################################################################################################

    # graph, ranges = osmh.getGraphFromOsm(left=19.90110, bottom=50.07229, right=19.90473, top=50.07429)
    graph, ranges = osmh.getGraphFromOsm(left=19.90040, bottom=50.07430, right=19.90448, top=50.07620)  # TEN

    # graph, ranges = osmh.getGraphFromOsm(left=20.04038, bottom=50.05407, right=20.04790, top=50.05817)

    #graph = graph.to_undirected()

    ########################################################################################################
    # graph = rg.getRandomGraphWithBarabasiAlbertModel(7, 5)
    # graph = rg.getRandomGraphWithWattsStrogatzModel(6, 4, 0)
    # graph = rg.getRandomDiGraph(700, 0.5)
    # graph = nx.fast_gnp_random_graph(2000, 0.75, seed=1, directed=True)

    print(nx.is_eulerian(graph))
    print(len(graph.nodes))
    print(len(graph.edges))


    vis.draw(graph, printFakeEdges=True, ranges=ranges)
    start = time.time()
    path = ha.HierholzerAlgorithm(graph, True, startNode)
    end = time.time()

    toRemove = []
    last = None
    for id in range(0, len(path)):
        if last == path[id]:
            toRemove.append(id)
        last = path[id]

    for _ in sorted(toRemove, reverse=True):
        del path[_]

    print(end - start)
    print(path)
    showPath(path, graph, ranges)

    # #
    # start = time.time()
    # path = fa.FleuryAlgorithm(graph, startNode)
    # end = time.time()
    # print(end - start)
    # print(path)
    # showPath(path, graph)
