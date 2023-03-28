from TrafficSimulation2 import TrafficSystem
import math

# trafficSystem = TrafficSystem()
# trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")

# vehicles = trafficSystem.vehicleList
# Appendix B.6 - Default Values
length = 4
maximumSpeed = 16.6
absoluteMaxSpeed = 16.6
maximumAcceleration = 1.44
maximumBrakingFactor = 4.61
minimumFollowingDistance = 4
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
    frontVehicle = {"position": 999999999}
    vehicleExists = False  
    for i in range(len(vehicleList)):
        currVehicle = vehicleList[i]
        if (i != vehicleIndex and currVehicle["road"] == vehicle["road"] and 
            currVehicle["position"] > vehicle["position"]):
            vehicleExists = True
            if (frontVehicle["position"] > currVehicle["position"]):
                frontVehicle = vehicleList[i]

    speed = vehicle["speed"]
    
    # print("Front Vehicle Position ", frontVehicle["position"])
    # print("Back Vehicle Position ", backVehicle["position"])
    # print("Position Difference ", positionDifference)


    if(vehicleExists == True):
        positionDifference = frontVehicle["position"] - vehicle["position"] - length
        speedDifference = speed - frontVehicle["speed"]
        vehicleInteration = ((minimumFollowingDistance + max(0, speed + ((speed*speedDifference)/(2*math.sqrt(maximumAcceleration*maximumBrakingFactor)))))/positionDifference)
    else:
        vehicleInteration = 0
    
    acceleration = maximumAcceleration*(1 - (speed/maximumSpeed)**4 - vehicleInteration**2)

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
#   currentSpeed - the speed of the current vehicle being calculated
# return:
#   acceleration - the new acceleration of the vehicle
def adjustAccelerationToStop(currentSpeed):
    # Eq:  a = -(b_max*v / v_max)
    acceleration = -1 * ((maximumBrakingFactor * currentSpeed) / maximumSpeed)

    #DEBUG
    # print("Acceleration Set to: ", acceleration)

    return acceleration

# Checks to see if a vehicle is out of bounds by 
# comparing the length of the street and the position
# of the vehicle.
# parameters:
#   vehicleList  -  vehicleList from TrafficSystem()
#   vehicleIndex -  the index of the vehicle to be checked
#   roadList     -  roadList from TrafficSystem()
#   newPosition  -  the new position that the vehicle will be on the 
#                   next simulation step
# precondition:
#   a new positon is calculated for the vehicle
# postcondition:
#   vehicle will be removed from list if the new position
#   is off the street
# return:
#   void
def vehicleOutOfBounds(vehicleList: TrafficSystem, vehicleIndex, roadList: TrafficSystem):
    roads = roadList

    vehicle = vehicleList[vehicleIndex]

    # search for the current road the vehicle is on
    for road in roads:
        if (road["name"] == vehicle["road"]):
            # check if vehicle is off the road
            if (vehicle["position"] > road["length"]):
                # remove vehicle from road
                del vehicleList[vehicleIndex]
                break
    
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

    deceleration_factor = 0.5  # Slow it down by half
    
    # Apply the deceleration factor to the ith vehicle
    vehicles[i]["acceleration"] *= deceleration_factor

#calculateVehicleSpeedAndPosition(vehicles,0)
#calculateAcceleration(vehicles,0)
# adjustDesiredMaxSpeed(isSlowingDown=True)
# adjustAccelerationToStop(16.6)
# vehicleOutOfBounds(3, 1510)