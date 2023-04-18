from ursina import *
import random
from  AutomaticSimulation import *
import sys
from ursina import text
from VehicleGenerator import addVehicle
import random

app = Ursina()
vehicles = []
trafficLightsNS = []
trafficLightsEW = []
trafficSystem = AutomaticSimulation()
triggerboxes = []

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

# stopSign1 = Entity(model='sphere', scale=0, color=color.red)
# stopSign1.x = 3
# stopSign1.y = -3

# busStop1 = Entity(model='cube', scale=0, color=color.blue)
# busStop1.x = -25
# busStop1.y = 23

# traffic_light1 = Entity(model='cube', scale=(0, 0, 0), color=color.green)
# traffic_light1.x = 0
# traffic_light1.y = 25

# PLACE THE TRAFFIC LIGHTS ONTO THE ROADS
lights = trafficSystem.traffic_light_list

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
    


def create_vehicle_entity(speed, car_type, road, position):
    available_colors = [color.brown, color.blue, color.magenta, color.yellow, color.white, color.black, color.orange]
    color_random_index = random.randint(0, len(available_colors)-1)
    car = Entity(model='cube', scale=(2, 1, 1), color=available_colors[color_random_index])
    car.collider = 'box'
    car.speed = speed / 100
    car.originalSpeed = car.speed
    car.type = car_type
    car.road = road
    car.pos = position

    # This iteration implementation will make sure that the vehicle is on the assigned road (When there are more than 2 vehicles on the assigned road)
    for i in range(len(roads_Entity_objects)):
        if(car.road == roads_name_check_duplicate[i]):
            if (car.road[0] == "N" or car.road[0] == "S") and car.road[1] == " ":
                car.is_on_y_axis = True
                car.position = (roads_Entity_objects[i].x, car.pos)
                car.rotation = (0, 0, 90)
            else:
                car.is_on_y_axis = False
                car.position = (car.pos, roads_Entity_objects[i].y)

            trigger_box3 = Entity(model='wireframe_cube', color=color.white, scale=(4, 1, 1), collider='box', origin_y=0)
            trigger_box3.parent = car
            triggerboxes.append(trigger_box3)
            # Add the car to the list of vehicles
            vehicles.append(car)

# Loop through vehicle list to spawn cars and set attributes 
def createCars(type):
    if "default" == type:

        for i in range(len(trafficSystem.vehicle_list)):
            # Get the vehicle properties from the list
            vehicle_props = trafficSystem.vehicle_list[i]
            # Create a new car entity with the properties
            create_vehicle_entity(vehicle_props["speed"], vehicle_props["type"], vehicle_props["road"], vehicle_props["position"])

    elif "add" == type:
        newVehicle = addVehicle()
        # print(newVehicle)
        create_vehicle_entity(newVehicle[0]["speed"], newVehicle[0]["type"], newVehicle[0]["name"], newVehicle[0]["position"])



createCars("default")

# Define a function to move the cars
def update():
    traffic_light_time = time.time() % 16 # repeat cycle every 16 seconds
    
    #change light colors for North/South roads
    for NS_lightPoles in trafficLightsNS:
        if traffic_light_time < 8:
            NS_lightPoles.color = color.green
        elif traffic_light_time < 10:
            NS_lightPoles.color = color.yellow
        else:
            NS_lightPoles.color = color.red
            
    #change light colors for East/West roads
    #these should oppose the lights on N/W roads    
    if traffic_light_time < 10:
        for EW_lightPoles in trafficLightsEW:
            EW_lightPoles.color = color.red
    elif traffic_light_time < 13:
        for EW_lightPoles in trafficLightsEW:
            EW_lightPoles.color = color.green
            #for vehicle in vehicles:
                #if vehicle.is_on_y_axis == False:
                    #vehicle.speed = .1
    elif traffic_light_time < 15:
        for EW_lightPoles in trafficLightsEW:
            EW_lightPoles.color = color.yellow
            
    for vehicle in vehicles:
        #loop through the car's trigger boxes and check if they are colliding with a light that is red or yellow, then adjust speed
        for triggerbox in triggerboxes:
            for lightNS in trafficLightsNS:
                if (lightNS.intersects(triggerbox) and vehicle.intersects(triggerbox) and lightNS.color == color.green):
                    vehicle.speed = vehicle.originalSpeed
                if lightNS.intersects(triggerbox) and vehicle.intersects(triggerbox) and lightNS.color == color.red:
                    vehicle.speed = max(0,vehicle.speed - .008)
                if lightNS.intersects(triggerbox) and vehicle.intersects(triggerbox) and lightNS.color == color.yellow:
                    vehicle.speed = max(0, vehicle.speed - .008)
            for lightEW in trafficLightsEW:
                if (lightEW.intersects(triggerbox) and vehicle.intersects(triggerbox) and lightEW.color == color.green):
                    vehicle.speed = vehicle.originalSpeed
                if lightEW.intersects(triggerbox) and vehicle.intersects(triggerbox) and lightEW.color == color.red:
                    vehicle.speed = max(0, vehicle.speed - .008)
                if lightEW.intersects(triggerbox) and vehicle.intersects(triggerbox) and lightEW.color == color.yellow:
                    vehicle.speed = max(0, vehicle.speed - .008)
        if vehicle.is_on_y_axis:
            vehicle.y += vehicle.speed
            if vehicle.y > 49:
                vehicle.y = -49
        else:
            vehicle.x += vehicle.speed
            if vehicle.x > 49:
                vehicle.x = -49

# Create the button
def add_vehicle():
    # Define code to add a vehicle here
    pass

def on_restart_button_click():
    reset_program()
    createCars("default")
    
def on_end_button_click():
    app.quit()
    
def on_button_click():
    createCars("add")
    
def reset_program():
    # Reset the initial state of the program
    global vehicles
    global triggerboxes
    for vehicle in vehicles:
        destroy(vehicle)
    for triggerbox in triggerboxes:
        destroy(triggerbox)
    vehicles = [] 
    triggerboxes = []
    

button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.50, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_button_click)
restartButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.38, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_restart_button_click)
endButton = Button(text='End\nSimulation', color=rgb(128, 0, 0), highlight_color=color.red, position=(0.62, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_end_button_click)
app.run()
