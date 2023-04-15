from ursina import *
import random
from  AutomaticSimulation import *
import sys
from ursina import text
from VehicleGenerator import *

app = Ursina()
vehicles = []

trafficSystem = AutomaticSimulation()
newVehicleGen = VehicleGenerator()

# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 90

# create base
box = Entity(model='quad', scale=(120), color=rgb(51,165,50))

# CREATE ROADS
roads_name = []
for i in range(len(trafficSystem.intersection_list)):
    for j in range(len(trafficSystem.intersection_list[i])):

        road_name = trafficSystem.intersection_list[i][j]["road"]

        check_duplicate = False
        for k in range(len(roads_name)):
             if(roads_name[k] == road_name):
                 check_duplicate = True

        
        if(check_duplicate == False):

            roads_name.append(road_name)
            road_position = trafficSystem.intersection_list[i][j]["position"]
            
            print(road_name)
            print(road_position)

            if (road_name[0] == "N" or road_name[0] == "S") and road_name[1] == " ":  # Verticle Roads
                # Create the road_model Entity and pass roadText as a parent
                road_model = Entity(model='cube', scale=(4, 100, 0.1), color=color.gray)
                road_model.y = road_position/2   
                road_model.x = road_position*5
                roadText= Text(text=road_name, scale=(15,1))
                roadText.parent = road_model
                roadText.z = -.5
                roadText.y = -.5
                road_model.name = road_name
                
                
            elif (road_name[0] == "E" or road_name[0] == "W") and road_name[1] == " ": # Horizontal Roads
                # Create the road_model Entity and pass roadText as a parent
                road_model = Entity(model='cube', scale=(100, 4, 0.1), color=color.gray)
                road_model.y = road_position/2
                roadText= Text(text=road_name, scale=(1,15))
                roadText.parent = road_model
                roadText.z = -2
                roadText.y = -.5

            else:
                print("Please Declair N|S|E|W in the", trafficSystem.file_name, "input file")
                # Terminate the program without specifying an exit code
                sys.exit()



# # CREATE TRAFFICLIGHTS

traffic_light_NS_objects = []
cycle_light_NS_objects = []
traffic_light_EW_objects = []
cycle_light_EW_objects = []


for i in range(len(trafficSystem.traffic_light_list)):
# Because we are looking at crossroads/intersections,
# we look at both current index and index+1 of the traffic light list for each iteration    
    # Set the characteristics of the traffic lights
    # We will use green for N/S traffic lights for now and red for E/W

    current_light = trafficSystem.traffic_light_list[i]
    next_light = trafficSystem.traffic_light_list[i+1]


    # Lets take a look at the N/S light of the intersection
    if (current_light["road"][0] == "N" or current_light["road"][0] == "S") and current_light["road"][1] == " ":

        temp_current = []

        NS_lightPoles = Entity(model='cube', scale=(3.5, 0.5, 1), color= color.green)
        NSlightpos_x = current_light["position"] * 5
        NSlightpos_y = next_light["position"] / 2.2
        if NSlightpos_y < 0:
            NSlightpos_y = NSlightpos_y - 5
        NS_lightPoles.position = (NSlightpos_x, NSlightpos_y)

        traffic_light_NS_objects.append(NS_lightPoles)
        cycle_light_NS_objects.append(current_light["cycle"])

    # Now lets take a look at the E/W light of the intersection
    if (next_light["road"][0] == "E" or next_light["road"][0] == "W") and next_light["road"][1] == " ":

        EW_lightPoles = Entity(model='cube', scale=(0.5, 3.5, 1), color= color.red)
        EWlightpos_x = next_light["position"] / 1.8
        EWlightpos_y = current_light["position"] * 5
        if EWlightpos_x > 0:
            EWlightpos_x -= 5
        EW_lightPoles.position = (EWlightpos_x, EWlightpos_y)

        traffic_light_EW_objects.append(EW_lightPoles)
        cycle_light_EW_objects.append(next_light["cycle"])
        

    i += 1 # increment to get to the next intersection

    # We need this so we don't go out of bounds
    if (i) == len(trafficSystem.traffic_light_list) - 1:
        break



def signal_light_color_change(index, trafficlightDirection, color_indicator, cycle):

    print("-----CYCLE---->", cycle[index])
    print("-----COLOR---->", color_indicator)

    if(color_indicator == "red"):
        trafficlightDirection[index] = color.red

    elif(color_indicator == "yellow"):
        trafficlightDirection[index].color = color.yellow

    elif(color_indicator == "green"):
        trafficlightDirection[index] = color.green


#Loop through vehicle list to spawn cars and set attributes 

for i in range(len(trafficSystem.vehicle_list)):
    # Get the vehicle properties from the list
    vehicle_props = trafficSystem.vehicle_list[i]

    # Create a new car entity with the properties
    available_colors = [color.brown, color.blue, color.magenta, color.yellow, color.white, color.black, color.orange]
    car = Entity(model='cube', scale=(2, 1, 1), color=available_colors[i])
    car.speed = vehicle_props["speed"] / 100

    #car.acceleration = vehicle_props["acceleration"] / 100
    car.type = vehicle_props["type"]
    car.road = vehicle_props["road"]
    car.pos = vehicle_props["position"]
    if (car.road[0] == "N" or car.road[0] == "S") and car.road[1] == " ":
        car.is_on_y_axis = True
        car.position = (road_model.x, car.pos)
    else:
        car.is_on_y_axis = False
        car.position = (road_model.y, car.pos)
    
    # Add the car to the list of vehicles
    vehicles.append(car)

# Define a function to move the cars
def update():
    traffic_light_time = time.time() % 16 # repeat cycle every 16 seconds


    # if traffic_light_time < 7:
    #     traffic_light1.color = color.green
    # elif traffic_light_time < 9:
    #     traffic_light1.color = color.yellow
    # else:
    #     traffic_light1.color = color.red

    signal_light_color_change(2, traffic_light_NS_objects, "yellow", cycle_light_NS_objects)
    signal_light_color_change(2, traffic_light_EW_objects, "yellow", cycle_light_EW_objects)
    
    for vehicle in vehicles:
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
    
def on_button_click():
    # access addvehicle from vehiclegenerator and assign vehicle properties
    newVehicleGen.getVehicle()
    vehicleRoad = newVehicleGen.vehicles
    
    # Create a new vehicle entity based on vehicle properties
    available_colors = [color.red, color.green, color.blue, color.yellow, color.orange, color.cyan] # list of available colors
    vehicle = Entity(model='cube', scale=(2, 1, 1), color=random.choice(available_colors)) # choose a random color from the list
    if (vehicleRoad[0] == "N" or vehicleRoad[0] == "S") and vehicleRoad[1] == " ":
        vehicle.is_on_y_axis = True
    else:
        vehicle.is_on_y_axis = False
    vehicle.speed = .5
   
    vehicles.append(vehicle)
    # Make the new vehicle visible
    vehicle.visible = True
    
def reset_program():
    # Reset the initial state of the program
    global vehicles
    for vehicle in vehicles:
        destroy(vehicle)
    vehicles = [] 
    
button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.65, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_button_click)
restartButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.40, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_restart_button_click)

app.run()