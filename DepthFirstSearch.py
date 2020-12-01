#!/usr/bin/python3

import networkx
import enum

step = 0


class Color(enum.Enum):
    white = 1
    grey = 2
    black = 3

# Brute force algorithm


def DepthFirstSearch(graph):
    global step

    states = []
    dictionary = dict()
    dictionary['color'] = Color.white
    dictionary['parent'] = None
    dictionary['start'] = -1
    dictionary['end'] = -1

    for node in graph.nodes():
        states.append(dictionary.copy())

    step = 0
    for node in graph.nodes():
        if states[node]['color'] is Color.white:
            DFSVisit(graph, node, states)

    # findPath(graph, states)
    return states


def DFSVisit(graph, node, states):
    global step

    step += 1
    states[node]['start'] = step
    states[node]['color'] = Color.grey

    for neighbour in graph.neighbors(node):
        if states[neighbour]['color'] is Color.white:
            states[neighbour]['parent'] = node
            DFSVisit(graph, neighbour, states)

    states[node]['color'] = Color.black
    step += 1
    states[node]['end'] = step


def getNodeByStartStep(graph, states, step):
    for node in graph.nodes():
        if states[node]['start'] is step:
            return node


def getNodeByEndStep(graph, states, step):
    for node in graph.nodes():
        if states[node]['end'] is step:
            return node


def findPath(graph):
    fullPath = []
    
    print(fullPath)

