#!/usr/bin/python3

import xml.sax


class OsmNode(object):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.tags = {}


class OsmWay(object):
    def __init__(self, id, osm):
        self.id = id
        self.osm = osm
        self.nds = []  # list of nodes' references
        self.tags = {}


class Osm(object):
    def __init__(self, osmData):
        self.osmNodes = []
        self.osmWays = []
        superself = self

        class OsmHandler(xml.sax.ContentHandler):
            @classmethod
            def setDocumentLocator(self, loc):
                pass

            @classmethod
            def startDocument(self):
                pass

            @classmethod
            def endDocument(self):
                pass

            @classmethod
            def startElement(self, name, attrs):
                if name == 'node':
                    self.elem = OsmNode(attrs['id'], float(attrs['lon']), float(attrs['lat']))
                elif name == 'way':
                    self.elem = OsmWay(attrs['id'], superself)
                elif name == 'tag':
                    self.elem.tags[attrs['k']] = attrs['v']
                elif name == 'nd':
                    self.elem.nds.append(attrs['ref'])
                elif name == 'bounds':
                    superself.setRangeOfCoordinates(attrs['minlon'], attrs['maxlon'], attrs['minlat'], attrs['maxlat'])

            @classmethod
            def endElement(self, name):
                if name == 'node':
                    superself.osmNodes.append(self.elem)
                elif name == 'way':
                    superself.osmWays.append(self.elem)

            @classmethod
            def characters(self, chars):
                pass

            @classmethod
            def getElementIndexById(self, list, id):
                for ele in list:
                    if ele.id == id:
                        return list.index(ele)

        xml.sax.parseString(osmData, OsmHandler)

    def setRangeOfCoordinates(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
