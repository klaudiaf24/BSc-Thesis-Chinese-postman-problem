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
        [self.xmin, self.xmax, self.ymin, self.ymax] = [0, 0, 0, 0]
        self.osmNodes = []
        self.osmWays = []
        superself = self

        class OsmHandler(xml.sax.ContentHandler):
            @classmethod
            def setDocumentLocator(cls, loc):
                pass

            @classmethod
            def startDocument(cls):
                pass

            @classmethod
            def endDocument(cls):
                pass

            @classmethod
            def startElement(cls, name, attrs):
                if name == 'node':
                    cls.elem = OsmNode(attrs['id'], float(attrs['lon']), float(attrs['lat']))
                elif name == 'way':
                    cls.elem = OsmWay(attrs['id'], superself)
                elif name == 'tag':
                    cls.elem.tags[attrs['k']] = attrs['v']
                elif name == 'nd':
                    cls.elem.nds.append(attrs['ref'])
                elif name == 'bounds':
                    superself.setRangeOfCoordinates(attrs['minlon'], attrs['maxlon'], attrs['minlat'], attrs['maxlat'])

            @classmethod
            def endElement(cls, name):
                if name == 'node':
                    superself.osmNodes.append(cls.elem)
                elif name == 'way':
                    superself.osmWays.append(cls.elem)

            @classmethod
            def characters(cls, chars):
                pass

            @classmethod
            def getElementIndexById(cls, listOfAllElements, id):
                for ele in listOfAllElements:
                    if ele.id == id:
                        return listOfAllElements.index(ele)

        xml.sax.parseString(osmData, OsmHandler)

    def setRangeOfCoordinates(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
