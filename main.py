#!/usr/bin/python3

import Visualization as vis
import OsmHelper as osmh
import RandomGraph as rg
import networkx as nx

import HierholzerAlgorithm as ha
import FleuryAlgorithm as fa

if __name__ == "__main__":
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

    # graph = rg.getRandomGraphWithBarabasiAlbertModel(100, 4500)
    graph = rg.getRandomGraphWithWattsStrogatzModel(7, 4, 4444)
    # graph = rg.getRandomDiGraph(10, 30)
    print(nx.is_eulerian(graph))
    vis.draw(graph, printFakeEdges=True)
    # ha.printCircuit(graph)
    # fa.FleuryAlgorithm(graph, 0)
