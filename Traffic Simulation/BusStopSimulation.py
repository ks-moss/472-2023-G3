import VehicleCalculations
import datetime

# Global Variable
stopTimes = {} # road name, elapsed time

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
    busStop_road = busStop[busStopIndex]["road"]
    
    # Track the time when the bus stop was first read
    if busStop_road not in stopTimes:
        stopTimes[busStop_road] = datetime.datetime.now()
        elapsedTime = 0
    # If the time of the bus stop was previously recorded, calculate the difference between now and recorded time
    else:
        difference_time = datetime.datetime.now() - stopTimes[busStop_road]
        elapsedTime = difference_time.total_seconds()
                                             
    for i in range(0, len(vehicles)):
        # Make sure the current vehicle is on the current road
            if vehicles[i]["road"] == busStop_road:   
                # Adjust acceleration of vehicle if the vehicle is behind the traffic light's position
                if vehicles[i]["position"] < busStop_position:
                    distance_to_bus_stop = busStop_position - vehicles[i]["position"]
                    # 1 IF a bus type vehicle is in the deceleration distance
                    if vehicles[i]["type"] == "bus" and distance_to_bus_stop <= VehicleCalculations.decelerationDistance:
                        # 1.1 THEN apply the deceleration factor to the vehicle 
                        VehicleCalculations.applyDecelerationFactor(vehicles, i) 
                    # 2 ELSE IF a bus type vehicle is in the stopping distance
                    elif vehicles[i]["type"] == "bus" and distance_to_bus_stop <= VehicleCalculations.stoppingDistance:
                        # 2.1 THEN causes the vehicle to stop
                        VehicleCalculations.adjustAccelerationToStop(vehicles, i)
                    
                    if vehicles[i]["position"] == busStop[i]["position"]:
                        vehicles[i]["speed"] = 0
                        vehicles[i]["acceleration"] = 0
                    
                    # 3 IF time since vehicle with bus type stopped > waiting time
                    if elapsedTime > busStop[busStopIndex]["waitingtime"]:
                        # 3.1 THEN the vehicle may depart
                        VehicleCalculations.calculateAcceleration(vehicles, i)
    
    # Return the list of vehicles that have interacted with the bus stop with updated attributes
    return vehicles