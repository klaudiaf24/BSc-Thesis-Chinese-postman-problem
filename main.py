#!/usr/bin/python3

import Visualization as vis
import OsmHelper as osmh
import RandomGraph as rg
import networkx as nx

if __name__ == "__main__":
    # graph = osmh.getGraphFromOsm(left=19.92514, bottom=50.07657, right=19.93317, top=50.07974) #krk
    # graph = osmh.getGraphFromOsm(left=19.92435, bottom=50.07992, right=19.92837, top=50.08150) #poznanska
    # graph = osmh.getGraphFromOsm(left=22.08252, bottom=49.56268, right=22.09859, top=49.56908) #osiedlowa
    # graph = osmh.getGraphFromOsm(left=22.08691, bottom=49.55106, right=22.09495, top=49.55426) #nwm
    # graph = osmh.getGraphFromOsm(left=22.20569, bottom=49.55288, right=22.21033, top=49.55448) #Lipińskiego

    # graph = osmh.getGraphFromOsm(left=22.03886, bottom=49.57915, right=22.04288, top=49.58075)  # długie

    # graph = rg.getRandomGraphWithBarabasiAlbertModel(7, 3)
    # graph = rg.getRandomGraphWithWattsStrogatzModel(7, 4, 10)
    graph = rg.getRandomDiGraph(5, 10)
    print(nx.is_eulerian(graph))
    vis.draw(graph, printFakeEdges=True)
