import VehicleCalculations
import datetime

# Global Variable
stopTimes = {} # road name, elapsed time
busArrived = {} # road name, boolean

# Vehicles adapt depending on bus stops
# Parameters:
#   busStop - The current bus stop on the given road
#   vehicles - The current set of vehicles interacting with the traffic light
#   busStopIndex - The index of the bus stop
# Returns:
#   vehicles - The list of vehicles that have interacted with the traffic light
def busStopSimulation(busStop, vehicles, busStopIndex):
    busStop_position = busStop[busStopIndex]["position"]

    global stopTimes
    global busArrived
    
    busStop_position = busStop[busStopIndex]["position"]
    busStop_road = busStop[busStopIndex]["road"]
    
    # Initializes busStop dict
    if busStop_road not in stopTimes:
        stopTimes[busStop_road] = 0
    
    # Initializes elapsed time
    elapsedTime = stopTimes[busStop_road]
    
    # Initializes busArrived dict
    if elapsedTime == 0:
        busArrived[busStop_road] = False
                                   
    for i in range(0, len(vehicles)):
        # Make sure the current vehicle is on the current road
            if vehicles[i]["road"] == busStop_road:   
                # Adjust acceleration of vehicle if the vehicle is behind the bus stop's position
                if vehicles[i]["position"] < busStop_position:
                    distance_to_bus_stop = busStop_position - vehicles[i]["position"]
                    # 1 IF a bus type vehicle is in the deceleration distance
                    if vehicles[i]["type"] == "bus" and distance_to_bus_stop <= VehicleCalculations.decelerationDistance and distance_to_bus_stop >= VehicleCalculations.stoppingDistance:
                        # 1.1 THEN apply the deceleration factor to the vehicle 
                        # Apply deceleration to bus and all vehicles behind bus
                        for j in range (i, len(vehicles)):
                            VehicleCalculations.applyDecelerationFactor(vehicles, j)
                    # 2 ELSE IF a bus type vehicle is in the stopping distance
                    elif vehicles[i]["type"] == "bus" and distance_to_bus_stop <= VehicleCalculations.stoppingDistance:
                        # 2.1 THEN causes the vehicle to stop
                        # Apply decleration to stop to bus and all vehicles behind bus
                        for k in range (i, len(vehicles)):
                            VehicleCalculations.adjustAccelerationToStop(vehicles, k)

                        if vehicles[i]["type"] == "bus" and distance_to_bus_stop > 0 and distance_to_bus_stop < 0.1:
                            vehicles[i]["speed"] = 0
                            vehicles[i]["acceleration"] = 0

                            # Timer for when bus first arrives at bus stop
                            if busArrived[busStop_road] == False:
                                stopTimes[busStop_road] = datetime.datetime.now()
                                busArrived[busStop_road] = True
                                # Set the waiting time of the indexed bus back to zero since it has arrived
                                busStop[busStopIndex]["waitingtime"] = 0
                            else:
                                difference_time = datetime.datetime.now() - stopTimes[busStop_road]
                                elapsedTime = difference_time.total_seconds()
                            print("______________________________________________________")
                            print("| BUS AT BUS STOP                                     ")
                            print("______________________________________________________")
                            print("| Bus Stop on", busStop_road)
                            print("| Bus Waiting Time: ", busStop[busStopIndex]["waitingtime"])
                            print("| Bus Elapsed Time", elapsedTime)
                            print("______________________________________________________\n")
                    
                    # 3 IF time since vehicle with bus type stopped > waiting time   
                    if elapsedTime > busStop[busStopIndex]["waitingtime"]:
                        # 3.1 THEN the vehicle may depart 
                        # Change bus position to leave bus stop   
                        vehicles[i]["position"] = busStop_position + 0.1              
                        for l in range (i, len(vehicles)):
                            VehicleCalculations.calculateAcceleration(vehicles,l)
                        print("______________________________________________________")
                        print("BUS IS NOW LEAVING BUS STOP ON", busStop_road)
                        print("______________________________________________________")
                        stopTimes[busStop_road] = 0
                        
    
    # Return the list of vehicles that have interacted with the bus stop with updated attributes
    return vehicles