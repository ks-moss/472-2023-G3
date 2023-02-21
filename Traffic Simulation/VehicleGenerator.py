from TrafficSimulation2 import TrafficSystem

# create a TrafficSystem object from the input file
traffic_system = TrafficSystem()
traffic_system.ReadElementsFromFile("./InputFiles/vehicleGen2.xml")

#add list of generated vehicles to local variable
vehicles = traffic_system.vehicleGeneratorList

# addVehicle
# parameters:
#   none
# precondition:
#   new vehicles not part of vehicleList
# postcondition:
#   vehicles from vehiclegenerator xml added to vehicleList
# returns:
#   none
def addVehicle():
    for i in range(len(vehicles)):
        road = vehicles[i]["name"]
        print("Vehicle with frequency ", vehicles[i]["frequency"], " added to ", vehicles[i]["name"], " road")
        traffic_system.vehicleList.append({"road": road, "position": 0})
        
addVehicle()
