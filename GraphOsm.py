#!/usr/bin/python3

import networkx
import OsmParser as osmp
import random
from math import sqrt
import numpy

import Visualization as vis

scaleX = 70
scaleY = 100
distScale = 1000


class GraphOsm:
    def __init__(self, osmData):
        self.nodeIndex = 0
        self.edgeIndex = 0

        self.graph = networkx.DiGraph()
        self.osm = osmp.Osm(osmData)

        self.setPostOffice()
        self.setBuildings()
        self.setPossibleStreetNode()

        self.connectBuildings()
        vis.draw(self.graph)

        self.connectStreetNodes()
        vis.draw(self.graph)

        a = 1

    def connectStreetNodes(self):
        # add crossing
        for highway1 in self.getHighwayList():
            for highway2 in self.getHighwayList():
                if highway1 is not highway2:
                    for nd in highway1.nds:
                        node = self.getNodeByOsmId(nd)
                        pos = ((node.x - float(self.osm.xmin)) * scaleX, (node.y - float(self.osm.ymin)) * scaleY)
                        if pos not in self.getListOfRealStreetNodesCoordinate():
                            self.graph.add_node(self.nodeIndex, pos=pos, osmId='',
                                                streetName=highway1.tags['name'],
                                                address='', isPostOffice=False)
                            self.realStreetNodes.append(self.graph.nodes(data=True)[self.nodeIndex])
                            self.nodeIndex += 1

        listOfRealStreetNodesCoordinate = self.getListOfRealStreetNodesCoordinate()
        for highway in self.getHighwayList():
            path = []
            listOfCurrentFakeHighwayNodeCoordinate = self.getListOfFakeNodeStreetByOsmWay(highway)

            for coord in listOfCurrentFakeHighwayNodeCoordinate:
                if coord in listOfRealStreetNodesCoordinate:
                    path.append(self.getRealGraphNodeByCoordinates(coord)[0])

            # connect
            isOneWay = True if ('oneway' in highway.tags) and (highway.tags['oneway'] == 'yes') else False
            streetName = highway.tags['name']

            for id in range(0, len(path) - 1):
                node1X, node1Y = self.graph.nodes(
                    data=True)[id]['pos'][0], self.graph.nodes(data=True)[id]['pos'][1]
                node2X, node2Y = self.graph.nodes(data=True)[id + 1]['pos'][0], \
                                 self.graph.nodes(data=True)[id + 1]['pos'][1]
                dist = self.getDistance(node1X, node1Y, node2X, node2Y)
                dist *= distScale
                dist = int(dist)

                if isOneWay:
                    self.graph.add_edge(
                        path[id], path[id + 1], weight=dist, streetName=streetName)
                else:
                    self.graph.add_edge(
                        path[id], path[id + 1], weight=dist, streetName=streetName)
                    self.graph.add_edge(
                        path[id + 1], path[id], weight=dist, streetName=streetName)

    def getListOfFakeNodeStreetByOsmWay(self, osmWay):
        list = []
        for key in self.fakeStreetNodeWithInfo:
            if self.fakeStreetNodeWithInfo[key] is osmWay:
                list.append(key)
        return list

    def getListOfRealStreetNodesCoordinate(self):
        list = []
        for node in self.realStreetNodes:
            list.append(node['pos'])
        return list

    def connectBuildings(self):
        self.realStreetNodes = []
        for building in self.getListAllBuldingsInGraph():
            streetName = building[1]['streetName']
            streetNodes = self.getStreetFakeNodeListByStreetName(streetName)
            streetNodeIdxToConnect, dist = self.getTheNearestStreetNode(building, streetNodes, streetName)

            dist *= distScale
            dist = int(dist)
            self.graph.add_edge(building[0], streetNodeIdxToConnect, weight=dist, streetName=streetName)
            self.graph.add_edge(streetNodeIdxToConnect, building[0], weight=dist, streetName=streetName)
            # vis.draw(self.graph)

    def getRealGraphNodeByCoordinates(self, coord):
        for node in self.graph.nodes(data=True):
            if node[1]['pos'] == coord:
                return node
        return None

    def getTheNearestStreetNode(self, building, listOfNodes, streetName):
        minCoord = None
        minDist = float('inf')
        for coord in listOfNodes:
            dist = self.getDistance(coord[0], coord[1], building[1]['pos'][0], building[1]['pos'][1])
            if dist < minDist:
                minDist = dist
                minCoord = coord

        node = self.getRealGraphNodeByCoordinates(minCoord)
        if node:
            idx = node[0]
        else:
            idx = self.nodeIndex
            self.graph.add_node(idx, pos=minCoord, osmId='',
                                streetName=streetName,
                                address='', isPostOffice=False)
            self.realStreetNodes.append(self.graph.nodes(data=True)[idx])
            self.nodeIndex += 1
        return idx, minDist

    def getListAllBuldingsInGraph(self):
        buildings = []
        for node in self.graph.nodes(data=True):
            if node[1]['address'] != "":
                buildings.append(node)
        return buildings

    def setPossibleStreetNode(self):
        self.fakeStreetNodeWithInfo = dict()  # (x, y) : OsmWay
        self.fakeStreetNodeList = []  # [(x1, y1), (x2, y2) ...] - list of tuples

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
        nds = highway.nds

        startOsmNode = self.getNodeByOsmId(nds[startIdx])
        endOsmNode = self.getNodeByOsmId(nds[endIdx])

        step = 0.000001
        step *= 1 if startOsmNode.x < endOsmNode.x else -1

        for idx in range(startIdx, endIdx):
            # start nd
            nd1 = self.getNodeByOsmId(nds[idx])
            xn = (nd1.x - float(self.osm.xmin)) * scaleX
            yn = (nd1.y - float(self.osm.ymin)) * scaleY

            if (xn, yn) not in self.fakeStreetNodeWithInfo:
                self.fakeStreetNodeWithInfo[(xn, yn)] = highway  # (x, y) : OsmWay
                self.fakeStreetNodeList.append((xn, yn))

            # end nd
            nd2 = self.getNodeByOsmId(nds[idx + 1])

            for x in numpy.arange(nd1.x + step, nd2.x - step, step):
                y = self.getEquationOfStreet(x - float(self.osm.xmin), nd1.x - float(self.osm.xmin),
                                             nd1.y - float(self.osm.ymin), nd2.x - float(self.osm.xmin),
                                             nd2.y - float(self.osm.ymin))

                self.fakeStreetNodeWithInfo[
                    ((x - float(self.osm.xmin)) * scaleX, y * scaleY)] = highway  # (x, y) : OsmWay
                self.fakeStreetNodeList.append(((x - float(self.osm.xmin)) * scaleX, y * scaleY))

            xn = (nd2.x - float(self.osm.xmin)) * scaleX
            yn = (nd2.y - float(self.osm.ymin)) * scaleY

            if (xn, yn) not in self.fakeStreetNodeWithInfo:
                self.fakeStreetNodeWithInfo[(xn, yn)] = highway  # (x, y) : OsmWay
                self.fakeStreetNodeList.append((xn, yn))

    def getTheNearNodeDistance(self, x, y):
        minDist = float('inf')
        for node in self.graph.nodes(data=True):
            dist = self.getDistance(x, y, node[1]['pos'][0], node[1]['pos'][1])
            if dist < minDist:
                minDist = dist
        return minDist

    def setPostOffice(self):
        isPostOffice = False
        for building in self.getBuildingList():
            if 'amenity' in building.tags and building.tags['amenity'] == 'post_office':
                streetName = self.getStreetName(building)
                self.addNode(
                    building.nds[0], building.tags['addr:housenumber'], streetName, True)
                isPostOffice = True
                break

        # if post office doesnt exist in map, set random building as a post office
        if not isPostOffice:
            building = random.choice(self.getBuildingList())
            streetName = self.getStreetName(building)
            self.addNode(
                building.nds[0], building.tags['addr:housenumber'], streetName, True)

    def setBuildings(self):
        for building in self.getBuildingList():
            if building.nds[0] != self.graph.nodes[0]['osmId']:
                streetName = self.getStreetName(building)
                self.addNode(
                    building.nds[0], building.tags['addr:housenumber'], streetName, False)

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
                    elem.tags['name'] in streetNames and self.isCorrectStreet(elem):
                highways.append(elem)

        return highways

    def isCorrectStreet(self, street):
        counter = 0
        for nd in street.nds:
            if self.isCorrectNode(nd): counter += 1
            if counter > 2: return True
        return False

    def getEquationOfStreet(self, x, x1, y1, x2, y2):
        return ((y1 - y2) / (x1 - x2)) * x + (y1 - (y1 - y2) / (x1 - x2) * x1)

    def getDistance(self, node1X, node1Y, node2X, node2Y):
        return sqrt((node2X - node1X) ** 2 + (node2Y - node1Y) ** 2)

    def getBuildingList(self):
        buildings = []
        for elem in self.osm.osmWays:
            if 'building' in elem.tags \
                    and 'addr:street' in elem.tags \
                    and 'addr:housenumber' in elem.tags \
                    and self.isCorrectNode(elem.nds[0]) \
                    and self.isExistingStreet(elem.tags['addr:street']):
                buildings.append(elem)
        return buildings

    def isExistingStreet(self, streetName):
        for way in self.osm.osmWays:
            if 'highway' in way.tags \
                    and 'name' in way.tags \
                    and self.isCorrectStreet(way) \
                    and way.tags['name'] == streetName:
                return True
        return False

    def addNode(self, osmIndex, houseNumber, streetName, isPostOffice=False):
        building = self.getNodeByOsmId(osmIndex)
        x, y = (building.x - float(self.osm.xmin)) * \
               scaleX, (building.y - float(self.osm.ymin)) * scaleY
        self.graph.add_node(self.nodeIndex, pos=(x, y), osmId=building.id, streetName=streetName,
                            address=streetName + "\n" + houseNumber, isPostOffice=isPostOffice)
        self.nodeIndex += 1

    def getNodeByOsmId(self, indexOsm):
        for node in self.osm.osmNodes:
            if node.id == indexOsm:
                return node
        return None

    def getRealGraphNodeByOsmId(self, indexOsm):
        for node in self.graph.nodes(data=True):
            if node[1]['osmId'] == indexOsm:
                return node
        return None

    def getWayByOsmId(self, indexOsm):
        for way in self.osm.osmWays:
            if way.id == indexOsm:
                return way
        return None

    def getStreetFakeNodeListByStreetName(self, streetName):
        nodes = []
        for key in self.fakeStreetNodeWithInfo:
            if 'name' in self.fakeStreetNodeWithInfo[key].tags and \
                    self.fakeStreetNodeWithInfo[key].tags['name'] == streetName:
                nodes.append(key)

        return nodes

    def getStreetRealNodeListByStreetName(self, streetName):
        nodes = []
        for node in self.realStreetNodes:
            if node['osmId'] == '' and node['address'] == '' and node['streetName'] == streetName:
                nodes.append(node)

        return nodes

