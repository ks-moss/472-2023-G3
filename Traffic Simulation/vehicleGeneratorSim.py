# 3.4
from automaticSim import *
from VehicleCalculations import *
 
class VehicleGeneratorSimulator:

    def __init__(self):
        self.AutomaticSimulation = AutomaticSimulation()

    def simulator(self):
        '''
        3. FOR any vehicle generator
        3.1 IF time since last vehicle > frequency
        3.1.1 IF no vehicle on road between positions 0 and 2l 3.1.1.1 THEN add vehicle to road at position 0
        '''

       # for i in range(len(self.AutomaticSimulation.generated_vehicles)):

