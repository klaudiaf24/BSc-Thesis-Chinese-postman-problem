import GraphHelper


def DFS(adjList, v, visited):
    cnt = 1
    visited[v] = True

    for i in adjList[v]:
        if visited[i]:
            cnt = cnt + DFS(adjList, i, visited)
    return cnt


def isBridge(adjList, u, v, isDirected):
    if len(adjList[u]) == 1:
        return True
    else:
        visited = [False] * len(adjList)
        cntBeforeRestoreEdge = DFS(adjList, u, visited)

        removeEdge(adjList, u, v, isDirected)
        visited = [False] * len(adjList)
        cntAfterRestoreEdge = DFS(adjList, u, visited)

        # restore edge
        addEdge(adjList, u, v, isDirected)

        return cntBeforeRestoreEdge < cntAfterRestoreEdge


def addEdge(adjList, u, v, isDirected):
    adjList[u].append(v)
    if isDirected:
        adjList[v].append(u)


def removeEdge(adjList, u, v, isDirected):
    for neighbour in adjList[u]:
        if neighbour == v:
            adjList[u].remove(neighbour)
            break

    if not isDirected:
        for neighbour in adjList[v]:
            if neighbour == u:
                adjList[v].remove(neighbour)
                break


def FleuryAlgorithm(graph, isDirected, startNode):
    adjList = GraphHelper.getAdjList(graph)
    EulerCycle = list()

    findNextNode(adjList, startNode, EulerCycle, isDirected)
    return EulerCycle


def findNextNode(adjList, n, EulerCycle, isDirected):
    EulerCycle.append(n)

    for v in adjList[n]:
        if isBridge(adjList, n, v, isDirected):
            removeEdge(adjList, n, v, isDirected)
            findNextNode(adjList, v, EulerCycle, isDirected)
