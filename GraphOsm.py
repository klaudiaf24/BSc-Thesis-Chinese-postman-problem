#!/usr/bin/python3

import networkx
import OsmParser as osmp
import random
from math import sqrt
import numpy

scale = 200


class GraphOsm:
    def __init__(self, osmData):
        self.nodeIndex = 0
        self.edgeIndex = 0

        self.graph = networkx.DiGraph()
        self.osm = osmp.Osm(osmData)

        self.setPostOffice()
        self.setNodes()

        self.appendCrossing()

        self.setEdges()

    def setPostOffice(self):
        isPostOffice = False
        for building in self.getBuildingList():
            if 'amenity' in building.tags and building.tags['amenity'] == 'post_office':
                streetName = self.getStreetName(building)
                self.addNode(
                    building.nds[0], building.tags['addr:housenumber'], streetName, True)
                isPostOffice = True

        # if post office doesnt exist in map, set random building as a post office
        if not isPostOffice:
            building = random.choice(self.getBuildingList())
            streetName = self.getStreetName(building)
            self.addNode(
                building.nds[0], building.tags['addr:housenumber'], streetName, True)

    def setNodes(self):
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

    def setEdges(self):
        highways = self.getHighwayList()

        for highway in highways:
            path = []

            # add start of street
            startIdx = -1
            for idx in range(0, len(highway.nds) - 1):
                if highway.nds[idx] in self.getListOfOsmIsOfCurrentGraphNode():
                    path.append(self.getRealGraphNodeByOsmId(
                        highway.nds[idx])[0])
                    startIdx = idx
                    break

            # add end of street
            endIdx = -1
            for idx in range(len(highway.nds) - 1, 0, -1):
                if highway.nds[idx] in self.getListOfOsmIsOfCurrentGraphNode():
                    endIdx = idx
                    break

            # equation of line
            for idx in range(startIdx + 1, endIdx):
                node1 = self.getNodeByOsmId(highway.nds[idx - 1])
                node2 = self.getNodeByOsmId(highway.nds[idx])
                nextNode = self.getTheNearBuildingInTheSameStreetAndDistance(
                    node1, node2, path)
                path.append(nextNode)

            streetName = highway.tags['name']
            isOneWay = True if ('oneway' in highway.tags) and (
                highway.tags['oneway'] == 'yes') else False

            for id in range(0, len(path) - 2):
                node1X, node1Y = self.graph.nodes(
                    data=True)[id]['pos'][0], self.graph.nodes(data=True)[id]['pos'][1]
                node2X, node2Y = self.graph.nodes(data=True)[id + 1]['pos'][0], \
                    self.graph.nodes(data=True)[id + 1]['pos'][1]
                dist = self.getDistance(node1X, node1Y, node2X, node2Y)
                dist *= 1000
                dist = int(dist)
                if isOneWay:
                    self.graph.add_edge(
                        path[id], path[id + 1], weight=dist, streetName=streetName)
                else:
                    self.graph.add_edge(
                        path[id], path[id + 1], weight=dist, streetName=streetName)
                    self.graph.add_edge(
                        path[id + 1], path[id], weight=dist, streetName=streetName)

                # sys.stdin.read(1)
            print(path)

    def appendCrossing(self):
        highways = self.getHighwayList()
        for highway1 in highways:

            # start of street
            for nd in highway1.nds:
                if self.isCorrectNode(nd) and nd not in self.getListOfOsmIsOfCurrentGraphNode():
                    self.addNode(nd, "", "", isPostOffice=False)
                    break
            # end of street
            for nd in reversed(highway1.nds):
                if self.isCorrectNode(nd) and nd not in self.getListOfOsmIsOfCurrentGraphNode():
                    self.addNode(nd, "", "", isPostOffice=False)
                    break

            for highway2 in highways:
                if highway1.id != highway2.id:
                    for ndH1 in highway1.nds:
                        for ndH2 in highway2.nds:
                            if ndH1 == ndH2 and ndH1 not in self.getListOfOsmIsOfCurrentGraphNode():
                                if self.isCorrectNode(ndH1):
                                    self.addNode(
                                        ndH1, "", "", isPostOffice=False)

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
            if 'highway' in elem.tags and 'name' in elem.tags and elem.tags['name'] in streetNames:
                highways.append(elem)

        return highways

    def getTheNearBuildingInTheSameStreetAndDistance(self, node1, node2, path):
        epsilon = 1
        step = 0.001
        buildingId = -1
        minDist = float('inf')
        for x in numpy.arange(node1.x, node2.x, step):
            y = self.getEquationOfStreet(
                x, node1.x, node1.y, node2.x, node2.y)
            for node in self.graph.nodes(data=True):
                if node[0] not in path:

                    buildingOsm = self.getNodeByOsmId(node[1]['osmId'])
                    dist = self.getDistance(
                        buildingOsm.x, buildingOsm.y, x, y)
                    if dist < minDist and dist < epsilon:
                        minDist = dist
                        buildingId = node[0]
        return buildingId

    def getEquationOfStreet(self, x, x1, y1, x2, y2):
        return ((y1-y2)/(x1-x2)) * x + (y1-(y1-y2)/(x1-x2)*x1)

    def getDistance(self, node1X, node1Y, node2X, node2Y):
        return sqrt((node2X-node1X)**2 + (node2Y-node1Y)**2)

    def getBuildingList(self):
        buildings = []
        for elem in self.osm.osmWays:
            if 'building' in elem.tags and 'addr:housenumber' in elem.tags and self.isCorrectNode(elem.nds[0]):
                buildings.append(elem)
        return buildings

    def addNode(self, osmIndex, houseNumber, streetName, isPostOffice=False):
        building = self.getNodeByOsmId(osmIndex)
        x, y = (building.x - float(self.osm.xmin)) * \
            scale, (building.y - float(self.osm.ymin)) * scale
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

    def getWayByOsmId(self, indexOsm):
        for way in self.osm.osmWays:
            if way.id == indexOsm:
                return way

