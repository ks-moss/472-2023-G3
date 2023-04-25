from ursina import *
from ursina.shaders import lit_with_shadows_shader
from threading import Thread
import random as rng
rng.seed(rng.random())

#TODO adjust vehicle scales & positions

class Sedan(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'sedan.glb'
        self.rotation_y = 180
        self.scale = 4
        self.color = color.rgba(255, 255, 255, 255)
        self.y = 0.15
        self.z = -4
        self.collider = 'box'
        self.add_to_scene_entities = False
    
class Bus(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'bus.glb'
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -10
        self.collider = 'box'
        self.add_to_scene_entities = False

class FireTruck(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'firetruck.glb'
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -8
        self.collider = 'box'
        self.add_to_scene_entities = False

class PoliceCar(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'policecar.glb'
        self.rotation_y = 180
        self.scale = 5
        self.y = 0.4
        self.z = -6
        self.collider = 'box'
        self.add_to_scene_entities = False

class Ambulance(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'ambulance.glb'
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -6.5
        self.collider = 'box'
        self.add_to_scene_entities = False

class OffRoad(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        i = rng.randint(0, 3)
        self.model = 'offroad{}.glb'.format(i)
        self.rotation_y = 180
        self.scale = 6
        self.y = 0.5
        self.z = -5.7
        self.collider = 'box'
        self.add_to_scene_entities = False

class SportsCar(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        i = rng.randint(0, 3)
        self.model = 'sportscar{}.glb'.format(i)
        self.rotation_y = 180
        self.scale = 5
        self.y = 0.14
        self.z = -5
        self.collider = 'box'
        self.add_to_scene_entities = False

class Tuner(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        i = rng.randint(0, 3)
        self.model = 'tunercar{}.glb'.format(i)
        self.rotation_y = 180
        self.scale = 6
        self.y = 0.5
        self.z = -5
        self.collider = 'box'
        self.add_to_scene_entities = False

class IceCreamTruck(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'icecreamtruck.glb'
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -4.5
        self.collider = 'box'
        self.add_to_scene_entities = False

class Camper(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        i = rng.randint(0, 3)
        self.model = 'camper{}.glb'.format(i)
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -4.5
        self.collider = 'box'
        self.add_to_scene_entities = False

        


# Vehicle class inherits the Entity class
# for display a vehicle onto the window
# Each vehicle has there own limit and position
# only created from the VehicleFactory class
class Vehicle(Entity):

    def __init__(self, limit, startingPoints, type, **kwargs):
        super().__init__(**kwargs)
        self.limit = limit
        self.roads = startingPoints
        # self.model = 'cube'

        if type in ['car', 'auto']:
            i = rng.randint(0, 5)
            match(i):
                case 0:
                    Sedan(self)
                case 1:
                    Camper(self)
                case 2:
                    IceCreamTruck(self)
                case 3:
                    OffRoad(self)
                case 4:
                    SportsCar(self)
                case 5:
                    Tuner(self)

        elif type == 'bus':
            Bus(self)
        elif type == 'fire truck':
            FireTruck(self)
        elif type == 'police van':
            PoliceCar(self)
        elif type == 'ambulance':
            Ambulance(self)

    # used when moving the vehicle
    # called from @VehicleFactory.update
    # returns:
    #   False   - vehicle is out of bounds
    #   True    - vehicle is on road
    def move(self, simVehicle):
        pos = simVehicle['position']
        road = simVehicle['road']
        self.parent = self.roads[road]

        if pos > self.limit:
            return False
        
        self.z = pos
        return True


# VehicleFactory class inherits Entity
# only for the use of the update function
# this class is used to create the default vehicles
# from the xml file and can be used to add additional vehicles
# from the vehicle generator
# uses the data from the AutomaticSimulation file
class VehicleFactory(Entity):

    vehicleObjs = []

    def __init__(self, autoSim, startingPoints):
        super().__init__()

        self.limits = {}
        for road in autoSim.road_list:
            self.limits[road['name']] = road['length']
        self.startPoints = startingPoints
        self.vehicles = autoSim.vehicle_list
        self.autoSim = autoSim

    # creates the vehicles that are listed on the xml file
    # initially and creates a Vehicle object based on the 
    # data from AutomaticSimulation
    def createInitVehicles(self):
        for v in self.vehicles:
            road = v['road']
            pos = v['position']
            vtype = v['type']
            start = self.startPoints[road]
            limit = self.limits[road]

            vehicle = Vehicle(limit, 
                              self.startPoints,
                              parent = start,
                              type = vtype,
                              z = pos,
                              add_to_scene_entities = False)
            self.vehicleObjs.append(vehicle)
    
    def moveVehicles(self, objs, vehicles):
        for e, v in zip(objs, vehicles):
            if not e.move(v):
                destroy(e)
                objs.remove(e)
                vehicles.remove(v)

    def addVehicle(self):
        if self.autoSim.vehicle_generator_update():
            newVehicle = self.vehicles[-1]
            road = newVehicle['road']
            pos = newVehicle['position']
            vtype = newVehicle['type']
            start = self.startPoints[road]
            limit = self.limits[road]

            vehicle = Vehicle(limit, 
                              self.startPoints,
                              parent = start,
                              type = vtype,
                              z = pos)
            self.vehicleObjs.append(vehicle)
    
    # called by the engine every frame
    # first invokes the function to update the values of each
    # vehicle using @AutomaticSimulation.vehicle_on_road()
    # grabs the data from the vehicle states and sends them 
    # to each of the vehicles respectivelly
    def update(self):
        Thread(target=self.autoSim.vehicle_on_road).start()
        Thread(target=self.moveVehicles, args=(self.vehicleObjs, self.vehicles)).start()
        Thread(target=self.addVehicle).start()
        
    



