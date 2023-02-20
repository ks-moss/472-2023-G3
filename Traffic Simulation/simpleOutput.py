from TrafficSimulation2 import TrafficSystem
import time

# create a TrafficSystem object from the input file
traffic_system = TrafficSystem()
traffic_system.ReadElementsFromFile("./InputFiles/trafficSim2.xml")

# get list of vehicles, roads, and traffic lights
vehicles = traffic_system.vehicleList
roads = traffic_system.roadList
trafficLights = traffic_system.trafficLightList

# create a start time and a time check whenever runtime needed
startTime = time.time()
timeCheck1 = time.time()
print("Time ",timeCheck1-startTime)

# iterate over the list of vehicles and print their information
for i in range(len(vehicles)):
    print("Vehicle " , i+1)
    print("    -> road: ",vehicles[i]["road"])
    print("    -> position: ",vehicles[i]["position"])
    print("    -> speed: 16.6")
   