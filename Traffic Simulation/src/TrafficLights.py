from ursina import *
from ursina.shaders import lit_with_shadows_shader

#TODO make model of traffic light
#TODO make vehicles stop for red light

# class Light
# inherits ursina.Entity and all its attributes
# holds the position and model of the traffic light
class Light(Entity):

    offset = 3 # move to the side of the road

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.z += self.offset

        # create light pole model
        lightpole = Entity(model = 'trafficlight.glb',
               parent = self,
               x = 2.2,
               z = 0.2,
               y = 0.2,
               scale = 5)
        
        self.glight = Entity(model = 'sphere',
                        parent = lightpole,
                        scale = 0.1,
                        x = -0.19,
                        y = 0.55,
                        z = -0.03,
                        color = color.green)
        
        self.rlight = Entity(model = 'sphere',
                        parent = lightpole,
                        scale = 0.1,
                        x = -0.19,
                        y = 0.68,
                        z = -0.03,
                        color = color.red)
        
        self.walk = Entity(model = 'quad',
                           parent = lightpole,
                           scale = 0.06,
                           x = 0.26,
                           y = 0.23,
                           z = -0.05,
                           color = color.white)
    
    def green(self):
        self.glight.color = color.green
        self.rlight.color = color.black
        self.walk.color = color.white

    def red(self):
        self.glight.color = color.black
        self.rlight.color = color.red
        self.walk.color = color.red


# class TrafficLights
# inherits ursina.Entity for the use of the update function
# creates the traffic lights from the AutomaticSimulation class
class TrafficLights(Entity):

    lightObjs = []

    def __init__(self, autoSim, startingPoints):
        super().__init__()
        self.autoSim = autoSim
        self.tlights = autoSim.traffic_light_list
        self.tlightStates = autoSim.trafficlight_current_state
        self.glight = autoSim.green_light
        self.startPoints = startingPoints


    # createTrafficLights
    # called after the TrafficLights class is instantiated
    # creates and places each Light object into the scene
    # position is calculated and given to the entity
    # the entity is added to the lightObjs list for later use
    def createTrafficLights(self):
        for l in self.tlights:
            road  = l['road']
            pos   = l['position']
            start = self.startPoints[road]

            light = Light(parent = start,
                          z = pos)
            self.lightObjs.append(light)

    # update
    # overrides parent class update
    # called for every frame of the simulation
    # uses AutomaticSimulation.green_light for the
    # state of each traffic light.
    # changes the color of the traffic light when the cycle 
    # starts and finishes
    def update(self):
        self.autoSim.traffic_light_on_road()
        for l, s in zip(self.lightObjs, self.tlightStates):
            name = s['road']
            if self.glight[name]:
                l.green()
            else:
                l.red()




