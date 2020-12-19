#!/usr/bin/python3
import random

import matplotlib.pyplot as plt
import networkx as nx


def draw(graph, route=None, printFakeEdges=False):
    if route is None:
        route = []
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

    # additional edges - to make eulerian graph
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

    # normal edges
    if address:
        nx.draw_networkx_edges(graph, position,
                               arrows=True, width=0.2, arrowsize=3, arrowstyle='->',
                               edgelist=set(graph.edges) - set(fakeEdges))
    else:
        nx.draw_networkx_edges(graph, position,
                               arrows=True, width=0.5, arrowsize=10,
                               edgelist=set(graph.edges) - set(fakeEdges) - set(route))
    if route:
        nx.draw_networkx_edges(graph, position, edge_color='red',
                               arrows=True, width=0.7, arrowsize=5,
                               edgelist=set(route[:-1]))

        nx.draw_networkx_edges(graph, position, edge_color='red',
                               arrows=True, width=2.5, arrowsize=10,
                               edgelist=set(route[-1:]))
    plt.show()
    # write_dot(graph, 'my_graph.dot')
