from ursina import *
import random

app = Ursina()
vehicles = []

# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 70

# create base
box = Entity(model='quad', scale=100, color=rgb(51,165,50))

# create roads
road1 = Entity(model='cube', scale=(100, 4, 0.1), color=color.gray)
road1.y = -0.5

road2 = Entity(model='cube', scale=(100, 4, 0.1), color=color.gray)
road2.y = 20

road3 = Entity(model='cube', scale=(4, 100, 0.1), color=color.gray)
road3.y = 0

stopSign1 = Entity(model='sphere', scale=1, color=color.red)
stopSign1.x = 3
stopSign1.y = -3

busStop1 = Entity(model='cube', scale=1, color=color.blue)
busStop1.x = -25
busStop1.y = 23

traffic_light1 = Entity(model='cube', scale=(1, 3, 1), color=color.green)
traffic_light1.x = 0
traffic_light1.y = 22



# Create cars
car = Entity(model='cube', scale=(2, 1, 1), color=color.red)
car.x = -20
car.collider = 'box'

car2 = Entity(model='cube', scale=(2, 1, 1), color=color.blue)
car2.y = 20
car2.x = -20
car2.collider = 'box'

car3 = Entity(model='cube', scale=(1, 2, 1), color=color.yellow)
car3.y = 30
car3.x = 0
car3.collider = 'box'

car_positions = [car.position, car2.position, car3.position]
# Define a function to move the cars
def update():
    traffic_light_time = time.time() % 16 # repeat cycle every 16 seconds
    if traffic_light_time < 7:
        traffic_light1.color = color.green
    elif traffic_light_time < 9:
        traffic_light1.color = color.yellow
    else:
        traffic_light1.color = color.red
    car.x += 0.1 #car speed
    if car.x > 49: #when car needs to reset
        car.x = -49
    car2.x += 0.2 
    if car2.x > 48:  
        car2.x = -48
    car3.y += 0.1
    if car3.y > 49:  
        car3.y = -49
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

def on_button_click():
    # Choose a random car position
    
    car_position = random.choice(car_positions)

    # Create a new vehicle entity
    available_colors = [color.red, color.green, color.blue, color.yellow, color.orange, color.cyan] # list of available colors
    vehicle = Entity(model='cube', scale=(2, 1, 1), color=random.choice(available_colors)) # choose a random color from the list
    
    
    if car_position == car_positions[2]:
        vehicle.rotation = (0, 0, 90)
        vehicle.is_on_y_axis = True
    else:
        vehicle.is_on_y_axis = False
        
    # Set the position of the new vehicle to the chosen car position
    vehicle.position = car_position
    
    vehicle.speed = random.uniform(0.05, 0.2) # set a random speed between 0.05 and 0.2
    
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
startButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.40, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_button_click)

app.run()