import pygame
from vector import Vector2
from constants import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
    
    def getNeighbors(self):
        return self.neighbors
    
    def getPosition(self):
        return self.position
    
    # def __str__(self):        
    #     return f"{self.position.x},{self.position.y}"
    
    def __eq__(self, otro):
        if isinstance(otro, Node): # Reemplaza 'Node' por el nombre exacto de tu clase
            return self.position.x == otro.position.x and self.position.y == otro.position.y
        return False

    def __hash__(self):
        # Permite que el diccionario indexe el nodo usando sus coordenadas
        return hash((self.position.x, self.position.y))

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                # line_start = self.position.asTuple()
                # line_end = self.neighbors[n].position.asTuple()
                # pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, GREEN, self.position.asInt(), 8)
    def __lt__(self, other):
        return (self.position.x < other.position.x)

class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.mazeCosts = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']+[str(x) for x in range(1, 101)]
        self.costSymbols = [str(x) for x in range(1, 101)]
        self.mazeCostsNodes = {}
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.createCostsTable(data)

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT
    
    def createCostsTable(self, data, xoffset=0, yoffset=0):
       for row in list(range(data.shape[0])):
           for col in list(range(data.shape[1])):
               if data[row][col] in self.costSymbols:
                   x, y = self.constructKey(col+xoffset, row+yoffset)
                   self.mazeCosts[(x, y)] = data[row][col]
                   self.mazeCostsNodes[(x, y)]=Node(x,y)
                   
    def getMazeCosts(self):
        return self.mazeCosts
    
    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None
           
    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None
    
    def getCostNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.mazeCostsNodes.keys():
            return self.mazeCostsNodes[(x, y)]
        return None
    
    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def getNodes(self):
        return self.nodesLUT
    
    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def render(self, screen):
        for nwco in self.nodesLUT.values():
            if nwco not in self.mazeCostsNodes:
                nwco.render(screen)
        # nodesWithoutCosts=[nwco for nwco in self.nodesLUT.values() not in self.mazeCostsNodes]
        # for node in nodesWithoutCosts:#self.nodesLUT.values() not in self.mazeCostsNodes:
        #     node.render(screen)