from ursina import *
import random
from SimulationWVehicleGenerator import VehicleGeneratorSimulation
from TrafficLightSimulation import *
import sys
from ursina import text
#from VehicleGenerator import addVehicle
import random


app = Ursina()
vehicles = []
trafficLightsNS = []
trafficLightsEW = []
trafficSystem = VehicleGeneratorSimulation("")
triggerboxes = []
triggerboxesRoadsNS = []
triggerboxesRoadsEW = []
# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 90

# create base
box = Entity(model='quad', scale=(120), color=rgb(51,165,50))


# create roads
roads_name_check_duplicate = []
roads_Entity_objects = []

for i in range(len(trafficSystem.intersection_list)):
    for j in range(len(trafficSystem.intersection_list[i])):

        road_name = trafficSystem.intersection_list[i][j]["road"]

        check_duplicate = False
        for k in range(len(roads_name_check_duplicate)):
             if(roads_name_check_duplicate[k] == road_name):
                 check_duplicate = True

        
        if(check_duplicate == False):

            roads_name_check_duplicate.append(road_name)
            road_position = trafficSystem.intersection_list[i][j]["position"]

            if (road_name[0] == "N" or road_name[0] == "S") and road_name[1] == " ":  # Verticle Roads
                # Create the object_rec Entity and pass text_entity as a child
                road_model = Entity(model='cube', scale=(4, 100, 0.1), color=color.gray)
                trigger_box_road1 = Entity(model='wireframe_cube', color=color.white, scale=(.05, 1, 1), collider='box', origin_x=8)
                trigger_box_road1.parent = road_model
                #add trigger box to list of NS roads triggers
                triggerboxesRoadsNS.append(trigger_box_road1)
                road_model.y = road_position/2   
                road_model.x = road_position*5
                roadText= Text(text=road_name, scale=(15,1))
                roadText.parent = road_model
                roadText.z = -.5
                roadText.y = -.5
                road_model.name = road_name
                roads_Entity_objects.append(road_model)
                
                
            elif (road_name[0] == "E" or road_name[0] == "W") and road_name[1] == " ": # Horizontal Roads
                # Create the object_rec Entity and pass text_entity as a child
                road_model = Entity(model='cube', scale=(100, 4, 0.1), color=color.gray)
                trigger_box_road2 = Entity(model='wireframe_cube', color=color.white, scale=(1, .05, 1), collider='box', origin_y=8)
                trigger_box_road2.parent = road_model
                triggerboxesRoadsEW.append(trigger_box_road2)
                road_model.y = road_position/2
                roadText= Text(text=road_name, scale=(1,15))
                roadText.parent = road_model
                roadText.z = -2
                roadText.y = -.5
                roads_Entity_objects.append(road_model)

            else:
                print("Please Declair N|S|E|W in the", trafficSystem.file_name, "input file")
                # Terminate the program without specifying an exit code
                sys.exit()


# PLACE THE TRAFFIC LIGHTS ONTO THE ROADS
lights = trafficSystem.traffic_light_list
busStops = trafficSystem.bus_stop_list

for i in range(0, len(lights)-1, 2):
# Because we are looking at crossroads/intersections,
# we look at both current index and index+1 of the traffic light list for each iteration    
    # Set the characteristics of the traffic lights
    # We will use green for N/S traffic lights for now and red for E/W
    
    NS_lightPoles = Entity(model='cube', scale=(3.5, 0.5, 1), color= color.green)
    NS_lightPoles.collider = 'box'
    
    EW_lightPoles = Entity(model='cube', scale=(0.5, 3.5, 1), color= color.red)
    EW_lightPoles.collider = 'box'
   
    # Lets take a look at the N/S light of the intersection
    if lights[i]["road"][0] == "N" or lights[i]["road"][0] == "S":
        NSlightpos_x = lights[i]["position"] * 5
        NSlightpos_y = lights[i + 1]["position"] / 2.2
        if NSlightpos_y < 0:
            NSlightpos_y = NSlightpos_y - 5
        NS_lightPoles.position = (NSlightpos_x, NSlightpos_y)
            
            #triggerboxes.append(trigger_box1)
        trafficLightsNS.append(NS_lightPoles)
    # Now lets take a look at the E/W light of the intersection
    if lights[i+1]["road"][0] == "W" or lights[i+1]["road"][0] == "E":
        EWlightpos_x = lights[i + 1]["position"] / 1.8
        EWlightpos_y = lights[i]["position"] * 5
        if EWlightpos_x > 0:
            EWlightpos_x -= 5
        EW_lightPoles.position = (EWlightpos_x, EWlightpos_y)
        #add light to list of lights
        trafficLightsEW.append(EW_lightPoles)
    i += 1 # increment to get to the next intersection

    # We need this so we don't go out of bounds
    if i == len(lights) - 1:
        break
    
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
    for i in range(len(roads_Entity_objects)):
        if(tsVehicle["road"] == roads_name_check_duplicate[i]):
            if (tsVehicle["road"][0] == "N" or tsVehicle["road"][0] == "S") and tsVehicle["road"][1] == " ":
                positionOnRoad = calculateVehiclePosition(roads_name_check_duplicate[i], tsVehicle["position"])
                vehicle.position = (roads_Entity_objects[i].x, positionOnRoad)
                vehicle.rotation = (0, 0, 90)
            else:
                positionOnRoad = calculateVehiclePosition(roads_name_check_duplicate[i], tsVehicle["position"])
                vehicle.position = (positionOnRoad, roads_Entity_objects[i].y)
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
        for j in range(len(roads_Entity_objects)):
            if (tsVehicle["road"] == roads_name_check_duplicate[j]):
                if (tsVehicle["road"][0] == 'N' or tsVehicle["road"][0] == 'S'):
                    positionOnRoad = calculateVehiclePosition(roads_name_check_duplicate[j], tsVehicle["position"])
                    v.position = (roads_Entity_objects[j].x, positionOnRoad)
                    v.rotation = (0, 0, 90)
                else:
                    positionOnRoad = calculateVehiclePosition(roads_name_check_duplicate[j], tsVehicle["position"])
                    v.position = (positionOnRoad, roads_Entity_objects[j].y)
                    v.rotation = (0, 0, 180)

def updateTrafficLights():
    for i in range(len(trafficLightsNS)):
        pass # TODO: implement traffic light update

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
    trafficSystem = VehicleGeneratorSimulation("")
    initializeVehicles()

    
def on_end_button_click():
    app.quit()
    
def on_add_vehicle_button_click():
    road = random.choice(trafficSystem.road_list)["name"]
    trafficSystem.create_vehicle_on_road(road, 0, 50, 1.2, 'car')
    createVehicleEntity(len(trafficSystem.vehicle_list)-1)
    

button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.50, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_add_vehicle_button_click)
restartButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.38, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_restart_button_click)
endButton = Button(text='End\nSimulation', color=rgb(128, 0, 0), highlight_color=color.red, position=(0.62, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_end_button_click)
app.run()