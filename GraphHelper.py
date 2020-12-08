#!/usr/bin/python3

import networkx as nx
import random


def makeEulerianGraph(graph):
    listOfOddDegreeNodes = []
    dictOfOddDegreeNodesWithNeighbours = dict()

    for node in graph.nodes(data=True):
        if idOddNumber(graph.degree[node[0]]):
            listOfOddDegreeNodes.append(node[0])
            dictOfOddDegreeNodesWithNeighbours[node[0]] = []

    # if odd number of all odd degree nodes return None
    if idOddNumber(len(listOfOddDegreeNodes)):
        return None

    for node in listOfOddDegreeNodes:
        for neighbor in graph.neighbors(node):
            if neighbor in listOfOddDegreeNodes:
                list = dictOfOddDegreeNodesWithNeighbours[node]
                list.append(neighbor)

    while listOfOddDegreeNodes:
        node = getNodeWithTheSmallestNumberOfOddNeighboursButNotEmpty(dictOfOddDegreeNodesWithNeighbours)
        if node != -1:
            neighbor = dictOfOddDegreeNodesWithNeighbours[node][0]
            addFakeNode(graph, node, neighbor)
            removeUsedNodes(dictOfOddDegreeNodesWithNeighbours, listOfOddDegreeNodes, node, neighbor)
        else:
            minPath = findTheShortestPath(graph, listOfOddDegreeNodes)
            for idx in range(1, len(minPath)):
                node1 = minPath[idx - 1]
                node2 = minPath[idx]
                addFakeNode(graph, node1, node2)

            removeUsedNodes(dictOfOddDegreeNodesWithNeighbours, listOfOddDegreeNodes, minPath[0],
                            minPath[len(minPath) - 1])
    return graph


def addFakeNode(graph, node1, node2):
    weight = graph[node1][node2]['weight']

    x = (graph.nodes(data=True)[node1]['pos'][0] + graph.nodes(data=True)[node2]['pos'][0]) / 2 \
        + random.uniform(-0.1, 0.1)
    y = (graph.nodes(data=True)[node1]['pos'][1] + graph.nodes(data=True)[node2]['pos'][1]) / 2 \
        + random.uniform(-0.1, 0.1)
    fakeNodeIdx = len(graph.nodes)
    graph.add_node(fakeNodeIdx, pos=(x, y), isPostOffice=False, isFakeNode=True)

    graph.add_edge(node1, fakeNodeIdx, weight=0, isFakeRoute=True)
    graph.add_edge(fakeNodeIdx, node2, weight=weight, isFakeRoute=True)


def removeUsedNodes(dictOfOddDegreeNodesWithNeighbours, listOfOddDegreeNodes, node1, node2):
    removeNodeFromDictOfNeighboursAndList(node1, dictOfOddDegreeNodesWithNeighbours, listOfOddDegreeNodes)
    removeNodeFromDictOfNeighboursAndList(node2, dictOfOddDegreeNodesWithNeighbours,
                                          listOfOddDegreeNodes)


def removeNodeFromDictOfNeighboursAndList(node, dictOfNodes, listOdNodes):
    for n in dictOfNodes:
        if node in dictOfNodes[n]:
            list = dictOfNodes[n]
            list.remove(node)
    del dictOfNodes[node]
    listOdNodes.remove(node)


def findTheShortestPath(graph, listOdNodes):
    path = None
    minDist = float('inf')
    for n1 in listOdNodes:
        for n2 in listOdNodes:
            if n1 is not n2:
                # dist = nx.shortest_path_length(graph, n1, n2)
                dist = nx.shortest_path_length(graph, n1, n2, weight='weight')
                if dist < minDist:
                    # path = nx.shortest_path(graph, n1, n2)
                    path = nx.shortest_path(graph, n1, n2, weight='weight')
                    minDist = dist
    return path


def getNodeWithTheSmallestNumberOfOddNeighboursButNotEmpty(dictOfNodes):
    node = -1
    numberOfNeighbour = float('inf')

    for n in dictOfNodes:
        if dictOfNodes[n] and len(dictOfNodes[n]) < numberOfNeighbour:
            numberOfNeighbour = len(dictOfNodes[n])
            node = n
    return node


def idOddNumber(number):
    return number % 2


def isEulerianGraph(graph):
    return nx.is_eulerian(graph)
