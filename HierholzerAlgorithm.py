from collections import deque
import GraphHelper


def getNextOutEdge(adjList, node):
    return adjList[node][0]


def checkOutDegree(adjList, node):
    return len(adjList[node])


def removeEdge(adjList, u, v, isDirected):
    adjList[u].remove(v)
    if not isDirected:
        adjList[v].remove(u)


def HierholzerAlgorithm(graph, isDirected, startNode):
    adjList = GraphHelper.getAdjList(graph)
    EulerCycle = list()
    stackOfNodes = deque()

    node = startNode
    EulerCycle.append(node)

    while True:
        if checkOutDegree(adjList, node):
            v = getNextOutEdge(adjList, node)
            stackOfNodes.append(node)
            removeEdge(adjList, node, v, isDirected)
            node = v
        else:
            node = stackOfNodes.pop()
            EulerCycle.append(node)

        if not stackOfNodes:
            break

    EulerCycle.reverse()
    return EulerCycle
