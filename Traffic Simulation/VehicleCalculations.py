from TrafficSimulation2 import TrafficSystem
import math

trafficSystem = TrafficSystem()
trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")

vehicles = trafficSystem.vehicleList
# Appendix B.6 - Default Values
length = 4
maximumSpeed = 16.6
maximumAcceleration = 1.44
maximumBrakingFactor = 4.61
minimumFollowingDistance = 4
simulationTime = 0.0166
decelerationDistance = 50
stoppingDistance = 15
delayFactor = 0.4

# 3.1 - Calculate the Speed and Position of Vehicle
def calculateVehicleSpeedAndPosition(vehicleIndex):
    vehicle = vehicles[vehicleIndex]
    speed = maximumSpeed
    position = 0
    acceleration = calculateAcceleration(vehicleIndex - 1, vehicleIndex)
    if (speed + acceleration*simulationTime) < 0:
        position = position - (speed*speed)/2*acceleration
        speed = 0
    else:
        speed = speed + acceleration*simulationTime
        position = position + speed*simulationTime + acceleration*((simulationTime*simulationTime)/2)

    #DEBUG
    #print("Speed: ", speed)
    #print("Position ", position)
    return [speed, position]

def calculateAcceleration(frontVehicleIndex, backVehicleIndex):
    try:
        frontVehicle = vehicles[frontVehicleIndex]
    except NameError:
        vehicleExists = False
    else:
        vehicleExists = True

    backVehicle = vehicles[backVehicleIndex]  

    speed = maximumSpeed

    positionDifference = frontVehicle["position"] - backVehicle["position"] - length

    speedDifference = 0 # It should be backVehicleSpeed - frontVehicleSpeed

    if(vehicleExists == True):
        vehicleInteration = (minimumFollowingDistance + max(0, speed + ((maximumSpeed*speedDifference)/(2*math.sqrt(maximumAcceleration*maximumBrakingFactor))))/positionDifference)
    else:
        vehicleInteration = 0
    
    acceleration = maximumAcceleration*(1 - (speed/maximumSpeed)**4 - vehicleInteration**2)

    #DEBUG
    #print("Acceleration: ", acceleration)
    return acceleration

calculateVehicleSpeedAndPosition(1)