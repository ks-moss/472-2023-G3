from TrafficSimulation2 import TrafficSystem
import math

class MovingVehicle:
    
    def __init__(self):


        self.trafficSystem = TrafficSystem()
        self.trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")

        self.vehicles = self.trafficSystem.vehicleList

        # Appendix B.6 - Default Values
        self.length = 4
        self.maximumSpeed = 16.6
        self.absoluteMaxSpeed = 16.6
        self.maximumAcceleration = 1.44
        self.maximumBrakingFactor = 4.61
        self.minimumFollowingDistance = 4
        self.simulationTime = 0.0166
        self.decelerationDistance = 50
        self.stoppingDistance = 15
        self.delayFactor = 0.4

        # Calculate the New Speed and Position of Vehicle
        # parameters:
        #   vehicleIndex - The index of the vehicle inside of the list
        #   currentSpeed - The current speed of the vehicle being calculated
        #   currentAcceleration - The current acceleration of the vehicle being calculated
        # returns:
        #   speed - The new speed of the vehicle
        #   position - The new position of the vehicle
    def calculateVehicleSpeedAndPosition(self, vehicleIndex, currentSpeed, currentAcceleration):
        vehicle = self.vehicles[vehicleIndex]
        speed = currentSpeed
        position = vehicle["position"]
        acceleration = currentAcceleration
        if (speed + acceleration*self.simulationTime) < 0:
            position = position - (speed*speed)/2*acceleration
            speed = 0
        else:
            speed = speed + acceleration*self.simulationTime
            position = position + (speed*self.simulationTime) + acceleration*((self.simulationTime*self.simulationTime)/2)

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
    def calculateAcceleration(self, vehicleIndex, currentSpeed, currentFrontSpeed):
        try:
            frontVehicle = self.vehicles[vehicleIndex - 1]
        except NameError:
            vehicleExists = False
        else:
            vehicleExists = True

        backVehicle = self.vehicles[vehicleIndex]  

        speed = currentSpeed

        positionDifference = frontVehicle["position"] - backVehicle["position"] - self.length
            
        # print("Front Vehicle Position ", frontVehicle["position"])
        # print("Back Vehicle Position ", backVehicle["position"])
        # print("Position Difference ", positionDifference)

        speedDifference = speed - currentFrontSpeed

        if(vehicleExists == True):
            vehicleInteration = ((self.minimumFollowingDistance + max(0, speed + ((speed*speedDifference)/(2*math.sqrt(self.maximumAcceleration*self.maximumBrakingFactor)))))/positionDifference)
        else:
            vehicleInteration = 0
            
        acceleration = self.maximumAcceleration*(1 - (speed/self.maximumSpeed)**4 - vehicleInteration**2)

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
    def adjustDesiredMaxSpeed(self, isSlowingDown):
        if (isSlowingDown):
            # Eq:  v_max = sV_max
            maximumSpeed = self.delayFactor*self.absoluteMaxSpeed
        else:
            # Eq:  v_max = V_max
            maximumSpeed = self.absoluteMaxSpeed

        #DEBUG
        # print("Max Speed set to: ", maximumSpeed)

    # Sets the acceleration in each simulation step according to the
    # current speed of the vehicle. This function should be called for 
    # each simulation step when stopping a vehicle
    # parameters:
    #   currentSpeed - the speed of the current vehicle being calculated
    # return:
    #   acceleration - the new acceleration of the vehicle
    def adjustAccelerationToStop(self, currentSpeed):
        # Eq:  a = -(b_max*v / v_max)
        acceleration = -1 * ((self.maximumBrakingFactor * currentSpeed) / self.maximumSpeed)

        #DEBUG
        # print("Acceleration Set to: ", acceleration)

        return acceleration


movingVehicle = MovingVehicle()
movingVehicle.calculateVehicleSpeedAndPosition(0,16,1)
movingVehicle.calculateAcceleration(0,16,16)
movingVehicle.adjustDesiredMaxSpeed(isSlowingDown=True)
movingVehicle.adjustAccelerationToStop(16.6)