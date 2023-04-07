from ursina import *
import random as rng


# GridMap class used in the GraphicsEngine Class
# used for creating the road maps for the simulation
# Functions:
#   __init__:               Creates the variables used for the GridMap
#   setTile:                places a texture at a x & y position in the grid
#   cutMap:                 removes unused rows & columns in the array
#   paddingCheck:           uses the padding variables to check the spacing of roads
#   createIntersections:    creates the intersections of the input file
#   createRoads:            creates the roads of the input file
#   print:                  DEBUG - prints the 2D array grid map
class GridMap:

    SCALE = 50          # the size of tiles (ex. 100 = 100x100 units)
    MIN_PADDING = 4     # minimum distance between roads
    MAX_PADDING = 10    # maximum distance between roads

    def __init__(self, roads, intersections):
        rng.seed(rng.random())
        self.roads = roads
        self.intersections = intersections
        self.xSize = ceil(max([r['length'] for r in self.roads]) / self.SCALE)
        self.ySize = self.xSize
        self.map = [['' for _ in range(self.xSize)] for _ in range(self.ySize)]
        self.map[0][0] = color.black
        self.map[0][1] = color.white


    # only used in method @createWorldMap
    # places a texture onto the map grid based on the x & y inputs
    # will extend the grid if x | y falls out of bounds
    # parameters:
    #   x       - x position of tile
    #   y       - y position of tile
    #   texture - texture of tile
    #   startx  - starting x of a road (changes if map is extended to left)
    #   starty  - starting y of a road (changes if map is extended to down)
    # return:
    #   startx  - same as startx | different if map is expanded
    #   starty  - same as starty | different if map is expanded
    def setTile(self, x, y, texture, startx, starty):
        # if startx or starty out of bounds
        if startx >= self.xSize:
            for _ in range(startx + 1 - self.xSize):
                for row in range(self.ySize):
                    self.map[row].extend([''])
        elif startx < 0:
            for _ in range(abs(startx)):
                for row in range(self.ySize):
                    self.map[row] = ['', *self.map[row]]
            startx = 0
            x = 0
        self.xSize = len(self.map[0])

        if starty >= self.ySize:
            for _ in range(starty + 1 - self.ySize):
                self.map = [*self.map, ['' for _ in range(self.xSize)]]
        elif starty < 0:
            for _ in range(abs(starty)):
                self.map = [['' for _ in range(self.xSize)], *self.map]
            starty = 0
            y = 0
        self.ySize = len(self.map)


        # if x or y out of bounds
        if (x >= self.xSize):                                           # extend right
            for row in range(len(self.map)): 
                self.map[row].extend([''])
        elif (x < 0):                                                   # extend left
            for row in range(len(self.map)): 
                self.map[row] = ['', *self.map[row]]
            startx += 1
        self.xSize = len(self.map[0])

        if (y >= self.ySize):                                           # extend up
            self.map = [*self.map, ['' for _ in range(self.xSize)]]
        elif (y < 0):                                                   # extend down
            self.map = [['' for _ in range(self.xSize)], *self.map]
            starty += 1
        self.ySize = len(self.map)


        x = clamp(x, 0, self.xSize - 1)
        y = clamp(y, 0, self.ySize - 1)

        self.map[y][x] = texture
        return startx, starty



    # cutMap
    # takes the current map array and removes unused columns and rows
    # the function automatically adjusts the map size variables
    def cutMap(self):
        y = 0
        while (y < len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] != '':
                    y += 1
                    break
            else:
                # remove slice
                self.map.pop(y)

        x = 0
        while (x < len(self.map[0])):
            for y in range(len(self.map)):
                if self.map[y][x] != '':
                    x += 1
                    break
            else:
                for i in range(len(self.map)): 
                    self.map[i].pop(x)
        
        self.xSize = len(self.map[0])
        self.ySize = len(self.map)

    

    # paddingCheck
    # checks around the designated coordinates if there are other tiles
    # within the padding range (MIN_PADDING, MAX_PADDING)
    # parameters:
    #   tileX           - the x coordinate of the designated tile
    #   tileY           - the y coordinate of the designated tile
    #   checkMaxPadding - toggle whether to check the max padding or not
    # returns:
    #   True            - if there's no tile < minimum padding & there's a tile in the padding range
    #   False           - if there's a tile < minimum padding or there's no tile in the padding range
    def paddingCheck(self, tileX, tileY, checkMaxPadding):
        minP = self.MIN_PADDING
        maxP = self.MAX_PADDING

        def getTile(x, y):
            try:
                t = self.map[y][x]
            except:
                t = ''
            return t
        
        # -------- check for minimum padding first -----------
        for y in range(-minP, minP):
            for x in range(-minP, minP):
                if getTile(tileX + x, tileY + y) != '':
                    return False
                
        # -------- check for maximum padding next ------------
        if not checkMaxPadding:
            return True
        
        for y in range(-maxP, maxP):
            if y in range(-minP, minP):
                for x in [*range(-maxP, -minP), *range(minP, maxP)]:
                    if getTile(tileX + x, tileY + y) != '':
                        return True
            else:
                for x in range(-maxP, maxP):
                    if getTile(tileX + x, tileY + y) != '':
                        return True
        
        return False

    

    # createIntersections
    # This function should be called before @createRoads
    # Places the intersections on the map using the intersection list
    # PostCondition:
    #   map will have all of the intersections placed without any collisions
    #TODO add ability to use more than one intersection
    #TODO check if path is clear before placing roads
    def createIntersections(self):
        # create intersections
        for i in self.intersections:
            while True:
                ix = rng.randint(0, self.xSize)
                iy = rng.randint(0, self.ySize)
                if self.paddingCheck(ix, iy, False):
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
    
    

    # createRoads
    # This function should be called after @createIntersections
    # this will place the remaining roads in the roads list
    # no road should be colliding with another road.
    # spacing should be correct with the padding variables
    def createRoads(self):
        cDir = [{'x' : 0, 'y' : 1},     # north
                {'x' : 1, 'y' : 0},     # west
                {'x' : 0, 'y' : -1},    # south
                {'x' : -1, 'y' : 0}]    # east
        
        for road in self.roads:
            if 'isPlaced' in road.keys():
                continue

            # find a clear path to place the road
            isClear = False
            rng.shuffle(cDir)

            tries = 0
            expansion = 0
            while not isClear:

                # get a random starting position
                startX = rng.randint(-expansion, self.xSize + expansion)
                startY = rng.randint(-expansion, self.ySize + expansion)
                length = road['length'] // self.SCALE

                for d in cDir:
                    isFirst = True
                    for l in range(length):
                        xi = startX + (l * d['x'])
                        yi = startY + (l * d['y'])
                        if not self.paddingCheck(xi, yi, isFirst):
                            break
                        isFirst = False
                    else:
                        isClear = True
                        break

                tries += 1
                expansion = expansion + 1 if tries % 10 == 0 else expansion

            # place the road
            startX, startY = self.setTile(startX, startY, color.brown, startX, startY)
            for l in range(1, length):
                xi = startX + (l * d['x'])
                yi = startY + (l * d['y'])
                startX, startY = self.setTile(xi, yi, color.yellow, startX, startY)

            self.cutMap()



    # print
    # Only used for debugging purposes
    # since I can't see the game during the loading phase.
    def print(self):
        print('\n' * 10)
        for y in range(self.ySize):
            for x in range(self.xSize):
                tile = self.map[y][x]
                tile = ' 0' if tile != '' else ' -'
                print(tile, end='')
            print()