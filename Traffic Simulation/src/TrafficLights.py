from ursina import Entity, destroy, color

#TODO make model of traffic light
#TODO make vehicles stop for red light

# class Light
# inherits ursina.Entity and all its attributes
# holds the position and model of the traffic light
class Light(Entity):

    offset = 0.5 # move to the side of the road

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position -= self.right * self.offset


# class TrafficLights
# inherits ursina.Entity for the use of the update function
# creates the traffic lights from the AutomaticSimulation class
class TrafficLights(Entity):

    lightObjs = []
    SCALE = 20
    ROAD_SCALE = 50
    ppt = SCALE * 0.191
    ratio = None

    def __init__(self, autoSim, startingPoints):
        super().__init__()
        TrafficLights.ppt = self.SCALE * 0.191
        TrafficLights.ratio = self.ppt / self.ROAD_SCALE

        self.autoSim = autoSim
        self.tlights = autoSim.traffic_light_list
        self.tlightStates = autoSim.trafficlight_current_state
        self.glight = autoSim.green_light
        self.startPoints = startingPoints

        self.createTrafficLights()

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

            light = Light(model = 'cube',
                          parent = start,
                          z = pos * self.ratio,
                          color = color.green)
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
                l.color = color.green
            else:
                l.color = color.red




