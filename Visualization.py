#!/usr/bin/python3
import random

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot

def draw(graph, route=[], printFakeEdges=False):
    weight = []

    for (u, v, attrib_dict) in list(graph.edges.data()):
        weight.append(attrib_dict['weight'])

    position = nx.get_node_attributes(graph, 'pos')
    address = nx.get_node_attributes(graph, 'address')

    if address:
        for idx in graph.nodes:
            graph.nodes[idx]['color'] = 'green' if graph.nodes[idx]['address'] == "" else 'grey'
            graph.nodes[idx]['size'] = 0.1 if graph.nodes[idx]['address'] == "" else 100
            if graph.nodes[idx]['isPostOffice']:
                graph.nodes[idx]['color'] = 'red'

        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        size = [node[1]['size'] for node in graph.nodes(data=True)]
    else:
        for idx in graph.nodes:
            graph.nodes[idx]['color'] = 'red' if graph.nodes[idx]['isPostOffice'] else 'grey'
            graph.nodes[idx]['size'] = 100

        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        size = [node[1]['size'] for node in graph.nodes(data=True)]


    nx.draw_networkx_nodes(graph, position, node_size=size, node_color=colors)
    if address:
        nx.draw_networkx_labels(graph, position, labels=address, font_size=4)
    else:
        nx.draw_networkx_labels(graph, position, font_size=10)


    # additional edges - to make graph eulerian
    fakeEdges = []
    for edge in graph.edges(data=True):
        if edge[2]['isFakeRoute'] == True:
            fakeEdges.append((edge[0], edge[1], 1))

    if printFakeEdges:
        nx.draw_networkx_edges(graph, position,
                               arrows=True, width=3, arrowsize=5,
                               edgelist=fakeEdges, edge_color='green',
                               connectionstyle="arc3,rad=rrr".replace('rrr',
                                                                      str(0.3 * random.uniform(-1.0, 1.0))))

    # normal edges
    if address:
        nx.draw_networkx_edges(graph, position,
                           arrows=True, width=0.2, arrowsize=3, arrowstyle='->',
                           edgelist=set(graph.edges) - set(fakeEdges))
    else:
        nx.draw_networkx_edges(graph, position,
                           arrows=True, width=0.5, arrowsize=5,
                           edgelist=set(graph.edges) - set(fakeEdges))

    plt.show()
    # write_dot(graph, 'my_graph.dot')
