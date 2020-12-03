#!/usr/bin/python3

import Visualization as vis
import OsmHelper as osmh
import RandomGraph as rg

import DepthFirstSearch as dfs
import ChristofidesAlgorithm as ch
import HeldKarpAlgorithm as hk


if __name__ == "__main__":
    graph = osmh.getGraphFromOsm(left=22.08252, bottom=49.56268, right=22.09859, top=49.56908) 
    # graph = osmh.getGraphFromOsm(left=22.20569, bottom=49.55288, right=22.21033, top=49.55448)

    # graph = osmh.getGraphFromOsm(left=22.03886, bottom=49.57915, right=22.04288, top=49.58075)

    # graph = rg.getRandomGraphWithBarabasiAlbertModel(8, 6)
    # graph = rg.getRandomGraphWithWattsStrogatzModel(7, 4, 10)

    vis.draw(graph)

