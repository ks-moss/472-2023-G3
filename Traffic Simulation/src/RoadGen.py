from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random as rng
from copy import deepcopy

# what to do next
#TODO add textures

class Road(Entity):

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.shader = None
        self.colorValue = kwargs['color']

        self.text = Text(text = name,
             parent = self,
             x = 0,
             y = 0.55,
             z = 0,
             origin = (0, 0),
             scale = (1, 30),
             world_rotation_x = 90,
             world_rotation_z = -90,
             current_color = color.white,
             shader = None)
        
        
    # create sidewalks
    def createSidewalks(self):
        length = int(self.scale_z) // 4
        for p in range(length):
            piece = Entity(model = 'cube',
                           parent = self,
                           x = .7501,
                           y = .3,
                           z = p/length - .5 + .5/length,
                           scale = (.5, 1, 1/length),
                           color = color.gray,
                           collider = 'box')
            if piece.intersects(ignore=RoadGen.ignoreList).hit:
                destroy(piece)
            RoadGen.ignoreList.append(piece)

            piece = Entity(model = 'cube',
                           parent = self,
                           x = -.7501,
                           y = .3,
                           z = p/length - .5 + .5/length,
                           scale = (.5, 1, 1/length),
                           color = color.gray,
                           collider = 'box')
            if piece.intersects(ignore=RoadGen.ignoreList).hit:
                destroy(piece)
            RoadGen.ignoreList.append(piece)

        for p in RoadGen.ignoreList:
            p.collider = None

            
            

    def on_mouse_enter(self):
        if not mouse.locked:
            self.color = color.white
            self.y += 0.01

    def on_mouse_exit(self):
        self.color = self.colorValue
        self.y -= 0.01

# RoadGen class used in the GraphicsEngine Class
# used for creating the roads for the simulation
# Functions:
#   __init__:               Creates the variables used for the RoadGen
class RoadGen:

    roadWidth = 6   # width scale
    ignoreList = []

    # constructor for RoadGen
    # parameters:
    #   AutoSim - object of class AutomaticSimulation
    def __init__(self, AutoSim):
        rng.seed(rng.random())
        self.roads = deepcopy(AutoSim.road_list)
        self.crossRoads = deepcopy(AutoSim.intersection_list)
        self.startingPoints = {}
        self.roadObjs = []
        self.nIntersections = {}


    def placeRoads(self):
        placedRoads = []
        directions = {'N': (0, 1),
                      'E': (1, 0),
                      'S': (0, -1),
                      'W': (-1, 0)}
        directionAngle = {'N': 0,
                          'E': 90,
                          'S': 180,
                          'W': 270}

        for intersection in self.crossRoads:
            x = intersection[0]['position']
            y = intersection[1]['position']
            w = self.roadWidth
            Entity(model = 'cube', scale = (w/2, 1, w/2), color = color.gray, position = (x - w*.75, .3, y - w*.75))
            Entity(model = 'cube', scale = (w/2, 1, w/2), color = color.gray, position = (x - w*.75, .3, y + w*.75))
            Entity(model = 'cube', scale = (w/2, 1, w/2), color = color.gray, position = (x + w*.75, .3, y - w*.75))
            Entity(model = 'cube', scale = (w/2, 1, w/2), color = color.gray, position = (x + w*.75, .3, y + w*.75))


            print(intersection[0]['road'], 'x', intersection[1]['road'])

            for road in intersection:

                # check if road was placed already
                if road['road'] in placedRoads:
                    self.nIntersections[road['road']] += 1
                    continue

                # place road into the list
                self.nIntersections[road['road']] = 1
                placedRoads.append(road['road'])

                # place road according to name & position
                name = road['road']
                position = road['position']
                dName = name.split(' ')[0]
                numD = directions[dName]

                dx = position if not numD[0] else 0
                dz = position if not numD[1] else 0

                # get length from roads list
                for r in self.roads:
                    if r['name'] == name:
                        length = r['length']

                roadObj = Road(name,
                               model = 'cube',
                               color = color.dark_gray,
                               collider = 'box',
                               x = dx,
                               z = dz,
                               rotation_x = 0,
                               rotation_y = directionAngle[dName],
                               rotation_z = 0,
                               scale_x = self.roadWidth,
                               scale_y = 1,
                               scale_z = length)
                
                self.roadObjs.append(roadObj)

                # create starting point entities
                startPoint = Entity(parent = roadObj,
                                    model = 'cube',
                                    z = -0.5,
                                    y = 1,
                                    scale = (1 / self.roadWidth, 1, 1 / length))
                self.startingPoints[name] = startPoint
        
        for r in self.roadObjs:
            r.createSidewalks()
        
    
    def clear(self):
        for e in self.roadObjs:
            destroy(e)
        for k, v in self.startingPoints.items:
            destroy(v)
