from ursina import *
import random
from SimulationWVehicleGenerator import VehicleGeneratorSimulation
from TrafficLightSimulation import *
import sys
from ursina import text
#from VehicleGenerator import addVehicle
import random


app = Ursina()
trafficSystem = VehicleGeneratorSimulation("./InputFiles/prototype2.xml")
# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 90

# create base
box = Entity(model='quad', scale=(120))
box.texture=load_texture(f'textures/desert.png')

vehicles = []
triggerboxes = []
trafficLightsNS = []
trafficLightsEW = []

# create roads
roads_Entity_objects = [] # list of road entities

num_NS_roads = 0
num_EW_roads = 0

# create road entities and calculate the number of NS and EW roads
for r in trafficSystem.road_list:
    if (r["name"][0] == "N" or r["name"][0] == "S") and r["name"][1] == " ":
        num_NS_roads += 1
        road_model = Entity(model='cube', scale=(4, r["length"], 0.1), color=color.gray)
        road_model.name = r["name"]
        roads_Entity_objects.append(road_model)

    elif (r["name"][0] == "E" or r["name"][0] == "W") and r["name"][1] == " ":
        num_EW_roads += 1
        road_model = Entity(model='cube', scale=(r["length"], 4, 0.1), color=color.gray)
        road_model.name = r["name"]
        roads_Entity_objects.append(road_model)
    
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

for i in range(len(trafficSystem.road_list)):
    r = trafficSystem.road_list[i]
    e = roads_Entity_objects[i]
    if (r["name"][0] == "N" or r["name"][0] == "S") and r["name"][1] == " ":
        current_spacing_NS += spacing_NS
        e.x = current_spacing_NS
        e.y = 0
        roadText= Text(text=r["name"], scale=(20,1), color=color.black)
        roadText.parent = road_model
        roadText.x = (e.x / (2*num_NS_roads)) - 5
        roadText.y = -.5
        roadText.z = -2

    elif (r["name"][0] == "E" or r["name"][0] == "W") and r["name"][1] == " ":
        current_spacing_EW += spacing_EW
        e.y = current_spacing_EW
        e.x = 0
        roadText= Text(text=r["name"], scale=(20,1), color=color.black)
        roadText.parent = road_model
        roadText.x = -15
        roadText.y = (e.y / (50*num_EW_roads)) - .02
        roadText.z = -2

# Initialize traffic lights
lights_Entity_objects = [] # list of traffic light entities
for t in trafficSystem.traffic_light_list:
    for i in range(len(roads_Entity_objects)):
        r = roads_Entity_objects[i]
        if (r.name == t["road"]):
            road_index = i
    
    r1 = roads_Entity_objects[road_index]
    if (r1.name[0] == "N" or r1.name[0] == "S") and r1.name[1] == " ":
        NS_traffic_y = (t["position"]-50) + ((100-trafficSystem.road_list[road_index]["length"])/2)
        NS_traffic_Entity = Entity(model='sphere', scale=(1, 1, 1), color= color.green)
        NS_traffic_Entity.x = r1.x
        NS_traffic_Entity.y = NS_traffic_y + 2
        NS_traffic_Entity.name = t["position"]
        lights_Entity_objects.append(NS_traffic_Entity)

    elif (r1.name[0] == "E" or r1.name[0] == "W") and r1.name[1] == " ":
        EW_traffic_x = (t["position"]-50) + ((100-trafficSystem.road_list[road_index]["length"])/2)
        EW_traffic_Entity = Entity(model='sphere', scale=(1, 1, 1), color= color.green)
        EW_traffic_Entity.x = EW_traffic_x + 2
        EW_traffic_Entity.y = r1.y
        EW_traffic_Entity.name = t["position"]
        lights_Entity_objects.append(EW_traffic_Entity)



# Initialize intersections
for i in trafficSystem.intersection_list:
    for j in range(len(roads_Entity_objects)):
        r = roads_Entity_objects[j]
        if (r.name == i[0]["road"]):
            i_0_entity = j
        if (r.name == i[1]["road"]):
            i_1_entity = j
    
    r1 = roads_Entity_objects[i_0_entity]
    r2 = roads_Entity_objects[i_1_entity]
    if (r1.name[0] == "N" or r1.name[0] == "S") and r1.name[1] == " ":
        NS_traffic_position = (r2.y + 50) - ((100 - trafficSystem.road_list[i_0_entity]["length"])/2)
        i[0]["position"] = NS_traffic_position
        trafficSystem.create_traffic_light_on_road(i[0]["road"], NS_traffic_position, 200, "green")
        NS_traffic_Entity = Entity(model='sphere', scale=(1, 1, 1), color= color.green)
        NS_traffic_Entity.x = r1.x
        NS_traffic_Entity.y = r2.y + 2
        NS_traffic_Entity.name = i[0]["road"]
        lights_Entity_objects.append(NS_traffic_Entity)

        EW_traffic_position = (r1.x + 50) - ((100 - trafficSystem.road_list[i_1_entity]["length"])/2)
        i[1]["position"] = EW_traffic_position
        trafficSystem.create_traffic_light_on_road(i[1]["road"], EW_traffic_position, 200, "red")
        EW_traffic_Entity = Entity(model='sphere', scale=(1, 1, 1), color= color.red)
        EW_traffic_Entity.x = r1.x + 2
        EW_traffic_Entity.y = r2.y
        NS_traffic_Entity.name = i[1]["road"]
        lights_Entity_objects.append(EW_traffic_Entity)
    
    else:
        print("Error - NS road must come first for each intersection in the XML file")
        sys.exit()
    
busStops = trafficSystem.bus_stop_list
#PLACE BUS STOPS
for i in range(0, len(busStops)):
    print("BUSSSTOPS", busStops)
    busStop1 = Entity(model='cube', scale=(3.5, 0.5, 1), color= color.blue)
    busStop1.collider = 'box'
    busStop1.position = 2
    #INCOMPLETE

def calculateVehiclePosition(road, vPosition):
    roadLength = 0
    for r in trafficSystem.road_list:
        if (r["name"] == road):
            roadLength = r["length"]
    percentageOfRoad = vPosition / roadLength
    positionOnRoad = percentageOfRoad * 100
    newPosition = -50 + positionOnRoad
    return newPosition

def createVehicleEntity(index):
    available_colors = [color.brown, color.blue, color.magenta, color.yellow, color.white, color.black, color.orange]
    color_random_index = random.randint(0, len(available_colors)-1)
    tsVehicle = trafficSystem.vehicle_list[index]
    vehicle = Entity(model='cube', scale=(2, 1, 1), color=available_colors[color_random_index])
    for e in roads_Entity_objects:
        if(tsVehicle["road"] == e.name):
            if (tsVehicle["road"][0] == "N" or tsVehicle["road"][0] == "S") and tsVehicle["road"][1] == " ":
                positionOnRoad = calculateVehiclePosition(e.name, tsVehicle["position"])
                vehicle.position = (e.x, positionOnRoad)
                vehicle.rotation = (0, 0, 90)
            else:
                positionOnRoad = calculateVehiclePosition(e.name, tsVehicle["position"])
                vehicle.position = (positionOnRoad, e.y)
                vehicle.rotation = (0, 0, 180)

            trigger_box3 = Entity(model='wireframe_cube', color=color.white, scale=(2.75, 1, 1), collider='box', origin_x=.3)
            trigger_box3.parent = vehicle
            triggerboxes.append(trigger_box3)
            # Add the car to the list of vehicles
            vehicles.append(vehicle)
        if (tsVehicle["type"] == 'bus'):
            vehicle.scale = (2,2,1)
            vehicle.color = color.blue

def initializeVehicles():
    for i in range(len(trafficSystem.vehicle_list)):
        createVehicleEntity(i)

def removeCarsOutOfBounds():
    for i in sorted(trafficSystem.to_be_removed, reverse=True):
        destroy(vehicles[i])
        del vehicles[i]
    
    for i in sorted(trafficSystem.to_be_removed, reverse=True):
        destroy(triggerboxes[i])
        del triggerboxes[i]

    trafficSystem.remove_vehicles_off_road()

def updateCarPositions():
    for i in range(len(vehicles)):
        v = vehicles[i]
        tsVehicle = trafficSystem.vehicle_list[i]
        for e in roads_Entity_objects:
            if (tsVehicle["road"] == e.name):
                if (tsVehicle["road"][0] == 'N' or tsVehicle["road"][0] == 'S'):
                    positionOnRoad = calculateVehiclePosition(e.name, tsVehicle["position"])
                    v.position = (e.x, positionOnRoad)
                    v.rotation = (0, 0, 90)
                else:
                    positionOnRoad = calculateVehiclePosition(e.name, tsVehicle["position"])
                    v.position = (positionOnRoad, e.y)
                    v.rotation = (0, 0, 180)

def updateTrafficLights():
    for q in range(len(lights_Entity_objects)):
        l = lights_Entity_objects[q]
        
        if (trafficSystem.trafficlight_current_states[q]["color"] == "green"):
            l.color = color.green
        elif (trafficSystem.trafficlight_current_states[q]["color"] == "red"):
            l.color = color.red
        elif (trafficSystem.trafficlight_current_states[q]["color"] == "yellow"):
            l.color = color.yellow


# Places initial cars onto roads
initializeVehicles()

# Define a function to move the cars
def update():
    # In each update the vehicle positions and traffic lights will be updated in trafficSystem (Automatic Simulation)
    # Then the vehicle models and traffic lights are updated in ursina to match trafficSystem
    # Other checks are done at different points in the update to remove vehicles that go out of bounds
    trafficSystem.update()
    removeCarsOutOfBounds()
    updateCarPositions()
    updateTrafficLights()

# Create the button
def on_restart_button_click():
    global vehicles
    global triggerboxes
    for vehicle in vehicles:
        destroy(vehicle)
    for triggerbox in triggerboxes:
        destroy(triggerbox)

    vehicles = []
    triggerboxes = []
    
    global trafficSystem
    trafficSystem = VehicleGeneratorSimulation("./InputFiles/prototype2.xml")
    initializeVehicles()

    
def on_end_button_click():
    sys.exit()
    
def on_add_vehicle_button_click():
    road = random.choice(trafficSystem.road_list)["name"]
    trafficSystem.create_vehicle_on_road(road, 0, 50, 1.2, 'car')
    createVehicleEntity(len(trafficSystem.vehicle_list)-1)
    

button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.50, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_add_vehicle_button_click)
restartButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.38, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_restart_button_click)
endButton = Button(text='End\nSimulation', color=rgb(128, 0, 0), highlight_color=color.red, position=(0.62, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_end_button_click)
app.run()