from ursina import *
import random as rng

class GridMap:

    SCALE = 50      # the size of tiles (ex. 100 = 100x100 units)
    PADDING = 4     # minimum distance between roads

    def __init__(self, roads, intersections):
        self.roads = roads
        self.intersections = intersections
        self.xSize = ceil(max([r['length'] for r in self.roads]) / self.SCALE)
        self.ySize = self.xSize
        self.map = [[color.green for _ in range(self.xSize)] for _ in range(self.ySize)]
        self.map[0][0] = ''


    # only used in method @createWorldMap
    # places a texture onto the map grid based on the x & y inputs
    # will extend the grid if x | y falls out of bounds
    # parameters:
    #   x       - x position of tile
    #   y       - y position of tile
    #   texture - texture of tile
    #   map     - grid map containing the textures used for the roads
    #   startx  - starting x of a road (changes if map is extended to left)
    #   starty  - starting y of a road (changes if map is extended to down)
    # return:
    #   startx  - same as startx | different if map is expanded
    #   starty  - same as starty | different if map is expanded
    #   map     - updated map with expansions (only needed if map extension is possible)
    def setTile(self, x, y, texture, startx, starty):
        # if x or y out of bounds
        if (x >= self.xSize):                                        # extend right
            for row in range(len(self.map)): 
                self.map[row].extend([color.white])
        elif (x < 0):                                                   # extend left
            for row in range(len(self.map)): 
                self.map[row] = [color.white, *self.map[row]]
            startx += 1
        if (y >= self.ySize):                                        # extend up
            self.map = [*self.map, [color.white for _ in range(self.xSize)]]
        elif (y < 0):                                                   # extend down
            self.map = [[color.white for _ in range(self.xSize)], *self.map]
            starty += 1

        self.xSize = len(self.map[0])
        self.ySize = len(self.map)
        x = clamp(x, 0, self.xSize - 1)
        y = clamp(y, 0, self.ySize - 1)

        self.map[y][x] = texture
        return startx, starty




    def cutMap(self):
        y = 0
        while (y < len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] != color.green and self.map[y][x] != color.white and self.map[y][x] != '':
                    y += 1
                    break
            else:
                # remove slice
                self.map.pop(y)

        x = 0
        while (x < len(self.map[0])):
            for y in range(len(self.map)):
                if self.map[y][x] != color.green and self.map[y][x] != color.white and self.map[y][x] != '':
                    x += 1
                    break
            else:
                for i in range(len(self.map)): 
                    self.map[i].pop(x)
        
        self.xSize = len(self.map[0])
        self.ySize = len(self.map)

    

    def paddingCheck(self, x, y):
        padding = self.PADDING

        # check horizontals
        for p in range(-padding, padding):
            try:
                tile = self.map[x + p][y]
            except(IndexError):
                tile = ''
            if tile == color.blue or tile == color.red:
                return False
        
        # check verticals
        for p in range(-padding, padding):
            try:
                tile = self.map[x + p][y]
            except(IndexError):
                tile = ''
            if  tile == color.blue or tile == color.red:
                return False
            
        # check diagonals
        for p in range(-padding, padding):
            try:
                tile = self.map[x+p][y+p]
            except(IndexError):
                tile = ''
            if tile == color.blue or tile == color.red:
                return False
            

            try:
                tile = self.map[x+p][y-p]
            except(IndexError):
                tile = ''
            if tile == color.blue or tile == color.red:
                return False
        
        return True
    


    def createIntersections(self):
        # create intersections
        for i in self.intersections:
            while True:
                ix = rng.randint(0, self.xSize)
                iy = rng.randint(0, self.ySize)
                if self.paddingCheck(ix, iy):
                    break
            self.setTile(ix, iy, color.black, ix, iy)

            # create roads for those intersections
            for iroad in [0, 1]:
                # find road in road list
                for r in self.roads:
                    if r['name'] == i[iroad]['road']:
                        road = r
                        break
                
                # get the length of the road split by the intersection
                frontDist = (road['length'] - i[iroad]['position']) // self.SCALE
                backDist = i[iroad]['position'] // self.SCALE

                # place road behind intersection
                for n in range(1, backDist - 1):
                        ix, iy = self.setTile(ix if iroad else ix - n, 
                                                        (iy - n) if iroad else iy, 
                                                        color.blue if iroad else color.red, 
                                                        ix, iy)

                # place road ahead intersection
                for n in range(1, frontDist - 1):
                        ix, iy = self.setTile(ix if iroad else ix + n, 
                                                        (iy + n) if iroad else iy, 
                                                        color.blue if iroad else color.red, 
                                                        ix, iy)
                
                r['isPlaced'] = True
        self.cutMap()
    
    

    def createRoads(self):
        for road in self.roads:
            if 'isPlaced' in road.keys():
                continue

            # find a clear path to place the road
            isClear = False
            cDir = [{'x' : 0, 'y' : 1},     # north
                    {'x' : 1, 'y' : 0},     # west
                    {'x' : 0, 'y' : -1},    # south
                    {'x' : -1, 'y' : 0}]    # east

            while not isClear:
                # get a random starting position
                x = rng.randint(0, self.xSize)
                y = rng.randint(0, self.ySize)
                length = road['length'] // self.SCALE

                for d in cDir:
                    for l in range(length):
                        try:
                            tile = self.map[y + (l * d['y'])][x + (l * d['x'])]
                        except(IndexError):
                            tile = ''    
                        if not self.paddingCheck(x+(l*d['x']), y+(l*d['y'])):
                            break
                    else:
                        isClear = True
                        break
            
            # place the road
            self.setTile(x, y, color.brown, x, y)
            for l in range(1, length):
                x, y = self.setTile(x + (l * d['x']), y + (l * d['y']), color.yellow, x, y)
            self.cutMap()