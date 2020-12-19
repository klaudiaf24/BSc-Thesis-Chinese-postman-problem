#!/usr/bin/python3

import random
import networkx as nx


def makeEulerianDiGraph(graph):
    diff = [None] * len(
        graph.nodes)  # list with nodes difference : predecessors nodes - successors nodes / input nodes - output nodes
    for node in graph.nodes(data=True):
        diff[node[0]] = len(graph.pred[node[0]]) - len(graph.succ[node[0]])

    negNodes = []
    posNodes = []
    for node in range(0, len(diff)):
        if diff[node] < 0:
            for rep in range(-1 * diff[node]):
                negNodes.append(node)
        if diff[node] > 0:
            for rep in range(diff[node]):
                posNodes.append(node)

    if idOddNumber(len(negNodes) - len(posNodes)):
        return None

    # listWithAllPerm = list(
    #     list(zip(r, p)) for (r, p) in zip(itertools.repeat(posNodes), itertools.permutations(negNodes)))
    listOfRandomParams = list()
    for _ in range(0, 100):
        random.shuffle(negNodes)
        listOfRandomParams.append(list(zip(posNodes, negNodes)))

    minPath = getOptimalAdditionalPaths(graph, listOfRandomParams)
    appendFakeEdges(graph, minPath)


def makeEulerianGraph(graph):
    listOfOddDegreeNodes = []
    for node in graph.nodes(data=True):
        if idOddNumber(graph.degree[node[0]]):
            listOfOddDegreeNodes.append(node[0])

    if idOddNumber(len(listOfOddDegreeNodes)):
        return None

    listWithAllPerm = allPairCombination(listOfOddDegreeNodes)
    minPath = getOptimalAdditionalPaths(graph, listWithAllPerm)
    appendFakeEdges(graph, minPath)


def allPairCombination(listOfNodes):
    if len(listOfNodes) < 2:
        yield []
        return
    else:
        a = listOfNodes[0]
        for i in range(1, len(listOfNodes)):
            pair = (a, listOfNodes[i])
            for rest in allPairCombination(listOfNodes[1:i] + listOfNodes[i + 1:]):
                yield [pair] + rest


def appendFakeEdges(graph, minPath):
    for pair in minPath:
        path = nx.shortest_path(graph, pair[0], pair[1], weight='weight')
        for idx in range(1, len(path)):
            node1 = path[idx - 1]
            node2 = path[idx]
            graph.add_edge(node1, node2, weight=graph[node1][node2][0]['weight'], isFakeRoute=True)


def getOptimalAdditionalPaths(graph, listWithAllPerm):
    minDist = float('inf')
    minPath = []
    for currentList in listWithAllPerm:
        dist = 0
        for pair in currentList:
            dist += nx.shortest_path_length(graph, source=pair[0], target=pair[1], weight='weight')
        if dist < minDist:
            minDist = dist
            minPath = currentList
    return minPath


def idOddNumber(number):
    return number % 2


def isEulerianGraph(graph):
    return nx.is_eulerian(graph)


def getAdjList(graph):
    adjList = dict()
    for node in graph.nodes():
        neighbours = []
        for neighbour in graph.adj[node]:
            for _ in graph.adj[node][neighbour]:
                neighbours.append(neighbour)
        adjList[node] = neighbours
    return adjList
