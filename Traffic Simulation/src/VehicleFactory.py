from ursina import Entity, color, destroy


# Vehicle class inherits the Entity class
# for display a vehicle onto the window
# Each vehicle has there own limit and position
# only created from the VehicleFactory class
class Vehicle(Entity):

    def __init__(self, limit, **kwargs):
        super().__init__(**kwargs)
        self.limit = limit

    # used when moving the vehicle
    # called from @VehicleFactory.update
    # returns:
    #   False   - vehicle is out of bounds
    #   True    - vehicle is on road
    def move(self, pos):
        if pos > self.limit:
            return False
        
        self.z = pos / 13 # <- supposedly the golden ratio
        return True


# VehicleFactory class inherits Entity
# only for the use of the update function
# this class is used to create the default vehicles
# from the xml file and can be used to add additional vehicles
# from the vehicle generator
# uses the data from the AutomaticSimulation file
class VehicleFactory(Entity):

    vehicleObjs = []
    SCALE = 20

    def __init__(self, autoSim, startingPoints):
        super().__init__()
        self.limits = {}
        for road in autoSim.road_list:
            self.limits[road['name']] = road['length']
        self.startPoints = startingPoints
        self.vehicles = autoSim.vehicle_list
        self.vStates = autoSim.vehicle_current_state
        self.autoSim = autoSim
        self.createInitVehicles()

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
                              parent = start,
                              z = pos // self.SCALE,
                              model = 'sphere',
                              color = color.white)
            self.vehicleObjs.append(vehicle)
    
    # called by the engine every frame
    # first invokes the function to update the values of each
    # vehicle using @AutomaticSimulation.vehicle_on_road()
    # grabs the data from the vehicle states and sends them 
    # to each of the vehicles respectivelly
    def update(self):
        self.autoSim.vehicle_on_road()
        for e, s, v in zip(self.vehicleObjs, self.vStates, self.vehicles):
            if not e.move(s['position']):
                destroy(e)
                self.vehicleObjs.remove(e)
                self.vStates.remove(s)
                self.vehicles.remove(v)


