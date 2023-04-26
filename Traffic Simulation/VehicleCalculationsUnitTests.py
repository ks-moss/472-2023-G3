import unittest
import VehicleCalculations

class TrafficSimulationTest(unittest.TestCase):

    def setUp(self):
        # Load sample data for testing
        with open('./InputFiles/vehicles.json') as f:
            self.data = VehicleCalculations.json.load(f)
        self.list_of_objects = list(self.data)
        self.vehicleType = {"car": 0, "bus": 1, "fire truck": 2, "ambulance": 3, "police van": 4}
        self.absoluteMaxSpeed = 16.6
        self.simulationTime = 0.0166
        self.decelerationDistance = 50
        self.stoppingDistance = 15
        self.delayFactor = 0.4

    # Test for correct calculation of speed and position of a vehicle
    def test_calculateVehicleSpeedAndPosition(self):
        vehicleList = VehicleCalculations.TrafficSystem()
        vehicleList.Append({"type": "car", "speed": 10, "position": 0, "acceleration": 0, "road": 1})
        vehicleIndex = 0

        VehicleCalculations.calculateVehicleSpeedAndPosition(vehicleList, vehicleIndex)

        expected_speed = 10  # Initial speed
        expected_position = 0.166  # Initial position + (speed * simulationTime) + (0.5 * acceleration * simulationTime^2)
        
        self.assertAlmostEqual(vehicleList[vehicleIndex]["speed"], expected_speed, places=2)
        self.assertAlmostEqual(vehicleList[vehicleIndex]["position"], expected_position, places=2)

    # Test for correct calculation of acceleration of a vehicle
    def test_calculateAcceleration(self):
        vehicleList = VehicleCalculations.TrafficSystem()
        vehicleList.Append({"type": "car", "speed": 10, "position": 0, "acceleration": 0, "road": 1})
        vehicleIndex = 0

        VehicleCalculations.calculateAcceleration(vehicleList, vehicleIndex)

        expected_acceleration = -0.96  # Max acceleration * (1 - (speed / maxSpeed)^4 - vehicleInteraction^2)
        
        self.assertAlmostEqual(vehicleList[vehicleIndex]["acceleration"], expected_acceleration, places=2)

    # Test for correct adjustment of desired maximum speed of vehicles
    def test_adjustDesiredMaxSpeed(self):
        isSlowingDown = True

        VehicleCalculations.adjustDesiredMaxSpeed(isSlowingDown)

        expected_maximum_speed = 6.64  # delayFactor * absoluteMaxSpeed
        
        self.assertAlmostEqual(VehicleCalculations.maximumSpeed, expected_maximum_speed, places=2)

if __name__ == '__main__':
    unittest.main()
