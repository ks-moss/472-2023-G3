import unittest
from src.AutomaticSimulation import *

class TestAutomaticSimulation(unittest.TestCase):
	def test_initialization_makes_traffic_sytem(self):
		automaticSimulation = AutomaticSimulation("InputFiles/test.xml")
		self.assertTrue(automaticSimulation.trafficSystem != None)
	def test_initialization_has_filename(self):
		automaticSimulation = AutomaticSimulation("InputFiles/test.xml")
		self.assertTrue(automaticSimulation.filename == "InputFiles/test.xml")
	def test_initialization_fixes_no_filename(self):
		automaticSimulation = AutomaticSimulation("")
		self.assertTrue(automaticSimulation.filename == "InputFiles/prototype2.xml")

if __name__ == '__main__':
	unittest.main()