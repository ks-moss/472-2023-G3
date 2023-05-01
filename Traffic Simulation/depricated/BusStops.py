from ursina import Entity, load_model


class Stop(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_to_scene_entities = False
        self.model = 'busstop.glb'
        self.scale = 5
        self.x = 7
        self.y = 1
        self.z -= 5
        self.rotation_y = 90



class BusStops(Entity):
    def __init__(self, autoSim, startPoints):
        super().__init__()
        self.autoSim = autoSim
        self.startPoints = startPoints
        self.busStops = autoSim.bus_stop_list

    def createBusStops(self):
        for s in self.busStops:
            road = s['road']
            pos = s['position']
            start = self.startPoints[road]

            Stop(parent = start,
                 z = pos,
                 add_to_scene_entities = False)
            
    def update(self):
        self.autoSim.bus_stop_on_road()

