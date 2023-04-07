import VehicleCalculations
import datetime
import time
# Goal: Simulating traffic lights
# Precondition: The system contains a diagram of the virtual road network. There is a traffic light on a road.
# Postcondition: Vehicles adapt depending on the state of the traffic light.

# Global Variables
green_light = {}    # (road name, True/False) True means green, False means red
light_Times = {}    # (road name, time since traffic light was last changed)

# Vehicles adapt depending on the state of the traffic light.
# Parameters:
#   trafficLight - The current traffic light on the given road
#   vehicles - The current set of vehicles interacting with the traffic light
#   timeSinceLastChange - The time since last change passed in from 3.3 Automatic Simulation
# Returns:
#   vehicles - The list of vehicles that have interacted with the traffic light
def trafficLightInteraction (trafficLight, vehicles, light_index):
    # Traffic Light Variables
    global green_light
    global light_Times

    trafficLight_road = trafficLight[light_index]["road"]
    trafficLight_position = trafficLight[light_index]["position"]
    trafficLight_cycle = trafficLight[light_index]["cycle"]
    
    # Track the time when the traffic light was first read
    if trafficLight_road not in light_Times:
        green_light[trafficLight_road] = True
        light_Times[trafficLight_road] = datetime.datetime.now()
        timeSinceLastChange = 0
    # If the time of the traffic light was previously recorded, calculate the difference between now and recorded time
    else:
        difference_time = datetime.datetime.now() - light_Times[trafficLight_road]
        timeSinceLastChange = difference_time.total_seconds()
        

    # 1 & 1.1. IF time since last change > cycle, THEN change the color of the light (green ⇐⇒ red)
    if timeSinceLastChange > trafficLight_cycle:
        light_Times[trafficLight_road] = datetime.datetime.now()
        if green_light[trafficLight_road]:
            print(trafficLight_road ,"'s light turned RED")
            green_light[trafficLight_road] = False
        else:
            print(trafficLight_road, "'s light turned GREEN")
            green_light[trafficLight_road] = True
    else:
        if green_light[trafficLight_road]:
            print(trafficLight_road, "'s Light has been GREEN for", timeSinceLastChange, "s, changes every ", trafficLight_cycle, "s")
        else:
            print(trafficLight_road, "'s Light has been RED for", timeSinceLastChange, "s, changes every ", trafficLight_cycle, "s")
        
    # 2 & 2.1. IF traffic light is green, THEN vehicles in front of the traffic light may accelerate back up
    if green_light[trafficLight_road] == True:
        # Invoke acceleration function for ALL vehicles in front of the current traffic light
        i = 0
        while i < len(vehicles):
            # Make sure the current vehicle is on the current road
            if vehicles[i]["road"] == trafficLight_road:   
                # Adjust acceleration of vehicle if the vehicle is behind the traffic light's position
                if vehicles[i]["position"] < trafficLight_position:
                    VehicleCalculations.calculateAcceleration(vehicles, i)
                    
            i += 1
                    
    # 3.1 IF traffic light is red
    if green_light[trafficLight_road] == False:

        # 3.1.1 THEN IF the first vehicle in front of the light is in the deceleration distance
        distance = trafficLight_position - vehicles[0]["position"] # Calculate distance between traffic light & first vehicle position
        closest_vehicle_index = 0
        closest_vehicle_distance = abs(trafficLight_position - vehicles[0]["position"])
        for i in range(1, len(vehicles)):
            # Calculate the distance between the traffic light and the current vehicle
            distance_to_traffic_light = abs(trafficLight_position - vehicles[i]["position"])
            # If the current vehicle is closer to the traffic light than the previous closest vehicle, update the closest vehicle
            if distance_to_traffic_light < closest_vehicle_distance:
                closest_vehicle_index = i
                closest_vehicle_distance = distance_to_traffic_light
        if closest_vehicle_distance > 0.0 and closest_vehicle_distance < VehicleCalculations.decelerationDistance:
            # Apply the deceleration factor to the closest vehicle and all vehicles behind it within the deceleration distance
            for i in range(closest_vehicle_index, len(vehicles)):
                distance_to_traffic_light = trafficLight_position - vehicles[i]["position"]
                if distance_to_traffic_light <= VehicleCalculations.decelerationDistance:
                    VehicleCalculations.applyDecelerationFactor(vehicles, i)
                    # Debug print
                    # print("Applied Deceleration Factor to Vehicle: ", vehicles[i]["type"])

        # 3.1.2 ELSE IF the first vehicle in front of the light is in the first half of the stopping distance
        elif distance > (VehicleCalculations.stoppingDistance / 2) and distance < VehicleCalculations.stoppingDistance:
            # 3.1.2.1 THEN stop the vehicle
            def stopVehicle(vehicles):
                # iterate through all vehicles and set them to stop at their current position
                i = 0
                while i < len(vehicles):
                    vehicles[i]["position"] = "position"
                    i += 1
            1 # Function unavailable (Pending 3.1 team)
    
    # Return the list of vehicles that have interacted with the traffic light with updated attributes
    return vehicles
