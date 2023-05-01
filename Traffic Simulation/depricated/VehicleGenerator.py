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
    temp = []
    for i in range(len(vehicles)):
        temp.append({"speed" : vehicles[i]["speed"], "type" : vehicles[i]["type"] ,"name" : vehicles[i]["name"], "position" : vehicles[i]["position"], "acceleration" : vehicles[i]["acceleration"]})
    return temp
