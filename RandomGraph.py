#!/usr/bin/python3

import random
import networkx as nx
import GraphHelper as gh


def getRandomDiGraph(numberOfNodes, numberOfEdges):
    while True:
        graph = nx.gnm_random_graph(numberOfNodes, numberOfEdges, seed=4, directed=True)
        while not nx.is_strongly_connected(graph):
            graph = nx.gnm_random_graph(numberOfNodes, numberOfEdges, seed=4, directed=True)
        setAttriubutes(graph)
        graph = nx.MultiDiGraph(graph)
        if not gh.isEulerianGraph(graph):
            gh.makeEulerianDiGraph(graph)
        if graph != None:
            break
    return graph


def getRandomGraphWithWattsStrogatzModel(numberOfNodes, numberOfNearestNeighborsInRing, probability):
    while True:
        graph = nx.watts_strogatz_graph(numberOfNodes, numberOfNearestNeighborsInRing, probability)
        setAttriubutes(graph)
        graph = nx.MultiGraph(graph)
        graph = improveIfNecessaryGraph(graph)
        if graph != None:
            break
    return graph


def getRandomGraphWithBarabasiAlbertModel(numberOfNodes, numberOfEdgesToAttach):
    while True:
        graph = nx.barabasi_albert_graph(numberOfNodes, numberOfEdgesToAttach)
        setAttriubutes(graph)
        graph = nx.MultiGraph(graph)
        graph = improveIfNecessaryGraph(graph)
        if graph != None:
            break
    return graph


def improveIfNecessaryGraph(graph):
    if not gh.isEulerianGraph(graph):
        gh.makeEulerianGraph(graph)
    return graph


def setAttriubutes(graph):
    position = nx.spring_layout(graph, k=0.4, iterations=20)#, seed=2)
    nx.set_node_attributes(graph, position, 'pos')
    addRandomWeight(graph)
    setPostOfficeOnFirstNode(graph)
    nx.set_edge_attributes(graph, False, 'isFakeRoute')


def addRandomWeight(graph):
    for elem in graph.edges:
        graph[elem[0]][elem[1]]['weight'] = random.randint(1, 10)


def setPostOfficeOnFirstNode(graph):
    nx.set_node_attributes(graph, False, 'isPostOffice')
    postOffice = graph.nodes[0]
    postOffice['isPostOffice'] = True
