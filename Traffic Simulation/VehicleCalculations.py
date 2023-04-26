from TrafficSimulation2 import TrafficSystem
import math
import json

# trafficSystem = TrafficSystem()
# trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")

# Parse the JSON data from the vehicle configuration file (json)

with open('./InputFiles/vehicles.json') as f:
    data = json.load(f)

# Gather each vehicle's specs as a list
list_of_objects = list(data)

types = []
lengths = []
maxSpeeds = []
maxAccels = []
maxBrakingFactors = []
minFollowingDists = []

# Loop through the JSON data and process each object
# for obj in data:
    # Now you can work with the individual object
    # print(obj)

# Add specs to list
for obj in list_of_objects:
    types.append(obj['type'])
    lengths.append(obj['length'])
    maxSpeeds.append(obj["maximumSpeed"])
    maxAccels.append(obj["maximumAcceleration"])
    maxBrakingFactors.append(obj["maximumBrakingFactor"])
    minFollowingDists.append(obj["minimumFollowingDistance"])

# NOTE: Each vehicle corresponds to the same index, ie index 0 for each array contains a car's specs
    # types[0] = car, lengths[0] = 4 (car's length)

#tentative variable to choose type of vehicle from config file (json)
vehicleType = {"car": 0, "bus": 1, "fire truck": 2, "ambulance": 3, "police van": 4}

"""type = types[setVehicle]
length = lengths[setVehicle]
maximumSpeed = maxSpeeds[setVehicle]
maximumAcceleration = maxAccels[setVehicle]
maximumBrakingFactor = maxBrakingFactors[setVehicle]
minimumFollowingDistance = minFollowingDists[setVehicle]"""

# vehicles = trafficSystem.vehicleList
# Appendix B.6 - Default Values
#length = 4
#maximumSpeed = 16.6
absoluteMaxSpeed = 16.6
#maximumAcceleration = 1.44
#maximumBrakingFactor = 4.61
#minimumFollowingDistance = 4
simulationTime = 0.0166
decelerationDistance = 50
stoppingDistance = 15
delayFactor = 0.4

# Calculate the New Speed and Position of Vehicle
# parameters:
#   vehicleList - The vehicleList from TrafficSystem()
#   vehicleIndex - The index of the vehicle inside of the list
# returns:
#   none
def calculateVehicleSpeedAndPosition(vehicleList: TrafficSystem, vehicleIndex):
    vehicle = vehicleList[vehicleIndex]
    speed = vehicle["speed"]
    position = vehicle["position"]
    calculateAcceleration(vehicleList, vehicleIndex)
    acceleration = vehicle["acceleration"]
    
    if (speed + acceleration*simulationTime) < 0:
        position = position - (speed*speed)/2*acceleration
        speed = 0
    else:
        speed = speed + acceleration*simulationTime
        position = position + (speed*simulationTime) + acceleration*((simulationTime*simulationTime)/2)

    vehicle["speed"] = speed
    vehicle["position"] = position

    #DEBUG
    # print("Speed: ", speed)
    # print("Position ", position)
    # return [speed, position]

# Calculates The New Acceleration of Vehicle
# parameters:
#   vehicleList - The vehicleList from TrafficSystem()
#   vehicleIndex - The index of the vehicle inside of the list
# returns:
#   none
def calculateAcceleration(vehicleList: TrafficSystem, vehicleIndex):
    vehicle = vehicleList[vehicleIndex]
    speed = vehicle["speed"]
    typeIndex = vehicleType[vehicle["type"]]

    closestVehicle = {"position": 999999999}
    for i in range(len(vehicleList)):
        currVehicle = vehicleList[i]
        if (i != vehicleIndex and currVehicle["road"] == vehicle["road"] and 
            currVehicle["position"] > vehicle["position"]):
            if (closestVehicle["position"] > currVehicle["position"]):
                closestVehicle = currVehicle

    if(closestVehicle["position"] != 999999999):
        positionDifference = closestVehicle["position"] - vehicle["position"] - lengths[typeIndex]
        if (positionDifference < 3):
            speedDifference = speed - closestVehicle["speed"]
            vehicleInteration = ((minFollowingDists[typeIndex] + max(0, speed + ((speed*speedDifference)/(2*math.sqrt(maxAccels[typeIndex]*maxBrakingFactors[typeIndex])))))/positionDifference)
        else:
            vehicleInteration = 0
    else:
        vehicleInteration = 0
    
    acceleration = maxAccels[typeIndex]*(1 - (speed/maxSpeeds[typeIndex])**4 - vehicleInteration**2)

    vehicle["acceleration"] = acceleration
    #DEBUG
    # print("Acceleration: ", acceleration)
    # return acceleration

# Sets the maximum speed of the vehicles
# calling "calculateVehicleSpeedAndPosition" function will slow down each 
# vehicle according to the max speed possible
# parameters:
#   isSlowingDown - (Boolean) True: slow down vehicles | False: speed up vehicles
# returns:
#   void
def adjustDesiredMaxSpeed(isSlowingDown):
    if (isSlowingDown):
        # Eq:  v_max = sV_max
        maximumSpeed = delayFactor*absoluteMaxSpeed
    else:
        # Eq:  v_max = V_max
        maximumSpeed = absoluteMaxSpeed
    
    #DEBUG
    # print("Max Speed set to: ", maximumSpeed)

# Sets the acceleration in each simulation step according to the
# current speed of the vehicle. This function should be called for 
# each simulation step when stopping a vehicle
# parameters:
#   vehicles - vehicle list
#   vehicleIndex - index of current vehicle
# return:
#   none
def adjustAccelerationToStop(vehicles, vehicleIndex):
    # Eq:  a = -(b_max*v / v_max)
    vehicle = vehicles[vehicleIndex]
    typeIndex = vehicleType[vehicle["type"]]
    currentSpeed = vehicle["speed"]
    vehicle["acceleration"] = -1 * ((maxBrakingFactors[typeIndex] * currentSpeed) / maxSpeeds[typeIndex])


# Checks to see if each vehicle is out of bounds by 
# comparing the length of the street and the position
# of the vehicle.
# parameters:
#   vehicleList  -  vehicleList from TrafficSystem()
#   roadList     -  roadList from TrafficSystem()
#   to_be_removed  -  list of indices of vehicles that have reached the end of the road
# precondition:
#   vehicles new positions have been recalculated and may be off of the road
# postcondition:
#   vehicle index will be appended to to_be_removed if the new position
#   is off the road
# return:
#   void
def calculateVehicleOOB(vehicleList: TrafficSystem, roadList: TrafficSystem, to_be_removed: TrafficSystem):
    # Appends the index of all vehicles not on the road to to_be_removed
    for i in range(len(vehicleList)):
        vehicle = vehicleList[i]
        for road in roadList:
            if (road["name"] == vehicle["road"]):
                # check if vehicle is off the road
                if (vehicle["position"] > road["length"]):
                    # remove vehicle from road
                    to_be_removed.append(i)
                    #print("Vehicle", i, "has driven off the road, ")
    
    #DEBUG
    # print('current vehicle list', *vehicles, sep="\n")


# Applies the deceleration factor to the Ith vehicle in the list of vehicles.
# The deceleration factor is applied by adjusting the vehicle's acceleration attribute.
# parameters:
#   vehicles     -  vehicleList from TrafficSystem()
#   i            -  the index of the vehicle to be checked
# precondition:
#   vehicle is interacting with traffic light
# postcondition:
#   acceleration attribute is adjusted for the traffic light
# return:
#   void
def applyDecelerationFactor(vehicles, i):

    deceleration_factor = 0.2  # Slow it down by half
    
    # Apply the deceleration factor to the ith vehicle
    vehicles[i]["acceleration"] *= deceleration_factor

# Calculates the time required for a vehicle to travel a certain distance.
# parameters:
#   speed (float): The current speed of the vehicle in meters per second.
#   acceleration (float): The acceleration of the vehicle in meters per second squared.
#   distance (float): The distance to be traveled in meters.
#   timeStep (float): The duration of the simulation time step in seconds.
# return:
#   float: The time required for the vehicle to travel the specified distance in seconds.
def calculateTravelTime(speed, acceleration, distance, timeStep):
    
    # Calculate the time required to reach maximum speed
    t_max = (absoluteMaxSpeed - speed) / acceleration
    # Calculate the distance traveled during acceleration
    d_acc = speed * t_max + 0.5 * acceleration * t_max ** 2
    # Calculate the remaining distance to be traveled
    d_rem = distance - d_acc
    # Calculate the time required to travel the remaining distance at maximum speed
    t_rem = d_rem / absoluteMaxSpeed
    # Calculate the total time required
    total_time = t_max + t_rem
    # Adjust the total time for the simulation time step
    total_time += timeStep
    return total_time

#calculateVehicleSpeedAndPosition(vehicles,0)
#calculateAcceleration(vehicles,0)
# adjustDesiredMaxSpeed(isSlowingDown=True)
# adjustAccelerationToStop(16.6)
# vehicleOutOfBounds(3, 1510)