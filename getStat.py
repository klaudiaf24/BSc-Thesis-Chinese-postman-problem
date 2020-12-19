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

    for k in [10, 50, 100, 500, 1000, 10000]:
        diGraphParam.append((k, k * 3))
        BarbasiAlbertParam.append((k, k / 2))
        WattsStrogatzParam.append((k, (k / 2), 0.2))

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
    randomDiGraph_FleuryAlgo_File = open('stat/randomDiGraph_FleuryAlgo_File.txt', "a")
    randomGraphWithBarabasiAlbertModel_FleuryAlgo_File = open(
        'stat/randomGraphWithBarabasiAlbertModel_FleuryAlgo_File.txt', "a")
    randomGraphWithWattsStrogatzModel_FleuryAlgo_File = open(
        'stat/randomGraphWithWattsStrogatzModel_FleuryAlgo_File.txt', "a")
    return randomDiGraph_FleuryAlgo_File, randomGraphWithBarabasiAlbertModel_FleuryAlgo_File, randomGraphWithWattsStrogatzModel_FleuryAlgo_File


def closeFile(f1, f2, f3):
    f1.close()
    f2.close()
    f3.close()


randomDiGraph_FleuryAlgo_File, \
randomGraphWithBarabasiAlbertModel_FleuryAlgo_File, \
randomGraphWithWattsStrogatzModel_FleuryAlgo_File = openFile()

randomDiGraph_Param, \
randomGraphWithBarabasiAlbertModel_Param, \
randomGraphWithWattsStrogatzModel_Param = setParam()

###############################################################

for param in randomDiGraph_Param:
    allTimes = 0
    for _ in range(numberOfSamples):
        start = time.time()
        FleuryAlgorithm.FleuryAlgorithm(RandomGraph.getRandomDiGraph(param[0], param[1]), 0)
        end = time.time()
        allTimes += end - start
    randomDiGraph_FleuryAlgo_File.write(
        "{0:>7} {0:>7} {0:>50}".format(param[0], param[1], allTimes / numberOfSamples))

###############################################################

for param in randomGraphWithBarabasiAlbertModel_Param:
    allTimes = 0
    for _ in range(numberOfSamples):
        start = time.time()
        FleuryAlgorithm.FleuryAlgorithm(RandomGraph.getRandomGraphWithBarabasiAlbertModel(param[0], param[1]))
        end = time.time()
        allTimes += end - start
    randomGraphWithBarabasiAlbertModel_FleuryAlgo_File.write(
        "{0:>7} {0:>7} {0:>50}".format(param[0], param[1], allTimes / numberOfSamples))

###############################################################

for param in randomGraphWithWattsStrogatzModel_Param:
    allTimes = 0
    for _ in range(numberOfSamples):
        start = time.time()
        FleuryAlgorithm.FleuryAlgorithm(RandomGraph.getRandomGraphWithWattsStrogatzModel(param[0], param[1], param[3]),
                                        0)
        end = time.time()
        allTimes += end - start
    randomGraphWithWattsStrogatzModel_FleuryAlgo_File.write(
        "{0:>7} {0:>7} {0:>4} {0:>50}".format(param[0], param[1], param[3], allTimes / numberOfSamples))

###############################################################

closeFile(randomDiGraph_FleuryAlgo_File, randomGraphWithBarabasiAlbertModel_FleuryAlgo_File,
          randomGraphWithWattsStrogatzModel_FleuryAlgo_File)
