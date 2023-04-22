from ursina import *
from ursina.shaders import lit_with_shadows_shader

class Sedan(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'sedan.glb'
        self.rotation_y = 180
        self.scale = 4
        self.color = color.rgba(255, 255, 255, 255)
        self.y = 0.15
        self.z = -5
        self.collider = 'box'
    
class Bus(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'bus.glb'
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -10
        self.collider = 'box'

class FireTruck(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'firetruck.glb'
        self.rotation_y = 180
        self.scale = 6
        self.y = 1
        self.z = -8
        self.collider = 'box'

class PoliceCar(Entity):
    def __init__(self, parent):
        super().__init__(parent = parent)
        self.model = 'policecar.glb'
        self.rotation_y = 180
        self.scale = 4
        self.y = 0.15
        self.z = -4
        self.collider = 'box'
        


# Vehicle class inherits the Entity class
# for display a vehicle onto the window
# Each vehicle has there own limit and position
# only created from the VehicleFactory class
class Vehicle(Entity):

    def __init__(self, limit, startingPoints, type, **kwargs):
        super().__init__(**kwargs)
        self.limit = limit
        self.roads = startingPoints

        if type == 'car':
            vehicle = Sedan(self)
        elif type == 'bus':
            vehicle = Bus(self)
        elif type == 'fire truck':
            vehicle = FireTruck(self)
        elif type == 'police van':
            vehicle = PoliceCar(self)

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
                              z = pos)
            self.vehicleObjs.append(vehicle)
    
    # called by the engine every frame
    # first invokes the function to update the values of each
    # vehicle using @AutomaticSimulation.vehicle_on_road()
    # grabs the data from the vehicle states and sends them 
    # to each of the vehicles respectivelly
    def update(self):
        self.autoSim.vehicle_on_road()
        for e, v in zip(self.vehicleObjs, self.vehicles):
            if not e.move(v):
                destroy(e)
                self.vehicleObjs.remove(e)
                self.vehicles.remove(v)


