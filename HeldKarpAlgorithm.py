#!/usr/bin/python3

import networkx as nx
import itertools

##################################
#
# Pseudocode (Wikipedia)
#
#
# function algorithm TSP (G, n) is
#     for k := 2 to n do
#         C({k}, k) := d1,k
#     end for
#
#     for s := 2 to n−1 do
#         for all S ⊆ {2, . . . , n}, |S| = s do
#             for all k ∈ S do
#                 C(S, k) := minm≠k,m∈S [C(S\{k}, m) + dm,k]
#             end for
#         end for
#     end for
#
#     opt := mink≠1 [C({2, 3, . . . , n}, k) + dk, 1]
#     return (opt)
# end function
#


def HeldKarpAlgo(graph):
    distanceMatrix = nx.floyd_warshall_numpy(graph)
    n = len(distanceMatrix)

    # costs - dictionary of pairs of tuple
    # costs = { (subsets of node represented as binary value, subset ended node)
    #       : (subset's cost, second-to-last node/prevNode of subset ended node)
    #
    # example
    # distanceMatrix = [[ 0,     13,     9,      5]
    #                   [13,      0,     4,      8]
    #                   [ 9,      4,     0,      4]
    #                   [ 5,      8,     4,      0]]
    # costs =   {
    #           (2, 1)  : (13, 0)   ->     2  = 0010 , from 0 -> 1 cost 13
    #           (4, 2)  : (9, 0)    ->     4  = 0100 , from 0 -> 2 cost 9
    #           (8, 3)  : (5, 0)    ->     8  = 1000 , from 0 -> 3 cost 5
    #           (6, 1)  : (13, 2)   ->     6  = 0110 , from 2 -> 1 cost 13
    #           (6, 2)  : (17, 1)   ->     6  = 0110 , from 1 -> 2 cost 17
    #           (10, 1) : (13, 3)   ->    10  = 1010 , from 3 -> 1 cost 13
    #           (10, 3) : (21, 1)   ->    10  = 1010 , from 1 -> 3 cost 21
    #           (12, 2) : (9, 3)    ->    12  = 1100 , from 3 -> 2 cost 9
    #           (12, 3) : (13, 2)   ->    12  = 1100 , from 2 -> 3 cost 13
    #           (14, 1) : (13, 2)   ->    14  = 1110 , from 3 -> 2 -> 1 cost 13
    #           (14, 2) : (17, 1)   ->    14  = 1110 , from 3 -> 1 -> 2 cost 17
    #           (14, 3) : (21, 1)   ->    14  = 1110 , from 2 -> 1 -> 3 cost 21
    #       }

    costs = {}

    # Initial state from 0 to other nodes, from distance matrix
    # 1 << k - subsets of noder reprezent as bits
    for k in range(1, n):
        costs[(1 << k, k)] = (distanceMatrix[0][k], 0)

    # Iterate by all nodes
    for s in range(2, n):
        for subset in itertools.combinations(range(1, n), s):

            # Set subsets of node represented as binary value
            currentSubsetBits = 0
            for node in subset:
                currentSubsetBits |= 1 << node

            # Find the lowest cost to get to this subset
            for bit in subset:
                prevNode = currentSubsetBits & ~(1 << bit)

                tempCosts = []
                for node in subset:
                    if node == 0 or node == bit:
                        continue
                    tempCosts.append((costs[(prevNode, node)][0] + distanceMatrix[node][bit], node))
                costs[(currentSubsetBits, bit)] = min(tempCosts)


    # Calculate optimal cost
    pathWithoutStartNode = (2 ** n - 1) - 1
    tempCosts = []
    for node in range(1, n):
        tempCosts.append((costs[(pathWithoutStartNode, node)][0] + distanceMatrix[node][0], node))
    optimalPathLen, parent = min(tempCosts)

    # Find full path
    fullPath = []
    # TO DO

    print(optimalPathLen)
    print(list(reversed(fullPath)))

    return optimalPathLen, list(reversed(fullPath))
