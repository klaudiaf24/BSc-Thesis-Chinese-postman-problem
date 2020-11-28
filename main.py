#!/usr/bin/python3

import Visualization as vis
import OsmHelper as osmh
import RandomGraph as rg

import DepthFirstSearch as dfs
import ChristofidesAlgorithm as ch
import HeldKarpAlgorithm as hk


if __name__ == "__main__":
    graph = rg.getRandomGraphWithWattsStrogatzModel(7, 4, 10)
    vis.draw(graph)
