from ursina import *
import random
from  AutomaticSimulation import *
import sys
from ursina import text
from VehicleGenerator import addVehicle

app = Ursina()
vehicles = []

trafficSystem = AutomaticSimulation()

# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 90

# create base
box = Entity(model='quad', scale=(120), color=rgb(51,165,50))

# create roads
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
                # Create the object_rec Entity and pass text_entity as a child
                road_model = Entity(model='cube', scale=(4, 100, 0.1), color=color.gray)
                road_model.y = road_position/2   
                road_model.x = road_position*5
                roadText= Text(text=road_name, scale=(15,1))
                roadText.parent = road_model
                roadText.z = -.5
                roadText.y = -.5
                road_model.name = road_name
                
                
            elif (road_name[0] == "E" or road_name[0] == "W") and road_name[1] == " ": # Horizontal Roads
                # Create the object_rec Entity and pass text_entity as a child
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

stopSign1 = Entity(model='sphere', scale=0, color=color.red)
stopSign1.x = 3
stopSign1.y = -3

busStop1 = Entity(model='cube', scale=0, color=color.blue)
busStop1.x = -25
busStop1.y = 23

traffic_light1 = Entity(model='cube', scale=(0, 0, 0), color=color.green)
traffic_light1.x = 0
traffic_light1.y = 25

# PLACE THE TRAFFIC LIGHTS ONTO THE ROADS
lights = trafficSystem.traffic_light_list

for i in range(len(trafficSystem.traffic_light_list)):
# Because we are looking at crossroads/intersections,
# we look at both current index and index+1 of the traffic light list for each iteration    
    # Set the characteristics of the traffic lights
    # We will use green for N/S traffic lights for now and red for E/W
    NS_lightPoles = Entity(model='cube', scale=(3.5, 0.5, 1), color= color.green)
    EW_lightPoles = Entity(model='cube', scale=(0.5, 3.5, 1), color= color.red)

    # Lets take a look at the N/S light of the intersection
    if lights[i]["road"][0] == "N" or lights[i]["road"][0] == "S":
            NSlightpos_x = lights[i]["position"] * 5
            NSlightpos_y = lights[i + 1]["position"] / 2.2
            if NSlightpos_y < 0:
                NSlightpos_y = NSlightpos_y - 5
            NS_lightPoles.position = (NSlightpos_x, NSlightpos_y)
    # Now lets take a look at the E/W light of the intersection
    if lights[i+1]["road"][0] == "W" or lights[i+1]["road"][0] == "E":
        EWlightpos_x = lights[i + 1]["position"] / 1.8
        EWlightpos_y = lights[i]["position"] * 5
        if EWlightpos_x > 0:
            EWlightpos_x -= 5
        EW_lightPoles.position = (EWlightpos_x, EWlightpos_y)

    i += 1 # increment to get to the next intersection

    # We need this so we don't go out of bounds
    if i == len(lights) - 1:
        break
    

#Loop through vehicle list to spawn cars and set attributes 
def createCars():
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


createCars()


# Define a function to move the cars
def update():
    traffic_light_time = time.time() % 16 # repeat cycle every 16 seconds
    
   #  trafficSystem.update()

    if traffic_light_time < 7:
        traffic_light1.color = color.green
    elif traffic_light_time < 9:
        traffic_light1.color = color.yellow
    else:
        traffic_light1.color = color.red
    
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
    createCars()
    
def on_button_click():
    # access addvehicle from vehiclegenerator and assign vehicle properties
    newVehicle = addVehicle()
    vehicleType = newVehicle["type"]
    vehicleRoad = newVehicle["name"]
    #vehicleSpeed = newVehicle["speed"]
    #vehiclePosition = newVehicle["position"]
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