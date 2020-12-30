#!/usr/bin/python3

import networkx
import OsmParser as osmp
import random
import numpy
import GraphHelper as gh
from math import radians, cos, sin, asin, sqrt

distScale = 1000
stepStreetNode = 0.00001


def getDistance(x1, y1, x2, y2):
    x1, y1, x2, y2 = map(radians, [x1, y1, x2, y2])
    dx = x2 - x1
    dy = y2 - y1
    a = sin(dy / 2) ** 2 + cos(y1) * cos(y2) * sin(dx / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    r *= 1000
    return c * r


class OsmGraph:
    def __init__(self, osmData):
        self.street = []
        self.nodeIndex = 0
        self.edgeIndex = 0

        self.graph = networkx.MultiDiGraph()
        self.osm = osmp.Osm(osmData)

        self.setPostOffice()
        self.setBuildings()
        self.setStreet()

        self.connectBuildings()

        self.removeUnusedStreetNodes()

        self.makeStrongConnected()

        self.relabelNodes()
        # if not gh.isEulerianGraph(self.graph):
        #     try:
        gh.makeEulerianDiGraph(self.graph)
        #     except:
        #         print("Stworzenie grafu jest niemożliwe")
        #         exit(-1)

    def makeStrongConnected(self):
        gen = networkx.strongly_connected_components(self.graph)
        maxComponent = None
        maxLen = -1
        for s in gen:
            if len(s) > maxLen:
                maxLen = len(s)
                maxComponent = s
        nodesToRemove = set(self.graph.nodes()) - set(maxComponent)
        for node in nodesToRemove:
            self.graph.remove_node(node)

    def relabelNodes(self):
        idx = 0
        mapping = dict()
        for node in self.graph.nodes():
            mapping[node] = idx
            idx += 1

        self.graph = networkx.relabel_nodes(self.graph, mapping, False)
        a = 1

    def getRange(self):  # ranges = [xmin, xmax, ymin, ymax]
        return [float(self.osm.xmin), float(self.osm.xmax), float(self.osm.ymin), float(self.osm.ymax)]

    def removeUnusedStreetNodes(self):
        nodesToRemove = []
        for node in self.graph.nodes(data=True):
            if node[1]['osmId'] == "" and not self.isImportantStreetNode(node):
                nodesToRemove.append(node)
        self.reduceStreetConnection(nodesToRemove)

    def reduceStreetConnection(self, nodesToRemove):
        for node in nodesToRemove:
            pred = list(self.graph.predecessors(node[0]))[0]
            succ = list(self.graph.successors(node[0]))[0]
            if succ is pred:
                succ = list(self.graph.successors(node[0]))[1]
                dist = self.graph[pred][node[0]][0]['weight'] + self.graph[node[0]][succ][0]['weight']
                streetName = node[1]['streetName']
                self.graph.add_edge(pred, succ, weight=dist, streetName=streetName, isFakeRoute=False)
                self.graph.add_edge(succ, pred, weight=dist, streetName=streetName, isFakeRoute=False)
                self.graph.remove_node(node[0])
            else:
                dist = self.graph[pred][node[0]][0]['weight'] + self.graph[node[0]][succ][0]['weight']
                streetName = node[1]['streetName']
                self.graph.add_edge(pred, succ, weight=dist, streetName=streetName, isFakeRoute=False)
                self.graph.remove_node(node[0])

    def isImportantStreetNode(self, node):
        isImportant = False
        for pred in self.graph.pred[node[0]]:
            if self.graph.nodes[pred]['osmId'] != '':
                isImportant = True
                break
        for succ in self.graph.succ[node[0]]:
            if self.graph.nodes[succ]['osmId'] != '':
                isImportant = True
                break
        return isImportant

    def connectBuildings(self):
        for building in self.getListAllBuldingsInGraph():
            streetName = building[1]['streetName']
            streetNodes = self.getStreetNodeListByStreetName(streetName)
            streetNodeIdxToConnect, dist = self.getTheNearestStreetNode(building, streetNodes)

            dist *= distScale
            dist = int(dist)
            self.graph.add_edge(building[0], streetNodeIdxToConnect, weight=dist, streetName=streetName,
                                isFakeRoute=False)
            self.graph.add_edge(streetNodeIdxToConnect, building[0], weight=dist, streetName=streetName,
                                isFakeRoute=False)

    def getTheNearestStreetNode(self, building, listOfNodes):
        idx = -1
        dist = -1
        minDist = float('inf')
        for node in listOfNodes:
            dist = getDistance(node[1]['pos'][0], node[1]['pos'][1], building[1]['pos'][0], building[1]['pos'][1])
            if dist < minDist:
                minDist = dist
                idx = node[0]
        return idx, dist

    def getListAllBuldingsInGraph(self):
        buildings = []
        for node in self.graph.nodes(data=True):
            if node[1]['address'] != "":
                buildings.append(node)
        return buildings

    def setStreet(self):
        for highway in self.getHighwayList():
            startIdx, endIdx = -1, -1

            for idx in range(0, len(highway.nds) - 1):
                if self.isCorrectNode(highway.nds[idx]):
                    startIdx = idx
                    break

            for idx in range(len(highway.nds) - 1, 0, -1):
                if self.isCorrectNode(highway.nds[idx]):
                    endIdx = idx
                    break

            self.splitStreet(startIdx, endIdx, highway)

    def splitStreet(self, startIdx, endIdx, highway):
        # split
        nds = highway.nds
        streetName = highway.tags['name']
        isOneWay = True if ('oneway' in highway.tags) and (highway.tags['oneway'] == 'yes') else False

        path = []
        startOsmNode = self.getNodeByOsmId(nds[startIdx])
        endOsmNode = self.getNodeByOsmId(nds[endIdx])

        step = stepStreetNode
        step *= 1 if startOsmNode.x < endOsmNode.x else -1

        for idx in range(startIdx, endIdx):
            # start nd
            nd1 = self.getNodeByOsmId(nds[idx])
            if nds[idx] not in self.getListOfOsmIsOfCurrentGraphNode():
                self.graph.add_node(self.nodeIndex, pos=(nd1.x, nd1.y),
                                    osmId=nd1.id, streetName=streetName, address="", isPostOffice=False)
                path.append(self.nodeIndex)
                self.nodeIndex += 1
            elif nds[idx] in self.getListOfOsmIsOfCurrentGraphNode() and \
                    self.getRealGraphNodeByOsmId(nds[idx]) not in path:
                path.append(self.getRealGraphNodeByOsmId(nds[idx])[0])

            # end nd
            nd2 = self.getNodeByOsmId(nds[idx + 1])

            for x in numpy.arange(nd1.x + step, nd2.x - step, step):
                y = self.getEquationOfStreet(x, nd1.x,
                                             nd1.y, nd2.x,
                                             nd2.y)
                self.graph.add_node(self.nodeIndex, pos=(x, y), osmId="",
                                    streetName=streetName,
                                    address="", isPostOffice=False)
                path.append(self.nodeIndex)
                self.nodeIndex += 1

            if nds[idx + 1] not in self.getListOfOsmIsOfCurrentGraphNode():
                self.graph.add_node(self.nodeIndex, pos=(nd2.x, nd2.y),
                                    osmId=nd2.id, streetName=streetName, address="", isPostOffice=False)
                path.append(self.nodeIndex)
                self.nodeIndex += 1
            elif nds[idx + 1] in self.getListOfOsmIsOfCurrentGraphNode() and \
                    self.getRealGraphNodeByOsmId(nds[idx]) not in path:
                path.append(self.getRealGraphNodeByOsmId(nds[idx + 1])[0])

            for id in range(0, len(path) - 1):
                node1X, node1Y = self.graph.nodes(
                    data=True)[id]['pos'][0], self.graph.nodes(data=True)[id]['pos'][1]
                node2X, node2Y = self.graph.nodes(data=True)[id + 1]['pos'][0], \
                                 self.graph.nodes(data=True)[id + 1]['pos'][1]
                dist = getDistance(node1X, node1Y, node2X, node2Y)
                dist *= 1000
                dist = int(dist)
                if isOneWay:
                    self.graph.add_edge(
                        path[id], path[id + 1], weight=dist, streetName=streetName, isFakeRoute=False)
                else:
                    self.graph.add_edge(
                        path[id], path[id + 1], weight=dist, streetName=streetName, isFakeRoute=False)
                    self.graph.add_edge(
                        path[id + 1], path[id], weight=dist, streetName=streetName, isFakeRoute=False)

    def setPostOffice(self):
        isPostOffice = False
        for building in self.getBuildingList():
            if 'amenity' in building[0].tags and building[0].tags['amenity'] == 'post_office':
                streetName = self.getStreetName(building[0])
                if building[1]:
                    x, y = self.getBuildingPosition(building[0].nds)
                    self.addNode(
                        building[0].nds[0], building[0].tags['addr:housenumber'], streetName, x, y, True)
                else:
                    self.addNode(
                        building[0].id, building[0].tags['addr:housenumber'], streetName, building[0].x, building[0].y,
                        True)
                isPostOffice = True
                break

        # if post office doesnt exist in map, set random building as a post office
        if not isPostOffice:
            building = random.choice(self.getBuildingList())
            streetName = self.getStreetName(building[0])
            if building[1]:
                x, y = self.getBuildingPosition(building[0].nds)
                self.addNode(
                    building[0].nds[0], building[0].tags['addr:housenumber'], streetName, x, y, True)
            else:
                self.addNode(
                    building[0].id, building[0].tags['addr:housenumber'], streetName, building[0].x, building[0].y,
                    True)

    def setBuildings(self):
        for building in self.getBuildingList():
            if building[1] == True and building[0].nds[0] != self.graph.nodes[0]['osmId']:
                streetName = self.getStreetName(building[0])
                x, y = self.getBuildingPosition(building[0].nds)
                self.addNode(
                    building[0].nds[0], building[0].tags['addr:housenumber'], streetName, x, y, False)
            elif building[1] == False and building[0].id != self.graph.nodes[0]['osmId']:
                streetName = self.getStreetName(building[0])
                self.addNode(
                    building[0].id, building[0].tags['addr:housenumber'], streetName, building[0].x, building[0].y,
                    False)

    def getBuildingPosition(self, nds):
        x, y = 0, 0
        cnt = 0
        for nd in nds:
            node = self.getNodeByOsmId(nd)
            x += node.x
            y += node.y
            cnt += 1
        return x / cnt, y / cnt

    def getStreetName(self, building):
        if 'addr:street' not in building.tags:
            streetName = ''
        else:
            streetName = building.tags['addr:street']
        return streetName

    def isCorrectNode(self, nodeOsmId):
        nodeOsm = self.getNodeByOsmId(nodeOsmId)
        if nodeOsm.x >= float(self.osm.xmax) or nodeOsm.x <= float(self.osm.xmin) or \
                nodeOsm.y <= float(self.osm.ymin) or nodeOsm.y >= float(self.osm.ymax):
            return False
        else:
            return True

    def getListOfOsmIsOfCurrentGraphNode(self):
        list = []
        for node in self.graph.nodes(data=True):
            list.append(node[1]['osmId'])

        return list

    def getHighwayList(self):
        # get all streets' names form current graph's nodes
        streetNames = set()
        for building in self.graph.nodes(data=True):
            streetNames.add(building[1]['streetName'])

        highways = []
        for elem in self.osm.osmWays:
            if 'highway' in elem.tags and 'name' in elem.tags and \
                    elem.tags['name'] in streetNames:
                highways.append(elem)
            elif 'highway' in elem.tags and (
                    elem.tags['highway'] == 'service' or elem.tags['highway'] == 'residential'):
                self.addNoNameHighway(elem, highways, streetNames)

        return highways

    def addNoNameHighway(self, way, highways, streetNames):
        for nd in way.nds:
            for elem in self.osm.osmWays:
                if elem is not way and \
                        nd in elem.nds and \
                        'name' in elem.tags and \
                        elem.tags['name'] in streetNames:  # and self.isCorrectStreet(elem):
                    way.tags['name'] = elem.tags['name']
                    highways.append(way)
                    return

    def isCorrectStreet(self, street):
        counter = 0
        for nd in street.nds:
            if self.isCorrectNode(nd): counter += 1
            if counter > 2: return True
        return False

    def getEquationOfStreet(self, x, x1, y1, x2, y2):
        return ((y1 - y2) / (x1 - x2)) * x + (y1 - (y1 - y2) / (x1 - x2) * x1)

    def getBuildingList(self):
        buildings = []
        for elem in self.osm.osmWays:
            if 'building' in elem.tags \
                    and 'addr:street' in elem.tags \
                    and 'addr:housenumber' in elem.tags \
                    and self.isCorrectNode(elem.nds[0]) \
                    and self.isExistingStreet(elem.tags['addr:street']):
                buildings.append((elem, True))

        for elem in self.osm.osmNodes:
            if 'addr:street' in elem.tags \
                    and 'addr:housenumber' in elem.tags \
                    and self.isCorrectNode(elem.id) \
                    and self.isExistingStreet(elem.tags['addr:street']):
                buildings.append((elem, False))
        return buildings

    def isExistingStreet(self, streetName):
        for way in self.osm.osmWays:
            if 'highway' in way.tags \
                    and 'name' in way.tags \
                    and way.tags['name'] == streetName:
                return True
        return False

    def addNode(self, osmIndex, houseNumber, streetName, x, y, isPostOffice=False):
        building = self.getNodeByOsmId(osmIndex)
        self.graph.add_node(self.nodeIndex, pos=(x, y), osmId=building.id, streetName=streetName,
                            address=streetName + "\n" + houseNumber, isPostOffice=isPostOffice)
        self.nodeIndex += 1

    def getNodeByOsmId(self, indexOsm):
        for node in self.osm.osmNodes:
            if node.id == indexOsm:
                return node

    def getRealGraphNodeByOsmId(self, indexOsm):
        for node in self.graph.nodes(data=True):
            if node[1]['osmId'] == indexOsm:
                return node
        return None

    def getStreetNodeListByStreetName(self, streetName):
        nodes = []
        for node in self.graph.nodes(data=True):
            if node[1]['address'] == "" and node[1]['streetName'] == streetName:
                nodes.append(node)

        return nodes
