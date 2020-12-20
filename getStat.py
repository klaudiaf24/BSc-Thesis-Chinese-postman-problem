#!/usr/bin/python3

import time
import OsmHelper as osmh
import RandomGraph
import FleuryAlgorithm
import HierholzerAlgorithm

numberOfSamples = 1


def setParam():
    diGraphParam = []
    BarbasiAlbertParam = []
    WattsStrogatzParam = []

    for k in [10, 50, 100, 500, 1000]:
        diGraphParam.append((k, 0.6))
        BarbasiAlbertParam.append((k, int(k / 2)))
        WattsStrogatzParam.append((k, int(k / 2), 0.6))

    # for k in range(10, 500, 10):
    #     diGraphParam.append((k, k*3))
    #     BarbasiAlbertParam.append((k, int(k - 1)))
    #     WattsStrogatzParam.append((k, int(k / 2), 0.2))
    #
    # for k in range(500, 1000, 50):
    #     diGraphParam.append((k, int(k * (k - 1) / 2)))
    #     BarbasiAlbertParam.append((k, int(k - 1)))
    #     WattsStrogatzParam.append((k, int(k / 2), 0.2))
    #
    # for k in range(1000, 10000, 100):
    #     diGraphParam.append((k, int(k * (k - 1) / 2)))
    #     BarbasiAlbertParam.append((k, int(k - 1)))
    #     WattsStrogatzParam.append((k, int(k / 2), 0.2))

    return diGraphParam, BarbasiAlbertParam, WattsStrogatzParam


def openFile():
    randomDiGraph_HierholzerAlgo_File = open('stat/randomDiGraph_HierholzerAlgo_File.txt', "a")
    randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File = open(
        'stat/randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File.txt', "a")
    randomGraphWithWattsStrogatzModel_HierholzerAlgo_File = open(
        'stat/randomGraphWithWattsStrogatzModel_HierholzerAlgo_File.txt', "a")
    
    randomGraphWithBarabasiAlbertModel_FleuryAlgo_File = open(
        'stat/randomGraphWithBarabasiAlbertModel_FleuryAlgo_File.txt', "a")
    randomGraphWithWattsStrogatzModel_FleuryAlgo_File = open(
        'stat/randomGraphWithWattsStrogatzModel_FleuryAlgo_File.txt', "a")

    return randomDiGraph_HierholzerAlgo_File, randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File, randomGraphWithWattsStrogatzModel_HierholzerAlgo_File, \
     randomGraphWithBarabasiAlbertModel_FleuryAlgo_File, randomGraphWithWattsStrogatzModel_FleuryAlgo_File


def closeFile(f1, f2, f3, f4, f5):
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()


randomDiGraph_HierholzerAlgo_File, \
randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File,\
randomGraphWithWattsStrogatzModel_HierholzerAlgo_File,\
randomGraphWithBarabasiAlbertModel_FleuryAlgo_File, \
randomGraphWithWattsStrogatzModel_FleuryAlgo_File = openFile()

randomDiGraph_Param, \
randomGraphWithBarabasiAlbertModel_Param, \
randomGraphWithWattsStrogatzModel_Param = setParam()

###############################################################

for param in randomDiGraph_Param:
    allTimes = 0
    edges = 0
    for _ in range(numberOfSamples):
        print("digraph {0}, {1}".format(str(param[0]), str(param[1])))
        graph = RandomGraph.getRandomDiGraph(param[0], param[1])
        edges += len(graph.edges)
        print("DONE")

        start = time.time()
        HierholzerAlgorithm.HierholzerAlgorithm(graph, True, 0)
        end = time.time()
        
        allTimes += end - start
    
    randomDiGraph_HierholzerAlgo_File.write(
        "{0:>7} {1:>7} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimes / numberOfSamples))

###############################################################

for param in randomGraphWithBarabasiAlbertModel_Param:
    allTimesF = 0
    allTimesH = 0
    edges = 0

    for _ in range(numberOfSamples):
        print("Barabasi {0}, {1}".format(str(param[0]), str(param[1])))
        graph = RandomGraph.getRandomGraphWithBarabasiAlbertModel(param[0], param[1])
        edges += len(graph.edges)
        print("DONE")

        startF = time.time()
        FleuryAlgorithm.FleuryAlgorithm(graph, False, 0)
        endF = time.time()

        startH = time.time()
        HierholzerAlgorithm.HierholzerAlgorithm(graph, False, 0)
        endH = time.time()

        allTimesF += endF - startF
        allTimesH += endH - startH

    randomGraphWithBarabasiAlbertModel_FleuryAlgo_File.write(
        "{0:>7} {1:>7} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesF / numberOfSamples))

    randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File.write(
        "{0:>7} {1:>7} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesH / numberOfSamples))

###############################################################

for param in randomGraphWithWattsStrogatzModel_Param:
    allTimesF = 0
    allTimesH = 0
    edges = 0

    for _ in range(numberOfSamples):
        print("Watts {0}, {1}".format(str(param[0]), str(param[1])))
        graph = RandomGraph.getRandomGraphWithWattsStrogatzModel(param[0], param[1], param[2])
        edges += len(graph.edges)
        print("DONE")

        startF = time.time()
        FleuryAlgorithm.FleuryAlgorithm(graph, False, 0)
        endF = time.time()

        startH = time.time()
        HierholzerAlgorithm.HierholzerAlgorithm(graph, False, 0)
        endH = time.time()

        allTimesF += endF - startF
        allTimesH += endH - startH

    randomGraphWithWattsStrogatzModel_FleuryAlgo_File.write(
        "{0:>7} {1:>7} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesF / numberOfSamples))

    randomGraphWithWattsStrogatzModel_HierholzerAlgo_File.write(
        "{0:>7} {1:>7} {2:>50}\n".format(param[0], edges / numberOfSamples, allTimesH / numberOfSamples))

###############################################################

closeFile(randomDiGraph_HierholzerAlgo_File, randomGraphWithWattsStrogatzModel_HierholzerAlgo_File, randomGraphWithBarabasiAlbertModel_HierholzerAlgo_File, randomGraphWithBarabasiAlbertModel_FleuryAlgo_File, randomGraphWithWattsStrogatzModel_FleuryAlgo_File)
