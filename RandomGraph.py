#!/usr/bin/python3

import random
import networkx as nx

def addRandomWeight(graph):
    for elem in graph.edges:
        graph[elem[0]][elem[1]]['weight'] = random.randint(1, 10)


def setPostOfficeOnFirstNode(graph):
    for idx in graph.nodes:
        graph.nodes[idx]['isPostOffice'] = 'False'

    postOffice = graph.nodes[0]
    postOffice['isPostOffice'] = True


def getRandomGraphWithWattsStrogatzModel(numberOfNodes, numberOfNearestNeighborsInRing, probability):
    graph = nx.watts_strogatz_graph(numberOfNodes, numberOfNearestNeighborsInRing, probability)
    addRandomWeight(graph)
    setPostOfficeOnFirstNode(graph)
    return graph


def getRandomGraphWithBarabasiAlbertModel(numberOfNodes, numberOfEdgesToAttach):
    pass
