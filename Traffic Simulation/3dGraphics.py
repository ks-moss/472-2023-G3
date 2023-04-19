import time 
from ursina import *
from  AutomaticSimulation import *
from ursina import text
from FunctionCallSimulation import *
from VehicleGenerator import addVehicle

app = Ursina()

trafficSystem = AutomaticSimulation()
busStopsEntityModels = []
# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 90
# Create Base
box = Entity(model='quad', scale=(120))
box.texture=load_texture(f'textures/desert.png')
# Create Roads
roads_name_duplicate_lists, roads_Entity_objects, triggerboxesRoadsNS, triggerboxesRoadsEW = create_roads(trafficSystem)
# Create Teaffic Lights
trafficLightsNS, trafficLightsEW, busStopsEntity = place_traffic_lights_and_bus_stops(trafficSystem, roads_Entity_objects)    
        
vehicles = []
triggerboxes = []
# Loop through vehicle list to spawn cars and set attributes 
def createCars(type):
    if "default" == type:

        vehicles.clear
        triggerboxes.clear

        for i in range(len(trafficSystem.vehicle_list)):
            # Get the vehicle properties from the list
            speed = trafficSystem.vehicle_list[i]["speed"]
            type = trafficSystem.vehicle_list[i]["type"]
            road = trafficSystem.vehicle_list[i]["road"]
            position = trafficSystem.vehicle_list[i]["position"]
            # Create a new car entity with the properties
            create_vehicle_entity(speed, type, road, position, roads_Entity_objects, roads_name_duplicate_lists, vehicles, triggerboxes)

    elif "add" == type:

        newVehicle = addVehicle()
        
        for i in range(len(newVehicle)):
            # Get the vehicle properties from the list
            speed = newVehicle[i]["speed"]
            type = newVehicle[i]["type"]
            name = newVehicle[i]["name"]
            position = newVehicle[i]["position"]
            # Create a new car entity with the properties
            create_vehicle_entity(speed, type, name, position, roads_Entity_objects, roads_name_duplicate_lists, vehicles, triggerboxes)
    

createCars("default")

timePassed = 0

# Define a function to move the cars
def update():

    traffic_light_time = time.time() % 16 # repeat cycle every 16 seconds

    change_NS_lights(trafficLightsNS, traffic_light_time)
    change_EW_lights(trafficLightsEW, traffic_light_time)
    
    for vehicle in vehicles:
 
        direction_control(vehicle, triggerboxesRoadsNS, triggerboxesRoadsEW)

         #loop through the car's trigger boxes and check if they are colliding with a light that is red or yellow, then adjust speed
        for triggerbox in triggerboxes:
            global timePassed
            #check for bus stop trigger
            for busStopEntity in busStopsEntity:
                
                if timePassed > busStopEntity.waitingTime + 5:
                    timePassed = 0
                if(busStopEntity.intersects(vehicle)) and vehicle.isBus == True:
                    
                    vehicle.speed = 0
                    #simulate time with timepassing
                    timePassed += .01
                    
                    #check to see if waitingTime has been reached and set speed back
                    if timePassed > busStopEntity.waitingTime:
                        vehicle.speed = vehicle.originalSpeed
                        
            #check for lights trigger         
            for lightNS in trafficLightsNS:
                adjust_vehicle_speed_at_light(vehicle, lightNS, triggerbox)
            for lightEW in trafficLightsEW:
                adjust_vehicle_speed_at_light(vehicle, lightEW, triggerbox)
        #needed for timePass issue for bus... 
        timePassed += .001
        activate_moving_speed(vehicle)


# Create the button
def add_vehicle():
    pass

def on_add_busStop_button_click():
    
    #randomly create a bus stop based on roads in list
    randomRoad = random.choice(roads_Entity_objects)
    
    if randomRoad.name[0] in ['N','S']:
        busStop = Entity(model='cube', scale=(3.5, 0.5, 1), color= color.blue)
        busStop.position = randomRoad.position
        busStop.y += random.choice(range(-20,20))
    elif randomRoad.name[0] in ['E','W']:
        busStop = Entity(model='cube', scale=(0.5, 3.5, 1), color= color.blue)
        busStop.position = randomRoad.position
        busStop.x += random.choice(range(-20,20))
    else:
        return    
    busStop.collider = 'box'    
    busStop.waitingTime = 20
    busStopsEntity.append(busStop)
    
def on_restart_button_click():
    global vehicles
    global triggerboxes
    global busStopsEntity
    global timePassed
    
    for vehicle in vehicles:
        destroy(vehicle)
    for triggerbox in triggerboxes:
        destroy(triggerbox)
    for busStop in busStopsEntity:
        destroy(busStop)
        
    vehicles = [] 
    triggerboxes = []
    busStopsEntity = []
    timePassed = 0
    createCars("default")
    
def on_end_button_click():
    application.quit()
    
def on_button_click():
    createCars("add")
    

button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.50, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_button_click)
restartButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.38, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_restart_button_click)
endButton = Button(text='End\nSimulation', color=rgb(128, 0, 0), highlight_color=color.red, position=(0.62, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_end_button_click)
addBusStop = Button(text='Add\nBus\nStop', color=color.blue, highlight_color=color.cyan, position=(.50, 0.34), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_add_busStop_button_click)
app.run()
