from TrafficSimulation2 import TrafficSystem
import math

trafficSystem = TrafficSystem()
trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")

vehicles = trafficSystem.vehicleList
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
#   vehicleIndex - The index of the vehicle inside of the list
#   currentSpeed - The current speed of the vehicle being calculated
#   currentAcceleration - The current acceleration of the vehicle being calculated
# returns:
#   speed - The new speed of the vehicle
#   position - The new position of the vehicle
def calculateVehicleSpeedAndPosition(vehicleIndex, currentSpeed, currentAcceleration):
    vehicle = vehicles[vehicleIndex]
    speed = currentSpeed
    position = vehicle["position"]
    acceleration = currentAcceleration
    if (speed + acceleration*simulationTime) < 0:
        position = position - (speed*speed)/2*acceleration
        speed = 0
    else:
        speed = speed + acceleration*simulationTime
        position = position + (speed*simulationTime) + acceleration*((simulationTime*simulationTime)/2)

    #vehicle["speed"] = speed
    #DEBUG
    print("Speed: ", speed)
    print("Position ", position)
    return [speed, position]

# Calculates The New Acceleration of Vehicle
# parameters:
#   vehicleIndex - The index of the vehicle inside of the list
#   currentSpeed - The current speed of the vehicle being calculated
#   currentFrontSpeed - The current acceleration of the vehicle being calculated
# returns:
#   acceleration - The new acceleration of the vehicle
def calculateAcceleration(vehicleIndex, currentSpeed, currentFrontSpeed):
    try:
        frontVehicle = vehicles[vehicleIndex - 1]
    except NameError:
        vehicleExists = False
    else:
        vehicleExists = True

    backVehicle = vehicles[vehicleIndex]  

    speed = currentSpeed

    positionDifference = frontVehicle["position"] - backVehicle["position"] - length
    
    # print("Front Vehicle Position ", frontVehicle["position"])
    # print("Back Vehicle Position ", backVehicle["position"])
    # print("Position Difference ", positionDifference)

    speedDifference = speed - currentFrontSpeed

    if(vehicleExists == True):
        vehicleInteration = ((minimumFollowingDistance + max(0, speed + ((speed*speedDifference)/(2*math.sqrt(maximumAcceleration*maximumBrakingFactor)))))/positionDifference)
    else:
        vehicleInteration = 0
    
    acceleration = maximumAcceleration*(1 - (speed/maximumSpeed)**4 - vehicleInteration**2)

    #DEBUG
    # print("Acceleration: ", acceleration)
    return acceleration

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
#   vehicleIndex -  the index of the vehicle to be checked
#   newPosition  -  the new position that the vehicle will be on the 
#                   next simulation step
# precondition:
#   a new positon is calculated for the vehicle
# postcondition:
#   vehicle will be removed from list if the new position
#   is off the street
# return:
#   void
def vehicleOutOfBounds(vehicleIndex, newPosition):
    roads = trafficSystem.roadList

    vehicle = vehicles[vehicleIndex]

    # search for the current road the vehicle is on
    for road in roads:
        if (road["name"] == vehicle["road"]):
            # check if vehicle is off the road
            if (newPosition > road["length"]):
                # remove vehicle from road
                del vehicles[vehicleIndex]
                break
    
    #DEBUG
    # print('current vehicle list', *vehicles, sep="\n")


calculateVehicleSpeedAndPosition(0,16,1)
calculateAcceleration(0,16,16)
adjustDesiredMaxSpeed(isSlowingDown=True)
adjustAccelerationToStop(16.6)
vehicleOutOfBounds(3, 1510)