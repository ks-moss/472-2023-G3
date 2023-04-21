import VehicleCalculations
import datetime
import time
# Goal: Simulating traffic lights
# Precondition: The system contains a diagram of the virtual road network. There is a traffic light on a road.
# Postcondition: Vehicles adapt depending on the state of the traffic light.

# Vehicles adapt depending on the state of the traffic light.
# Parameters:
#   trafficLight - The current traffic light on the given road
#   vehicles - The current set of vehicles interacting with the traffic light
#   timeSinceLastChange - The time since last change passed in from 3.3 Automatic Simulation
# Returns:
#   vehicles - The list of vehicles that have interacted with the traffic light
def trafficLightInteraction (trafficLight, vehicles, light_index, lightStates):

    # 1 & 1.1. IF time since last change > cycle, THEN change the color of the light (green ⇐⇒ red)
    if lightStates[light_index]["counter"] == trafficLight[light_index]["cycle"]:
        lightStates[light_index]["counter"] = 0
        if lightStates[light_index]["color"] == "red":
            lightStates[light_index]["color"] = "green"
        else:
            lightStates[light_index]["color"] = "red"
    
    if lightStates[light_index]["counter"] == trafficLight[light_index]["cycle"]*0.9 and lightStates[light_index]["color"] == "green":
        lightStates[light_index]["color"] == "yellow"

    # 2 & 2.1. IF traffic light is green, THEN vehicles in front of the traffic light may accelerate back up
    if lightStates[light_index]["color"] == "green":
        # Invoke acceleration function for ALL vehicles in front of the current traffic light
        i = 0
        j = 0

        while i < len(vehicles):
            # Make sure the current vehicle is on the current road
            if vehicles[i]["road"] == trafficLight[light_index]["road"]:   
                # Adjust acceleration of vehicle if the vehicle is behind the traffic light's position
                if vehicles[i]["position"] < trafficLight[light_index]["position"]:
                    lightInBetween = False
                    for l in trafficLight:
                        if (l["position"] < trafficLight[light_index]["position"] and l["position"] > vehicles[i]["position"]):
                            lightInBetween = True
                    if (not lightInBetween):
                        VehicleCalculations.calculateAcceleration(vehicles, i)
                    
            i += 1
                    
    # 3.1 IF traffic light is red
    if lightStates[light_index]["color"] == "red" or lightStates[light_index]["color"] == "yellow":

        # 3.1.1 THEN IF the first vehicle in front of the light is in the deceleration distance
        distance = trafficLight[light_index]["position"] - vehicles[0]["position"] # Calculate distance between traffic light & first vehicle position
        closest_vehicle_index = 0
        closest_vehicle_distance = abs(trafficLight[light_index]["position"] - vehicles[0]["position"])
        for i in range(1, len(vehicles)):
            # Calculate the distance between the traffic light and the current vehicle
            distance_to_traffic_light = abs(trafficLight[light_index]["position"] - vehicles[i]["position"])
            # If the current vehicle is closer to the traffic light than the previous closest vehicle, update the closest vehicle
            if distance_to_traffic_light < closest_vehicle_distance:
                closest_vehicle_index = i
                closest_vehicle_distance = distance_to_traffic_light
        if closest_vehicle_distance > 0.0 and closest_vehicle_distance < VehicleCalculations.decelerationDistance:
            # Apply the deceleration factor to the closest vehicle and all vehicles behind it within the deceleration distance
            for i in range(closest_vehicle_index, len(vehicles)):
                distance_to_traffic_light = trafficLight[light_index]["position"] - vehicles[i]["position"]
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
            VehicleCalculations.adjustAccelerationToStop(vehicles, i)
    
    lightStates[light_index]["counter"] += 1
