from collections import deque
import copy
import random


def getOutEdges(graph, node):
    edges = []
    for neighbour in list(graph.neighbors(node)):
        for level in graph[node][neighbour]:
            edges.append((node, neighbour, level))
    return edges


def checkOutDegree(graph, node, isDirected):
    if isDirected:
        return graph.out_degree(node)
    else:
        return graph.degree(node)


def HierholzerAlgorithm(graph, isDirected, startNode):
    graphCopy = copy.deepcopy(graph)
    EulerCycle = list()
    stackOfNodes = deque()

    node = startNode
    EulerCycle.append(node)

    while True:
        if checkOutDegree(graphCopy, node, isDirected):
            edge = random.choice(getOutEdges(graphCopy, node))
            stackOfNodes.append(node)
            graphCopy.remove_edge(edge[0], edge[1], key=edge[2])
            node = edge[1]
        else:
            node = stackOfNodes.pop()
            EulerCycle.append(node)

        if not stackOfNodes:
            break

    EulerCycle.reverse()
    return EulerCycle
