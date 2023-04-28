from ursina import *
import random
from SimulationWVehicleGenerator import VehicleGeneratorSimulation
from TrafficLightSimulation import *
import sys
#from VehicleGenerator import addVehicle

class Graphics:
    
    def __init__(self):

        self.trafficSystem = VehicleGeneratorSimulation("./InputFiles/prototype2.xml")

        # window module settings
        window.title = "Traffic Simulation 3D"
        window.vsync = False
        window.borderless = False
        window.fullscreen = True
        # window.fps_counter.disable()
        window.cog_button.disable()

        # Create a camera with a bird's eye view
        camera.orthographic = True
        camera.position = (35, 25, -35)
        camera.rotation = (25, -45, 45)
        camera.fov = 90

        # Text settings
        Text.size = 0.02
        self.text_message = Text(text="", y=.46, x=-.7, scale=2, color=color.red)

        # create base
        box = Entity(model='quad', scale=(280,200,0), color="76AE76")
        box.position = (0, 0, 20)

        self.vehicles = []
        self.triggerboxes = []
        self.roads_Entity_objects = [] # list of road entities
        self.lights_Entity_objects = [] # list of traffic light entities
        self.bus_stop_Entity_objects = []

        self.selectedRoad = ""
        self.tempSelectedPosition = 0
        self.selectedPosition = 0

        self.initializeRoads()
        self.initializeVehicles()
        self.initializeIntersections()
        self.initializeBusStop()

        add_vehicles_button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.50, 0.43), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=self.on_add_vehicle_button_click)
        restartButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.38, 0.43), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=self.on_restart_button_click)
        endButton = Button(text='End\nSimulation', color=rgb(128, 0, 0), highlight_color=color.red, position=(0.62, 0.43), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=self.on_end_button_click)
        addTrafficLightButton = Button(text='Add\nTraffic\nLight', color=color.blue, highlight_color=color.cyan, position=(.44, 0.34), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=self.add_traffic_light_button_click)
        addBusStopButton = Button(text='Add\nBus\nStop', color=color.blue, highlight_color=color.cyan, position=(.56, 0.34), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=self.add_bus_stop_button_click)
        self.selectedRoadNotifier = Button(text=("Road:\n"+self.selectedRoad), color=color.black, position=(.26, 0.43), scale=(0.1, 0.1), model='circle')
        self.selectedPositionNotifier = Button(text=("Position:\n"+str(self.selectedPosition)), color=color.black, position=(.14, 0.43), scale=(0.1, 0.1), model='circle', text_scale=0.3)
        


    def initializeRoads(self):
        num_NS_roads = 0
        num_EW_roads = 0

        # create road entities and calculate the number of NS and EW roads
        for r in self.trafficSystem.road_list:
            if (r["name"][0] == "N" or r["name"][0] == "S") and r["name"][1] == " ":
                num_NS_roads += 1
                road_model = Entity(model='cube', scale=(7, r["length"], 0.1), color=color.gray, collider='box', on_click=self.road_on_click)
                road_model.texture=load_texture(f'textures/road.png')
                road_model.name = r["name"]
                self.roads_Entity_objects.append(road_model)

            elif (r["name"][0] == "E" or r["name"][0] == "W") and r["name"][1] == " ":
                num_EW_roads += 1
                road_model = Entity(model='cube', scale=(r["length"], 7, 0.1), color=color.gray, collider='box', on_click=self.road_on_click)
                road_model.texture=load_texture(f'textures/road2.png')
                road_model.name = r["name"]
                self.roads_Entity_objects.append(road_model)
            
            else: #simple error checking
                print("Error - Road name must start with \'N \', \'S \', \'E \', or \'W \'")
                sys.exit()

        # simple error checking
        if num_NS_roads > 20 or num_EW_roads > 20:
            print("Error - Too many roads for this prototype!")
            sys.exit()

        # Caculate the amount of spacing between each road
        spacing_NS = (110 - 4*num_NS_roads) / (num_NS_roads+1)
        current_spacing_NS = -50
        spacing_EW = (110 - 4*num_EW_roads) / (num_EW_roads+1)
        current_spacing_EW = -50

        for i in range(len(self.trafficSystem.road_list)):
            r = self.trafficSystem.road_list[i]
            e = self.roads_Entity_objects[i]
            if (r["name"][0] == "N" or r["name"][0] == "S") and r["name"][1] == " ":
                current_spacing_NS += spacing_NS
                e.x = current_spacing_NS
                e.y = 0
                roadText= Text(text=r["name"], scale=(20,1), color=color.black)
                roadText.parent = road_model
                roadText.x = (e.x / (2*num_NS_roads)) - 3.5
                roadText.y = -.5
                roadText.z = -2

            elif (r["name"][0] == "E" or r["name"][0] == "W") and r["name"][1] == " ":
                current_spacing_EW += spacing_EW
                e.y = current_spacing_EW
                e.x = 0
                roadText= Text(text=r["name"], scale=(20,1), color=color.black)
                roadText.parent = road_model
                roadText.x = -13
                roadText.y = (e.y / (50*num_EW_roads)) - .02
                roadText.z = -2



    def initializeTrafficLights(self):
        for t in self.trafficSystem.traffic_light_list:
            for i in range(len(self.roads_Entity_objects)):
                r = self.roads_Entity_objects[i]
                if (r.name == t["road"]):
                    road_index = i

            r1 = self.roads_Entity_objects[road_index]
            if (r1.name[0] == "N" or r1.name[0] == "S") and r1.name[1] == " ":
                NS_traffic_y = (t["position"]-50) + ((100-self.trafficSystem.road_list[road_index]["length"])/2)
                NS_traffic_Entity = Entity(model='cube', scale=(5, 0.5, 1), color= color.green)
                NS_traffic_Entity.x = r1.x
                NS_traffic_Entity.y = NS_traffic_y + 4
                NS_traffic_Entity.z = -.5
                NS_traffic_Entity.name = t["road"]
                self.lights_Entity_objects.append(NS_traffic_Entity)

            elif (r1.name[0] == "E" or r1.name[0] == "W") and r1.name[1] == " ":
                EW_traffic_x = (t["position"]-50) + ((100-self.trafficSystem.road_list[road_index]["length"])/2)
                EW_traffic_Entity = Entity(model='cube', scale=(0.5, 5, 1), color= color.red)
                EW_traffic_Entity.x = EW_traffic_x + 4
                EW_traffic_Entity.y = r1.y
                EW_traffic_Entity.z = -.5
                EW_traffic_Entity.name = t["road"]
                self.lights_Entity_objects.append(EW_traffic_Entity)



    # Initialize intersections
    def initializeIntersections(self):
        for i in self.trafficSystem.intersection_list:
            for j in range(len(self.roads_Entity_objects)):
                r = self.roads_Entity_objects[j]
                
                if (r.name == i[0]["road"]):
                    i_0_entity = j
                if (r.name == i[1]["road"]):
                    i_1_entity = j
            
            r1 = self.roads_Entity_objects[i_0_entity]
            r2 = self.roads_Entity_objects[i_1_entity]
            if (r1.name[0] == "N" or r1.name[0] == "S") and r1.name[1] == " ":
                NS_traffic_position = (r2.y + 50) - ((100 - self.trafficSystem.road_list[i_0_entity]["length"])/2)
                i[0]["position"] = NS_traffic_position
                self.trafficSystem.create_traffic_light_on_road(i[0]["road"], NS_traffic_position, 300, "green")
                NS_traffic_Entity = Entity(model='cube', scale=(5, 0.5, 1), color= color.green)
                NS_traffic_Entity.x = r1.x
                NS_traffic_Entity.y = r2.y + 4
                NS_traffic_Entity.z = -.5
                NS_traffic_Entity.name = i[0]["road"]
                self.lights_Entity_objects.append(NS_traffic_Entity)

                EW_traffic_position = (r1.x + 50) - ((100 - self.trafficSystem.road_list[i_1_entity]["length"])/2)
                i[1]["position"] = EW_traffic_position
                self.trafficSystem.create_traffic_light_on_road(i[1]["road"], EW_traffic_position, 300, "red")
                EW_traffic_Entity = Entity(model='cube', scale=(0.5, 5, 1), color= color.red)
                EW_traffic_Entity.x = r1.x + 4
                EW_traffic_Entity.y = r2.y
                EW_traffic_Entity.z = -.5
                EW_traffic_Entity.name = i[1]["road"]
                self.lights_Entity_objects.append(EW_traffic_Entity)
            
            else:
                print("Error - NS road must come first for each intersection in the XML file")
                sys.exit()



    def initializeBusStop(self):

        #PLACE BUS STOPS
        for t in self.trafficSystem.bus_stop_list:

            for i in range(len(self.roads_Entity_objects)):
                r = self.roads_Entity_objects[i]
                if (r.name == t["road"]):
                    road_index = i
            
            r1 = self.roads_Entity_objects[road_index]
            if (r1.name[0] == "N" or r1.name[0] == "S") and r1.name[1] == " ":
                NS_bus_stop_y = (t["position"]-50) + ((100-self.trafficSystem.road_list[road_index]["length"])/2)
                NS_bus_stop_Entity = Entity(model='cube', scale=(5, 0.5, 1), color= color.white)
                NS_bus_stop_Entity.x = r1.x
                NS_bus_stop_Entity.y = NS_bus_stop_y + 2
                NS_bus_stop_Entity.z = -.5
                NS_bus_stop_Entity.name = t["position"]
                self.bus_stop_Entity_objects.append(NS_bus_stop_Entity)

            elif (r1.name[0] == "E" or r1.name[0] == "W") and r1.name[1] == " ":
                EW_bus_stop_x = (t["position"]-50) + ((100-self.trafficSystem.road_list[road_index]["length"])/2)
                EW_bus_stop_Entity = Entity(model='cube', scale=(0.5, 5, 1), color= color.white)
                EW_bus_stop_Entity.x = EW_bus_stop_x + 2
                EW_bus_stop_Entity.y = r1.y
                EW_bus_stop_Entity.z = -.5
                EW_bus_stop_Entity.name = t["position"]
                self.bus_stop_Entity_objects.append(EW_bus_stop_Entity)



    def initializeVehicles(self):
        for i in range(len(self.trafficSystem.vehicle_list)):
            self.createVehicleEntity(i)



    def createVehicleEntity(self, index):
        available_colors = [color.light_gray, color.green, color.yellow, color.white, color.orange]
        color_random_index = random.randint(0, len(available_colors)-1)
        tsVehicle = self.trafficSystem.vehicle_list[index]
        vehicle = Entity(model='cube', scale=(2, 1, 1), color=available_colors[color_random_index])

        for e in self.roads_Entity_objects:
            if(tsVehicle["road"] == e.name):
                if (tsVehicle["road"][0] == "N" or tsVehicle["road"][0] == "S") and tsVehicle["road"][1] == ' ':
                    positionOnRoad = self.calculateVehiclePosition(e.name, tsVehicle["position"])
                    vehicle.position = (e.x, positionOnRoad)
                    vehicle.rotation = (0,0,90)
                else:
                    positionOnRoad = self.calculateVehiclePosition(e.name, tsVehicle["position"])
                    vehicle.position = (positionOnRoad, e.y)
                    vehicle.rotation = (0,0,180)

                if (tsVehicle["type"] == 'bus'):
                    vehicle.scale = (5,2,1)
                    vehicle.color = color.white
                    vehicle.texture=load_texture(f'textures/bus.png')
                    trigger_box3 = Entity(model='wireframe_cube', color=color.clear, scale=(2, 1, 1), collider='box', add_to_scene_entities=False)

                elif (tsVehicle["type"] == 'fire truck'):
                    vehicle.scale = (6,2,1)
                    vehicle.color = color.red
                    vehicle.texture=load_texture(f'textures/fireTruck.png')
                    trigger_box3 = Entity(model='wireframe_cube', color=color.clear, scale=(2, 1, 1), collider='box', origin_x=.3, add_to_scene_entities=False)

                elif (tsVehicle["type"] == 'police van'):
                    vehicle.scale = (4,1,1)
                    vehicle.color = color.white
                    vehicle.texture=load_texture(f'textures/police.png')
                    trigger_box3 = Entity(model='wireframe_cube', color=color.clear, scale=(2, 1, 1), collider='box', origin_x=.3, add_to_scene_entities=False)

                elif (tsVehicle["type"] == 'car'):
                    vehicle.texture=load_texture(f'textures/car.png')
                    trigger_box3 = Entity(model='wireframe_cube', color=color.clear, scale=(2.75, 1, 1), collider='box', origin_x=.3, add_to_scene_entities=False)


                # Add the car to the list of vehicles
                self.vehicles.append(vehicle)
                trigger_box3.parent = vehicle
                self.triggerboxes.append(trigger_box3)



    def calculateVehiclePosition(self, road, vPosition):
        roadLength = 0
        for r in self.trafficSystem.road_list:
            if (r["name"] == road):
                roadLength = r["length"]
        percentageOfRoad = vPosition / roadLength
        positionOnRoad = percentageOfRoad * 100
        newPosition = -50 + positionOnRoad
        return newPosition



    def removeCarsOutOfBounds(self):
        for i in sorted(self.trafficSystem.to_be_removed, reverse=True):
            destroy(self.vehicles[i])
            del self.vehicles[i]
        
        for i in sorted(self.trafficSystem.to_be_removed, reverse=True):
            destroy(self.triggerboxes[i])
            del self.triggerboxes[i]

        self.trafficSystem.remove_vehicles_off_road()



    def updateCarPositions(self):
        if (len(self.trafficSystem.vehicle_list) > len(self.vehicles)):
            for i in range(len(self.trafficSystem.vehicle_list) - len(self.vehicles)):
                self.createVehicleEntity(i+len(self.vehicles))

        for i in range(len(self.vehicles)):
            v = self.vehicles[i]
            tsVehicle = self.trafficSystem.vehicle_list[i]
            for e in self.roads_Entity_objects:
                if (tsVehicle["road"] == e.name):
                    if (tsVehicle["road"][0] == 'N' or tsVehicle["road"][0] == 'S'):
                        positionOnRoad = self.calculateVehiclePosition(e.name, tsVehicle["position"])
                        v.position = (e.x, positionOnRoad)
                        v.rotation = (0, 0, 90)
                    else:
                        positionOnRoad = self.calculateVehiclePosition(e.name, tsVehicle["position"])
                        v.position = (positionOnRoad, e.y)
                        v.rotation = (0, 0, 180)



    def updateTrafficLights(self):
        for q in range(len(self.lights_Entity_objects)):
            l = self.lights_Entity_objects[q]

            if (self.trafficSystem.trafficlight_current_states[q]["color"] == "green"):
                l.color = color.green
            elif (self.trafficSystem.trafficlight_current_states[q]["color"] == "red"):
                l.color = color.red
            elif (self.trafficSystem.trafficlight_current_states[q]["color"] == "yellow"):
                l.color = color.yellow



    def updateNotifiers(self):
        self.selectedRoadNotifier.text = ("Road:\n"+self.selectedRoad)
        self.selectedPositionNotifier.text = ("Position:\n"+str(self.selectedPosition))

    

    # Create the button
    def on_restart_button_click(self):
        for vehicle in self.vehicles:
            destroy(vehicle)
        for triggerbox in self.triggerboxes:
            destroy(triggerbox)
        for light in self.lights_Entity_objects:
            destroy(light)
        for stop in self.bus_stop_Entity_objects:
            destroy(stop)

        self.vehicles.clear()
        self.triggerboxes.clear()
        self.lights_Entity_objects.clear()
        self.bus_stop_Entity_objects.clear()
        
        self.trafficSystem = VehicleGeneratorSimulation("./InputFiles/prototype2.xml")
        self.initializeVehicles()
        self.initializeTrafficLights()
        self.initializeIntersections()
        self.initializeBusStop()
        


    def on_end_button_click(self):
        sys.exit()
        


    def on_add_vehicle_button_click(self):
        """for newVehicle in addVehicle():
            
            road = newVehicle["name"]
            speed = newVehicle["speed"]
            type = newVehicle["type"]
            position = newVehicle["position"]
            acceleration = newVehicle["acceleration"]

            self.trafficSystem.create_vehicle_on_road(road, position, speed, acceleration, type)
            self.createVehicleEntity(len(self.trafficSystem.vehicle_list)-1)"""
        
        if self.selectedRoad != "":
            road = self.selectedRoad
            roadObstructed = False
            for v in self.trafficSystem.vehicle_list:
                if v["road"] == road and (v["position"] < self.selectedPosition + 4 and v["position"] > self.selectedPosition - 4):
                    roadObstructed = True
                    self.text_message.text = "Road obstructed"
                    invoke(self.clear_error_message, delay=2)
            
            if (not roadObstructed):
                self.trafficSystem.create_vehicle_on_road(road, self.selectedPosition, 10, 1.2, 'bus')
                self.createVehicleEntity(len(self.trafficSystem.vehicle_list)-1)
        else:
            self.text_message.text = "Select a road first"
            invoke(self.clear_error_message, delay=2)
    
    #clear error message on screen
    def clear_error_message(self):
        self.text_message.text = ""
        
    def add_traffic_light_button_click(self):

        store_dup = []
        for i in range(len(self.lights_Entity_objects)):
            found = False
            for j in range(len(store_dup)):
                if store_dup[j][0] == str(self.lights_Entity_objects[i]):
                    store_dup[j][1] += 1
                    found = True
                    break
            if not found:
                store_dup.append([str(self.lights_Entity_objects[i].name), 1])


        store_dup = sorted(store_dup, key=lambda x: x[1], reverse=False)

        if self.selectedRoad != "":
            road = self.selectedRoad
            roadObstructed = False
            for v in store_dup:
                if v[0] == road and v[1]>2:
                    roadObstructed = True
                    self.text_message.text = "Traffic Light Limit Reached"
                    invoke(self.clear_error_message, delay=2)

            if (not roadObstructed):

                if (self.selectedRoad[0] == "N" or self.selectedRoad[0] == "S") and self.selectedRoad[1] == " ":
                            NS_traffic_Entity = Entity(model='cube', scale=(5, 0.5, 1), color= color.green)
                            NS_traffic_Entity.position = self.roadPosition
                            NS_traffic_Entity.z -= 1
                            NS_traffic_Entity.x += 1
                            NS_traffic_Entity.y += 5
                            NS_traffic_Entity.name = self.selectedRoad
                            self.trafficSystem.create_traffic_light_on_road(self.selectedRoad, 55, 300, "green")
                            self.lights_Entity_objects.append(NS_traffic_Entity)

                elif (self.selectedRoad[0] == "E" or self.selectedRoad[0] == "W") and self.selectedRoad[1] == " ":
                            EW_traffic_Entity = Entity(model='cube', scale=(0.5, 5, 1), color= color.red)
                            EW_traffic_Entity.position = self.roadPosition
                            EW_traffic_Entity.z -= 1
                            EW_traffic_Entity.x += 5
                            EW_traffic_Entity.y += 1
                            EW_traffic_Entity.name = self.selectedRoad
                            self.trafficSystem.create_traffic_light_on_road(self.selectedRoad, 55, 300, "green")
                            self.lights_Entity_objects.append(EW_traffic_Entity)
        else:
            self.text_message.text = "Select a road first"
            invoke(self.clear_error_message, delay=2)


    
    def add_bus_stop_button_click(self):
        
        if self.selectedRoad != "":
            road = self.selectedRoad
            roadObstructed = False
            for v in self.trafficSystem.bus_stop_list:
                if v["road"] == road:
                    roadObstructed = True
                    self.text_message.text = "Road already contains bus stop"
                    invoke(self.clear_error_message, delay=2)
            
            if (not roadObstructed):
                if (self.selectedRoad[0] == "N" or self.selectedRoad[0] == "S") and self.selectedRoad[1] == " ":
                    NS_bus_stop = Entity(model='cube', scale=(5, 0.5, 1), color= color.white)
                    NS_bus_stop.position = self.roadPosition
                    NS_bus_stop.z -= 1
                    NS_bus_stop.x += 1
                    NS_bus_stop.y += 3
                    self.trafficSystem.bus_stop_list.append({"road": self.selectedRoad, "position": 50, "waitingtime": 10}) 
                    self.bus_stop_Entity_objects.append(NS_bus_stop)
                    
                elif (self.selectedRoad[0] == "E" or self.selectedRoad[0] == "W") and self.selectedRoad[1] == " ":
                    EW_bus_stop = Entity(model='cube', scale=(0.5, 5, 1), color= color.white)
                    EW_bus_stop.position = self.roadPosition
                    EW_bus_stop.position = self.roadPosition
                    EW_bus_stop.z -= 1
                    EW_bus_stop.x += 3
                    EW_bus_stop.y += 1
                    self.trafficSystem.bus_stop_list.append({"road": self.selectedRoad, "position": 50, "waitingtime": 10})  
                    self.bus_stop_Entity_objects.append(EW_bus_stop)
        else:
            self.text_message.text = "Select a road first"
            invoke(self.clear_error_message, delay=2)
    
    def road_on_click(self):
        roadName = mouse.hovered_entity.name
        self.selectedRoad = roadName
        self.roadPosition = mouse.hovered_entity.position
        print("Click on road: ", roadName)



def update():
    # In each update the vehicle positions and traffic lights will be updated in trafficSystem (Automatic Simulation)
    # Then the vehicle models and traffic lights are updated in ursina to match trafficSystem
    # Other checks are done at different points in the update to remove vehicles that go out of bounds
    graphics.trafficSystem.update()
    graphics.updateCarPositions()
    graphics.removeCarsOutOfBounds()
    graphics.updateTrafficLights()
    graphics.updateNotifiers()



def input(key):
    if key == '0':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 0
    elif key == '1':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 1
    elif key == '2':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 2
    elif key == '3':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 3
    elif key == '4':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 4
    elif key == '5':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 5
    elif key == '6':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 6
    elif key == '7':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 7
    elif key == '8':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 8
    elif key == '9':
        graphics.tempSelectedPosition = graphics.tempSelectedPosition*10 + 9
    elif key == Keys.backspace:
        cur = graphics.tempSelectedPosition
        graphics.tempSelectedPosition = int((cur - (cur % 10)) / 10)
        print(graphics.tempSelectedPosition)
    elif key == Keys.enter:
        graphics.selectedPosition = graphics.tempSelectedPosition
        graphics.tempSelectedPosition = 0



if __name__ == "__main__":
    app = Ursina()
    graphics = Graphics()
    app.run()