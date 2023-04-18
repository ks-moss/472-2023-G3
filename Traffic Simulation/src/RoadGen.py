from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random as rng
from copy import deepcopy

# what to do next
#TODO add textures

class Road(Entity):

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.colorValue = kwargs['color']

        Text(text = name,
             parent = self,
             x = 0,
             y = 0.55,
             z = 0,
             origin = (0, 0),
             scale = (1, 30),
             world_rotation_x = 90,
             world_rotation_z = 90,
             color = color.white)

    def on_mouse_enter(self):
        if not mouse.locked:
            self.always_on_top = True
            self.color = color.white

    def on_mouse_exit(self):
        self.always_on_top = False
        self.color = self.colorValue

# RoadGen class used in the GraphicsEngine Class
# used for creating the roads for the simulation
# Functions:
#   __init__:               Creates the variables used for the RoadGen
class RoadGen:

    roadWidth = 5   # width scale

    # constructor for RoadGen
    # parameters:
    #   AutoSim - object of class AutomaticSimulation
    def __init__(self, AutoSim):
        rng.seed(rng.random())
        self.roads = deepcopy(AutoSim.road_list)
        self.crossRoads = deepcopy(AutoSim.intersection_list)
        self.startingPoints = {}
        self.roadObjs = []


    def placeRoads(self):
        placedRoads = []
        directions = {'N': (0, 1),
                      'E': (1, 0),
                      'S': (0, -1),
                      'W': (-1, 0)}
        directionAngle = {'N': 90,
                          'E': 0,
                          'S': 270,
                          'W': 180}

        for intersection in self.crossRoads:
            print(intersection[0]['road'], 'x', intersection[1]['road'])

            for road in intersection:

                # check if road was placed already
                if road['road'] in placedRoads:
                    continue

                # place road into the list
                placedRoads.append(road['road'])

                # place road according to name & position
                name = road['road']
                position = road['position']
                dName = name.split(' ')[0]
                numD = directions[dName]

                dx = position if not numD[1] else 0
                dz = position if not numD[0] else 0

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
                               scale_z = length,
                               scale_x = self.roadWidth,
                               scale_y = 1)
                
                self.roadObjs.append(roadObj)

                # create starting point entities
                startPoint = Entity(parent = roadObj,
                                    z = -0.5,
                                    y = 1,
                                    scale = (1 / self.roadWidth, 1, 1 / length))
                self.startingPoints[name] = startPoint
        
    
    def clear(self):
        for e in self.roadObjs:
            destroy(e)
        for k, v in self.startingPoints.items:
            destroy(v)
