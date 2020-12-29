import GraphHelper


def DFS(adjList, v, visited):
    cnt = 1
    visited[v] = True

    for i in adjList[v]:
        if not visited[i]:
            cnt = cnt + DFS(adjList, i, visited)
    return cnt


def isBridge(adjList, u, v):
    if len(adjList[u]) == 1:
        return True
    else:
        visited = [False] * len(adjList)
        cntBeforeRestoreEdge = DFS(adjList, u, visited)

        removeEdge(adjList, u, v)
        visited = [False] * len(adjList)
        cntAfterRestoreEdge = DFS(adjList, u, visited)

        # restore edge
        addEdge(adjList, u, v)

        return False if cntBeforeRestoreEdge > cntAfterRestoreEdge else True


def addEdge(adjList, u, v):
    adjList[u].append(v)
    adjList[v].append(u)


def removeEdge(adjList, u, v):
    for neighbour in adjList[u]:
        if neighbour == v:
            adjList[u].remove(neighbour)
            break
    for neighbour in adjList[v]:
        if neighbour == u:
            adjList[v].remove(neighbour)
            break


def FleuryAlgorithm(graph, startNode):
    adjList = GraphHelper.getAdjList(graph)
    EulerCycle = list()

    findNextNode(adjList, startNode, EulerCycle)
    return EulerCycle


def findNextNode(adjList, n, EulerCycle):
    EulerCycle.append(n)
    for v in adjList[n]:
        if isBridge(adjList, n, v):
            removeEdge(adjList, n, v)
            findNextNode(adjList, v, EulerCycle)
