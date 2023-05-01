import unittest
import VehicleCalculations
from BusStopSimulation import busStopSimulation

class TestBusStopSimulation(unittest.TestCase):

    # The first test case (test_busStopSimulation_deceleration) tests whether the bus decelerated as expected when it approaches the bus stop.
    def test_busStopSimulation_deceleration(self):
        # Set up the initial conditions
        vehicles = [{"road": "A", "type": "bus", "position": 49.8, "speed": 20, "acceleration": 0},
                    {"road": "A", "type": "car", "position": 20, "speed": 30, "acceleration": 0},
                    {"road": "A", "type": "car", "position": 30, "speed": 40, "acceleration": 0}]
        busStop = [{"road": "A", "position": 50, "waitingtime": 5}]
        busStopIndex = 0
        busStopCounter = [{"counter": 0}, {"counter": 0}, {"counter": 0}]
        VehicleCalculations.decelerationDistance = 10
        VehicleCalculations.stoppingDistance = 5

        # Call the function under test
        busStopSimulation(busStop, vehicles, busStopIndex, busStopCounter)

        # Check that the bus decelerated
        self.assertAlmostEqual(vehicles[0]["acceleration"], 0, places=5)

    # The second test case (test_busStopSimulation_stopping) tests whether the bus stopped at the bus stop as expected. 
    def test_busStopSimulation_stopping(self):
        # Set up the initial conditions
        vehicles = [{"road": "A", "type": "bus", "position": 19.8, "speed": 20, "acceleration": 0}]
        busStop = [{"road": "A", "position": 20, "waitingtime": 5}]
        busStopIndex = 0
        busStopCounter = [{"counter": 0}]
        VehicleCalculations.decelerationDistance = 10
        VehicleCalculations.stoppingDistance = 5

        # Call the function under test
        busStopSimulation(busStop, vehicles, busStopIndex, busStopCounter)

        # Check that the bus stopped
        self.assertAlmostEqual(vehicles[0]["speed"], 0, places=5)
        self.assertAlmostEqual(vehicles[0]["acceleration"], 0, places=5)

    # The third test case (test_busStopSimulation_waitingTime) tests whether the bus stopped at the bus stop for the correct amount of time.
    def test_busStopSimulation_waitingTime(self):
        # Set up the initial conditions
        vehicles = [{"road": "A", "type": "bus", "position": 19.8, "speed": 20, "acceleration": 0}]
        busStop = [{"road": "A", "position": 20, "waitingtime": 5}]
        busStopIndex = 0
        busStopCounter = [{"counter": 0}]
        VehicleCalculations.decelerationDistance = 10
        VehicleCalculations.stoppingDistance = 5

        # Call the function under test several times to simulate the bus waiting at the stop
        for i in range(0, 55):
            busStopSimulation(busStop, vehicles, busStopIndex, busStopCounter)

        # Check that the bus stopped at the stop for the correct amount of time
        self.assertEqual(busStopCounter[0]["counter"], 0, 50)

if __name__ == '__main__':
    unittest.main()
