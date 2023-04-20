import sys
from ursina import *





def create_roads(traffic_system):
    Entity_models = []
    triggerBoxesNS = []
    triggerboxesEW = []
    duplicate_list = []

    for i in range(len(traffic_system.intersection_list)):
        for j in range(len(traffic_system.intersection_list[i])):

            road_name = traffic_system.intersection_list[i][j]["road"]

            is_duplicate = False
            for k in range(len(duplicate_list)):
                if(duplicate_list[k] == road_name):
                    is_duplicate = True

            if(is_duplicate == False):

                duplicate_list.append(road_name)
                road_position = traffic_system.intersection_list[i][j]["position"]

                if (road_name[0] == "N" or road_name[0] == "S") and road_name[1] == " ":  # Verticle Roads
                    # Create the object_rec Entity and pass text_entity as a child
                    road_model = Entity(model='cube', scale=(4, 100, 0.1), color=color.gray)
                    road_model.texture=load_texture(f'textures/road.png')
                    trigger_box_road1 = Entity(model='wireframe_cube', color=color.clear, scale=(.05, 1, 1), collider='box', origin_x=8)
                    trigger_box_road1.parent = road_model
                    #add trigger box to list of NS roads triggers
                    triggerBoxesNS.append(trigger_box_road1)
                    road_model.y = road_position/2   
                    road_model.x = road_position*5
                    roadText= Text(text=road_name, scale=(25,2), color=color.black)
                    roadText.parent = road_model
                    roadText.z = -.5
                    roadText.y = -.5
                    road_model.name = road_name
                    Entity_models.append(road_model)
                    
                    box2 = Entity(model='cube', scale=(4))
                    box2.position = road_model.position -3 # then adjust the z-position relative to box
                    box2.texture=load_texture(f'textures/building.png')
                    box2.rotation = (28,30,32)
                    
                elif (road_name[0] == "E" or road_name[0] == "W") and road_name[1] == " ": # Horizontal Roads
                    # Create the object_rec Entity and pass text_entity as a child
                    road_model = Entity(model='cube', scale=(100, 4, 0.1), color=color.gray)
                    road_model.texture=load_texture(f'textures/road2.png')
                    road_model.texture.rotation = (0,0,90)
                    trigger_box_road2 = Entity(model='wireframe_cube', color=color.clear, scale=(1, .05, 1), collider='box', origin_y=8)
                    trigger_box_road2.parent = road_model
                    triggerboxesEW.append(trigger_box_road2)
                    road_model.y = road_position/2
                    roadText= Text(text=road_name, scale=(1.15,25), color=color.black)
                    roadText.parent = road_model
                    roadText.z = -2
                    roadText.y = -.5
                    road_model.name = road_name
                    Entity_models.append(road_model)
                    
                    box3 = Entity(model='cube', scale=(3,5,7))
                    box3.position = road_model.position -4 # then adjust the z-position relative to box
                    box3.texture=load_texture(f'textures/building2.png')
                    box3.rotation = (28,30,32)

                else:
                    print("Please Declair N|S|E|W in the", traffic_system.file_name, "input file")
                    # Terminate the program without specifying an exit code
                    sys.exit()

    return duplicate_list, Entity_models, triggerBoxesNS, triggerboxesEW









def place_traffic_lights(traffic_system):
    # PLACE THE TRAFFIC LIGHTS ONTO THE ROADS
    lights = traffic_system.traffic_light_list

    LightsNS = []
    LightsEW = []
    

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
            LightsNS.append(NS_lightPoles)
        # Now lets take a look at the E/W light of the intersection
        if lights[i+1]["road"][0] == "W" or lights[i+1]["road"][0] == "E":
            EWlightpos_x = lights[i + 1]["position"] / 1.8
            EWlightpos_y = lights[i]["position"] * 5
            if EWlightpos_x > 0:
                EWlightpos_x -= 5
            EW_lightPoles.position = (EWlightpos_x, EWlightpos_y)
            #add light to list of lights
            LightsEW.append(EW_lightPoles)
        i += 1 # increment to get to the next intersection

        # We need this so we don't go out of bounds
        if i == len(lights) - 1:
            break

    return LightsNS, LightsEW
        








def place_bus_stops(traffic_system, EntityModels):
    
    busStopsEntityModels = []

    busStops = traffic_system.bust_stop_list
    #PLACE BUS STOPS
    for i in range(0, len(busStops)):
        print("BUSSSTOPS", busStops)
        busStop1 = Entity(model='cube', scale=(3.5, 0.5, 1), color= color.white)
        busStop1.collider = 'box'
        busStop1.waitingTime = busStops[i]['waitingtime'] 
        busStop1.isTriggered = False
        for roads in EntityModels:
            if roads.name == busStops[i]['road']:
                busStop1.position = roads.position
                busStopsEntityModels.append(busStop1)

    return busStopsEntityModels 












def create_vehicle_entity(current_speed, current_car_type, current_road, current_position, roadEntityModels, roadsDuplicateList, vehiclesList, triggerboxesList):
    available_colors = [color.gold, color.white, color.magenta, color.yellow, color.white, color.pink, color.orange]
    color_random_index = random.randint(0, len(available_colors)-1)
    car = Entity(model='cube', scale=(2, 1, 1), color=available_colors[color_random_index])
    car.collider = 'box'
    car.speed = current_speed / 100
    car.originalSpeed = car.speed
    car.car_type = current_car_type
    car.road = current_road
    car.pos = current_position
    car.collided = False
    car.isBus = False
    car.texture=load_texture(f'textures/car.png')

    if (car.car_type == 'bus'):
        car.scale = (2,2,1)
        car.color = color.white
        car.isBus = True
        car.texture=load_texture(f'textures/bus.png')
    if (car.car_type == 'fire truck'):
        car.scale = (2,2,1)
        car.color = color.red
        car.texture=load_texture(f'textures/fireTruck.png')   
    if (car.car_type == 'police van'):
        car.color = color.white
        car.texture=load_texture(f'textures/police.png')
        
    # This iteration implementation will make sure that the vehicle is on the assigned road (When there are more than 2 vehicles on the assigned road)
    for i in range(len(roadEntityModels)):
        if(car.road == roadsDuplicateList[i]):
            if (car.road[0] == "N" or car.road[0] == "S") and car.road[1] == " ":
                car.is_on_y_axis = True
                car.position = (roadEntityModels[i].x, car.pos)
                car.rotation = (0, 0, 90)
            else:
                car.is_on_y_axis = False
                car.position = (car.pos, roadEntityModels[i].y)
                car.rotation = (0, 0, 180)

            trigger_box3 = Entity(model='wireframe_cube', color=color.clear, scale=(2.75, 1, 1), collider='box', origin_x=.3)
            trigger_box3.parent = car
            triggerboxesList.append(trigger_box3)
            # Add the car to the list of vehicles
            vehiclesList.append(car)







def change_NS_lights(traffic_lights_NS, traffic_light_time):
    #change light colors for North/South roads
    if traffic_light_time < 8:
        for NS_lightPoles in traffic_lights_NS:
            NS_lightPoles.color = color.green
    elif traffic_light_time < 10:
        for NS_lightPoles in traffic_lights_NS:
            NS_lightPoles.color = color.yellow
    else:
        for NS_lightPoles in traffic_lights_NS:
            NS_lightPoles.color = color.red






def change_EW_lights(traffic_lights_EW, traffic_light_time):
    #change light colors for East/West roads
    #these should oppose the lights on N/W roads
    if traffic_light_time < 10:
        for EW_lightPoles in traffic_lights_EW:
            EW_lightPoles.color = color.red
    elif traffic_light_time < 13:
        for EW_lightPoles in traffic_lights_EW:
            EW_lightPoles.color = color.green
    elif traffic_light_time < 15:
        for EW_lightPoles in traffic_lights_EW:
            EW_lightPoles.color = color.yellow





def direction_control(vehicle_object, triggerboxes_NS_object, triggerboxes_EW_object):
    #Check if vehicle intersects beginning of crossroads
    #if statement to account for constant vehicle checks at collision
    if random.choice(range(8)) == 1:
        vehicle_object.collided = False
    #check triggerboxes on NS roads        
    for triggerboxesNS in triggerboxes_NS_object:
        if vehicle_object.intersects(triggerboxesNS) and vehicle_object.collided == False:
            vehicle_object.collided = True
            #randomly choose to turn or not turn
            if random.choice(range(2)) == 1 and vehicle_object.collided == True:
                
                for i in range(20):
                    if vehicle_object.rotation == (0,0,90):
                        vehicle_object.is_on_y_axis = True
                        vehicle_object.collided = False
                        break
                    vehicle_object.rotation = vehicle_object.rotation-(0, 0, 5)
                    vehicle_object.position = vehicle_object.position + (.15,0,0)
            else: 
                pass

    for triggerboxesEW in triggerboxes_EW_object:
        if vehicle_object.intersects(triggerboxesEW) and vehicle_object.collided == False:
                
            vehicle_object.collided = True
            #randomly choose to turn or not turn
            if random.choice(range(2)) == 1 and vehicle_object.collided == True:
                
                for i in range(20):
                    if vehicle_object.rotation == (0,0,-90):
                        vehicle_object.is_on_y_axis = False
                        vehicle_object.collided = False
                        vehicle_object.rotation = (0, 0, 180)
                        break
                    vehicle_object.rotation = vehicle_object.rotation+(0, 0, -10)
                    vehicle_object.position = vehicle_object.position + (0,.15,0)
            else: 
                pass






def adjust_vehicle_speed_at_light(vehicle_object, light_signal, triggerbox_object):
    if light_signal.intersects(triggerbox_object) and vehicle_object.intersects(triggerbox_object) and light_signal.color == color.green:
        vehicle_object.speed = vehicle_object.originalSpeed
    elif light_signal.intersects(triggerbox_object) and vehicle_object.intersects(triggerbox_object) and (light_signal.color == color.yellow):
        vehicle_object.speed = max(0, vehicle_object.speed - .008)
    elif light_signal.intersects(triggerbox_object) and vehicle_object.intersects(triggerbox_object) and (light_signal.color == color.red):
        vehicle_object.speed = max(0, vehicle_object.speed - .008)
    


def activate_moving_speed(current_vehicle):
    if current_vehicle.is_on_y_axis:
            current_vehicle.y += current_vehicle.speed
            if current_vehicle.y > 49:
                current_vehicle.y = -49
    else:
        current_vehicle.x += current_vehicle.speed
        if current_vehicle.x > 49:
            current_vehicle.x = -49



