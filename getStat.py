#!/usr/bin/python3

import time
import RandomGraph
import FleuryAlgorithm
import HierholzerAlgorithm
import networkx

numberOfSamples = 5
probability = 0.6


def setParam():
    diGraphParam = []
    BarbasiAlbertParam = []
    WattsStrogatzParam = []

    for k in [50]:#, 100, 200, 500, 700, 1000, 2000]:
        diGraphParam.append((k, probability))
        BarbasiAlbertParam.append((k, int(k / 2)))
        WattsStrogatzParam.append((k, int(k / 2), probability))

    return diGraphParam, BarbasiAlbertParam, WattsStrogatzParam


def openFile():
    f1 = open('stat/Hierholzer/randomDiGraph_HierholzerAlgo_File.txt', "a")
    f2 = open('stat/Hierholzer/randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File.txt', "a")
    f3 = open('stat/Hierholzer/randomGraphWithWattsStrogatzModel_HierholzerAlgo_File.txt', "a")

    f4 = open('stat/Fleury/randomGraphWithBarabasiAlbertModel_FleuryAlgo_File.txt', "a")
    f5 = open('stat/Fleury/randomGraphWithWattsStrogatzModel_FleuryAlgo_File.txt', "a")

    return f1, f2, f3, f4, f5


def closeFile(f1, f2, f3, f4, f5):
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()


randomDiGraph_HierholzerAlgo_File, randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File, \
randomGraphWithWattsStrogatzModel_HierholzerAlgo_File, randomGraphWithBarabasiAlbertModel_FleuryAlgo_File, \
randomGraphWithWattsStrogatzModel_FleuryAlgo_File = openFile()

randomDiGraph_Param, randomGraphWithBarabasiAlbertModel_Param, randomGraphWithWattsStrogatzModel_Param = setParam()

###############################################################

for param in randomDiGraph_Param:
    allTimes = 0
    edges = 0
    for _ in range(numberOfSamples):
        filename = "stat/graph/diGraph_node{0}_sample{1}.txt".format(param[0], _)
        graph = RandomGraph.getRandomDiGraph(param[0], param[1])
        networkx.write_adjlist(graph, filename)
        edges += len(graph.edges)

        start = time.time()
        HierholzerAlgorithm.HierholzerAlgorithm(graph, True, 0)
        end = time.time()

        allTimes += end - start

    randomDiGraph_HierholzerAlgo_File.write(
        "{0:>7} {1:>20} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimes / numberOfSamples))

###############################################################

for param in randomGraphWithBarabasiAlbertModel_Param:
    allTimesF = 0
    allTimesH = 0
    edges = 0

    for _ in range(numberOfSamples):
        filename = "stat/graph/BarabasiAlbertModelGraph_node{0}_sample{1}.txt".format(param[0], _)
        graph = RandomGraph.getRandomGraphWithBarabasiAlbertModel(param[0], param[1])
        networkx.write_adjlist(graph, filename)
        edges += len(graph.edges)

        startF = time.time()
        FleuryAlgorithm.FleuryAlgorithm(graph, False, 0)
        endF = time.time()

        startH = time.time()
        HierholzerAlgorithm.HierholzerAlgorithm(graph, False, 0)
        endH = time.time()

        allTimesF += endF - startF
        allTimesH += endH - startH

    randomGraphWithBarabasiAlbertModel_FleuryAlgo_File.write(
        "{0:>7} {1:>20} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesF / numberOfSamples))

    randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File.write(
        "{0:>7} {1:>20} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesH / numberOfSamples))

###############################################################

for param in randomGraphWithWattsStrogatzModel_Param:
    allTimesF = 0
    allTimesH = 0
    edges = 0

    for _ in range(numberOfSamples):
        filename = "stat/graph/WattsStrogatzModelGraph_node{0}_sample{1}.txt".format(param[0], _)
        graph = RandomGraph.getRandomGraphWithWattsStrogatzModel(param[0], param[1], param[2])
        networkx.write_adjlist(graph, filename)
        edges += len(graph.edges)

        startF = time.time()
        FleuryAlgorithm.FleuryAlgorithm(graph, False, 0)
        endF = time.time()

        startH = time.time()
        HierholzerAlgorithm.HierholzerAlgorithm(graph, False, 0)
        endH = time.time()

        allTimesF += endF - startF
        allTimesH += endH - startH

    randomGraphWithWattsStrogatzModel_FleuryAlgo_File.write(
        "{0:>7} {1:>20} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesF / numberOfSamples))

    randomGraphWithWattsStrogatzModel_HierholzerAlgo_File.write(
        "{0:>7} {1:>20} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesH / numberOfSamples))

###############################################################

closeFile(randomDiGraph_HierholzerAlgo_File, randomGraphWithWattsStrogatzModel_HierholzerAlgo_File,
          randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File, randomGraphWithBarabasiAlbertModel_FleuryAlgo_File,
          randomGraphWithWattsStrogatzModel_FleuryAlgo_File)
