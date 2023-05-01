import sys
import os

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(FILE_DIR))

from src import VehicleCalculations

# Vehicles adapt depending on bus stops
# Parameters:
#   busStop - The current bus stop on the given road
#   vehicles - The current set of vehicles interacting with the traffic light
#   busStopIndex - The index of the bus stop
# Returns:
#   vehicles - The list of vehicles that have interacted with the traffic light
def busStopSimulation(busStop, vehicles, busStopIndex, busStopCounter):
    busStop_position = busStop[busStopIndex]["position"]
    busStop_road = busStop[busStopIndex]["road"]
                                   
    for i in range(0, len(vehicles)):
        # Make sure the current vehicle is on the current road
        if vehicles[i]["road"] == busStop_road and vehicles[i]["type"] == "bus":   
            # Adjust acceleration of vehicle if the vehicle is behind the bus stop's position
            if vehicles[i]["position"] < busStop_position:
                distance_to_bus_stop = busStop_position - vehicles[i]["position"]
                # 1 IF a bus type vehicle is in the deceleration distance
                if distance_to_bus_stop <= VehicleCalculations.decelerationDistance and distance_to_bus_stop > VehicleCalculations.stoppingDistance:
                    # 1.1 THEN apply the deceleration factor to the vehicle 
                    # Apply deceleration to bus and all vehicles behind bus
                    VehicleCalculations.applyDecelerationFactor(vehicles, i)
                # 2 ELSE IF a bus type vehicle is in the stopping distance
                elif vehicles[i]["type"] == "bus" and distance_to_bus_stop <= VehicleCalculations.stoppingDistance:
                    # 2.1 THEN causes the vehicle to stop
                    # Apply decleration to stop to bus and all vehicles behind bus
                    VehicleCalculations.adjustAccelerationToStop(vehicles, i)

                    if distance_to_bus_stop > 0 and distance_to_bus_stop < 0.3:
                        vehicles[i]["speed"] = 0
                        vehicles[i]["acceleration"] = 0

                        if busStopCounter[i]["counter"] >= busStop[busStopIndex]["waitingtime"]*10:
                            busStopCounter[i]["counter"] == 0
                            vehicles[i]["position"] = busStop_position + 0.1
                            VehicleCalculations.calculateAcceleration(vehicles, i)
                            print("______________________________________________________")
                            print("BUS IS NOW LEAVING BUS STOP ON", busStop_road)
                            print("______________________________________________________")
                        elif busStopCounter[i]["counter"] < busStop[busStopIndex]["waitingtime"]*10:
                            busStopCounter[i]["counter"] += 1
                        print("______________________________________________________")
                        print("| BUS AT BUS STOP                                     ")
                        print("______________________________________________________")
                        print("| Bus Stop on", busStop_road)
                        print("| Bus Waiting Time: ", busStop[busStopIndex]["waitingtime"])
                        print("| Bus Elapsed Time", busStopCounter[i]["counter"])
                        print("______________________________________________________\n")
            else: 
                busStopCounter[i]["counter"] = 0
                """# 3 IF time since vehicle with bus type stopped > waiting time   
                if elapsedTime >= busStop[busStopIndex]["waitingtime"]*10:
                    # 3.1 THEN the vehicle may depart 
                    # Change bus position to leave bus stop   
                    vehicles[i]["position"] = busStop_position + 0.1              
                    for l in range (i, len(vehicles)):
                        VehicleCalculations.calculateAcceleration(vehicles,l)
                    print("______________________________________________________")
                    print("BUS IS NOW LEAVING BUS STOP ON", busStop_road)
                    print("______________________________________________________")
                    stopTimes[busStop_road] = 0"""