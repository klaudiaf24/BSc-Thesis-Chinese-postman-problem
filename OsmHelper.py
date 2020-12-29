#!/usr/bin/python3

import urllib.request
import OsmParser
import OsmGraph


def getGraphFromOsm(left, bottom, right, top):
    osmMapData = getOsmData(False, top=top, right=right, bottom=bottom, left=left)
    osm = OsmGraph.OsmGraph(osmMapData)
    return osm.graph, osm.getRange()


def getGraphFromFile(filename):
    osmMapData = getOsmData(True, filename=filename)
    osm = OsmGraph.OsmGraph(osmMapData)
    return osm.graph, osm.getRange()


def getOsmData(isFile, filename='', top=-1, right=-1, bottom=-1, left=-1):
    if isFile:
        return OsmParser.Osm(open(filename, 'r').read())
    else:
        request = "http://api.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % (left, bottom, right, top)
        fp = urllib.request.urlopen(request)
        return fp.read().decode('utf-8')
