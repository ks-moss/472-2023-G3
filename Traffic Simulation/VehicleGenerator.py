from TrafficSimulation2 import TrafficSystem

# addVehicle
# parameters:
#   none
# precondition:
#   new vehicles not part of vehicleList
# postcondition:
#   vehicles from vehiclegenerator xml added to vehicleList
# returns:
#   none

class VehicleGenerator:
        
    def __init__(self):
         # create a TrafficSystem object from the input file
        self.traffic_system = TrafficSystem()
        self.traffic_system.ReadElementsFromFile("./InputFiles/vehicleGen2.xml")
        #add list of generated vehicles to local variable
        self.vehicles = self.traffic_system.vehicleGeneratorList
         
        
    def getVehicle(self):
        for i in range(len(self.vehicles)):
            road = self.vehicles[i]["name"]

            
            print("Vehicle of type", self.vehicles[i]["type"], "with frequency ", self.vehicles[i]["frequency"], " added to ", self.vehicles[i]["name"], " road")
            self.traffic_system.vehicleList.append({"road": road, "position": 0})


# temp = VehicleGenerator()
# temp.getVehicle()
