import VehicleCalculations

def calculateVehicleSpeedAndPositionTest(vehicleList: TrafficSystem, vehicleIndex):
    calculateVehicleSpeedAndPosition(vehicleList, 0)

def calculateAccelerationTest(vehicleList: TrafficSystem, vehicleIndex):
    calculateAcceleration(vehicleList, 0)

def adjustDesiredMaxSpeedTest(isSlowingDown):
    adjustDesiredMaxSpeed(True)
    adjustDesiredMaxSpeed(False)

def adjustAccelerationToStopTest(currentSpeed):
    adjustAccelerationToStop(5)

def vehicleOutOfBoundsTest(vehicleList: TrafficSystem, vehicleIndex, roadList: TrafficSystem):
    vehicleOutOfBounds(vehicleList, 0, roadList)
