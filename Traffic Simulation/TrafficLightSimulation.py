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
        for i in range(len(vehicles)):
            # Make sure the current vehicle is on the current road
            if vehicles[i]["road"] == trafficLight[light_index]["road"]:   
                # Adjust acceleration of vehicle if the vehicle is behind the traffic light's position
                if vehicles[i]["position"] < trafficLight[light_index]["position"]:
                    lightInBetween = False
                    for l in trafficLight:
                        if (l["position"] < trafficLight[light_index]["position"] and l["position"] > vehicles[i]["position"]):
                            lightInBetween = True
                    if (not lightInBetween):
                        if (vehicles[i]["speed"] < 5):
                            vehicles[i]["speed"] = 5
                        if (vehicles[i]["acceleration"] < 2):
                            vehicles[i]["acceleration"] = 2
                    
    # 3.1 IF traffic light is red
    elif lightStates[light_index]["color"] == "red":
        # 3.1.1 THEN IF the first vehicle in front of the light is in the deceleration distance
        for k in range(len(vehicles)):
            distance = (trafficLight[light_index]["position"] - 4) - vehicles[k]["position"] # Calculate distance between traffic light & first vehicle position
            if (vehicles[k]["road"] == trafficLight[light_index]["road"]):
                if vehicles[k]["position"] < trafficLight[light_index]["position"]:
                    lightInBetween = False
                    for l in trafficLight:
                        if (l["position"] < trafficLight[light_index]["position"] and l["position"] > vehicles[k]["position"]):
                            lightInBetween = True
                    if (not lightInBetween):
                        if (distance < VehicleCalculations.stoppingDistance):
                            VehicleCalculations.adjustAccelerationToStop(vehicles, k)
                            VehicleCalculations.applyDecelerationFactor(vehicles, k)
                            if (distance > 0 and distance < 0.3):
                                vehicles[k]["speed"] = 0
                                vehicles[k]["acceleration"] = 0
    
    lightStates[light_index]["counter"] += 1
