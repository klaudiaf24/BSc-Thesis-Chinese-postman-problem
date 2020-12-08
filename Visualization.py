#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx


def draw(graph, route=[], printFakeNodes = False):
    weight = nx.get_edge_attributes(graph, 'weight')
    address = nx.get_node_attributes(graph, 'address')
    streetName = nx.get_edge_attributes(graph, 'streetName')

    position = nx.get_node_attributes(graph, 'pos')
    if not position:
        position = nx.spring_layout(graph, k=0.4, iterations=20, seed=2)

    # Color nodes -> Post office in red -> crossing yellow
    if address:
        for idx in graph.nodes:
            graph.nodes[idx]['color'] = 'green' if graph.nodes[idx]['address'] == "" else 'grey'
            graph.nodes[idx]['size'] = 50 if graph.nodes[idx]['address'] == "" else 100
            if graph.nodes[idx]['isPostOffice']:
                graph.nodes[idx]['color'] = 'red'

        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        size = [node[1]['size'] for node in graph.nodes(data=True)]

    else:
        for idx in graph.nodes:
            graph.nodes[idx]['color'] = 'red' if graph.nodes[idx]['isPostOffice']\
                                                else 'green' if graph.nodes[idx]['isFakeNode']\
                                                    else'grey'
            graph.nodes[idx]['size'] = 40 if graph.nodes[idx]['isFakeNode'] else 200

        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        size = [node[1]['size'] for node in graph.nodes(data=True)]

    nx.draw_networkx_nodes(graph, position, node_size=size, node_color=colors)

    if address:
        nx.draw_networkx_labels(graph, position, labels=address, font_size=6)
    else:
        nx.draw_networkx_labels(graph, position, font_size=10)

    if streetName:
        nx.draw_networkx_edge_labels(
            graph, position, edge_labels=streetName, font_size=6)
    elif weight:
        nx.draw_networkx_edge_labels(
            graph, position, edge_labels=weight, font_size=6)

    # highlight
    nx.draw_networkx_edges(graph, position, arrows=True,
                           width=2.5, min_source_margin=0, edgelist=route, edge_color='red')

    # non highlight
    nx.draw_networkx_edges(graph, position, arrows=True, min_source_margin=0,
                           edgelist=set(graph.edges) - set(route))

    plt.show()
