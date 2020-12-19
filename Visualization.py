#!/usr/bin/python3
import random

import matplotlib.pyplot as plt
import networkx as nx


def draw(graph, eulerCycle=None, printFakeEdges=False):
    if eulerCycle is None:
        eulerCycle = []

    # nodes
    address, position = getNodeData(graph)
    drawNodesAndLabels(address, graph, position)

    # edges
    # fake edges - to make eulerian graph
    fakeEdges = drawFakeEdges(graph, position, printFakeEdges)

    # regular  edges
    drawRegularEdges(address, fakeEdges, graph, position, eulerCycle)

    # current edges form Euler cycle
    drawHighlightedEulerCycleEdges(graph, position, eulerCycle)

    plt.show()


def drawNodesAndLabels(address, graph, position):
    if address:
        colors, size = setDataForRealGraph(graph)
        nx.draw_networkx_nodes(graph, position, node_size=size, node_color=colors)
        nx.draw_networkx_labels(graph, position, labels=address, font_size=4)
    else:
        colors, size = setDataForRandomGraph(graph)
        nx.draw_networkx_nodes(graph, position, node_size=size, node_color=colors)
        nx.draw_networkx_labels(graph, position, font_size=10)


def drawRegularEdges(isRealGraph, fakeEdges, graph, position, eulerCycle):
    if isRealGraph:
        nx.draw_networkx_edges(graph, position,
                               arrows=True, width=0.2, arrowsize=3, arrowstyle='->',
                               edgelist=set(graph.edges) - set(fakeEdges))
    else:
        nx.draw_networkx_edges(graph, position,
                               arrows=True, width=0.5, arrowsize=10,
                               edgelist=set(graph.edges) - set(fakeEdges) - set(eulerCycle))


def drawFakeEdges(graph, position, printFakeEdges):
    fakeEdges = []

    for edge in graph.edges(data=True):
        if edge[2]['isFakeRoute']:
            fakeEdges.append((edge[0], edge[1], 1))

    if printFakeEdges:
        nx.draw_networkx_edges(graph, position,
                               arrows=True, width=1, arrowsize=5,
                               edgelist=fakeEdges, edge_color='green',
                               connectionstyle="arc3,rad=rrr".replace('rrr',
                                                                      str(0.3 * random.uniform(-1.0, 1.0))))

    return fakeEdges


def drawHighlightedEulerCycleEdges(graph, position, eulerCycle):
    if eulerCycle:
        nx.draw_networkx_edges(graph, position, edge_color='red',
                               arrows=True, width=0.7, arrowsize=5,
                               edgelist=set(eulerCycle[:-1]))

        nx.draw_networkx_edges(graph, position, edge_color='red',
                               arrows=True, width=2.5, arrowsize=10,
                               edgelist=set(eulerCycle[-1:]))


def setDataForRandomGraph(graph):
    for idx in graph.nodes:
        graph.nodes[idx]['color'] = 'red' if graph.nodes[idx]['isPostOffice'] else 'grey'
        graph.nodes[idx]['size'] = 100

    colors = [node[1]['color'] for node in graph.nodes(data=True)]
    size = [node[1]['size'] for node in graph.nodes(data=True)]

    return colors, size


def setDataForRealGraph(graph):
    for idx in graph.nodes:
        graph.nodes[idx]['color'] = 'green' if graph.nodes[idx]['address'] == "" else 'grey'
        graph.nodes[idx]['size'] = 0.1 if graph.nodes[idx]['address'] == "" else 100
        if graph.nodes[idx]['isPostOffice']:
            graph.nodes[idx]['color'] = 'red'

    colors = [node[1]['color'] for node in graph.nodes(data=True)]
    size = [node[1]['size'] for node in graph.nodes(data=True)]

    return colors, size


def getNodeData(graph):
    position = nx.get_node_attributes(graph, 'pos')
    address = nx.get_node_attributes(graph, 'address')

    return address, position
