import networkx as nx


def DFSCount(adjList, v, visited):
    count = 1
    visited[v] = True
    for i in adjList[v]:
        if visited[i] == False:
            count = count + DFSCount(adjList, i, visited)
    return count


def isValidNextEdge(adjList, u, v):
    if len(adjList[u]) == 1:
        return True
    else:
        visited = [False] * len(adjList)
        count1 = DFSCount(adjList, u, visited)

        isBothDirection = removeEdge(adjList, u, v)
        visited = [False] * len(adjList)
        count2 = DFSCount(adjList, u, visited)

        addEdge(adjList, u, v, isBothDirection)

        return False if count1 > count2 else True


def getAdjList(graph):
    adjList = dict()
    for node in graph.nodes():
        neighbours = []
        for neighbour in graph.adj[node]:
            for _ in graph.adj[node][neighbour]:
                neighbours.append(neighbour)
        adjList[node] = neighbours
    return adjList


def removeEdge(adjList, u, v):
    cnt = 0
    for neighbour in adjList[u]:
        if neighbour == v:
            adjList[u].remove(neighbour)
            cnt += 1
            break
    for neighbour in adjList[v]:
        if neighbour == u:
            adjList[v].remove(neighbour)
            cnt += 1
            break
    return cnt == 2


def addEdge(adjList, u, v, isBothDirection):
    adjList[u].append(v)
    if isBothDirection:
        adjList[v].append(u)


def FleuryAlgorithm(graph, n):
    adjList = getAdjList(graph)
    path = []
    FleuryAlgorithmCD(adjList, n, path)
    return path

def FleuryAlgorithmCD(adjList, n, path):
    path.append(n)
    for v in adjList[n]:
        if isValidNextEdge(adjList, n, v):
            # print("%d-%d " % (n, v)),
            removeEdge(adjList, n, v)
            FleuryAlgorithmCD(adjList, v,path)
