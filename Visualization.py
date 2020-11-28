#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import random


def draw(graph, route=[]):
    weight = nx.get_edge_attributes(graph, 'weight')
    address = nx.get_node_attributes(graph, 'address')
    streetName = nx.get_edge_attributes(graph, 'streetName')

    position = nx.get_node_attributes(graph, 'pos')
    if not position:
        position = nx.spring_layout(graph, k=2, iterations=20, seed=2)
        
    # Houses nodes - grey
    # Post office - red 
    # Crossings - yellow
    if address:
        for idx in graph.nodes:
            graph.nodes[idx]['color'] = 'green' if graph.nodes[idx]['streetName'] == "" else 'grey'
            graph.nodes[idx]['size'] = 50 if graph.nodes[idx]['streetName'] == "" else 200
            if graph.nodes[idx]['isPostOffice'] == True:
                graph.nodes[idx]['color'] = 'red'


        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        size = [node[1]['size'] for node in graph.nodes(data=True)]

    else:
        for idx in graph.nodes:
            graph.nodes[idx]['color'] = 'red' if graph.nodes[idx]['isPostOffice'] == True else 'grey'
            graph.nodes[idx]['size'] = 200

        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        size = [node[1]['size'] for node in graph.nodes(data=True)]

    nx.draw_networkx_nodes(graph, position, node_size=size, node_color=colors)

    # highlight
    nx.draw_networkx_edges(graph, position, arrows=True, width=2.5, edgelist=route, edge_color='red')

    # non highlight
    nx.draw_networkx_edges(graph, position, arrows=True, edgelist=set(graph.edges) - set(route))
    
    
    # labels
    if address:
        nx.draw_networkx_labels(graph, position, labels=address, font_size=6)
    else:
        nx.draw_networkx_labels(graph, position, font_size=10)

    if streetName:
    	nx.draw_networkx_edge_labels(graph, position, edge_labels=streetName, font_size=6)
    elif weight:
    	nx.draw_networkx_edge_labels(graph, position, edge_labels=weight, font_size=6)


    plt.show()

