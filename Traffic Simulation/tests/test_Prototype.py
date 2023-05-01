import unittest
from ursina import *
from src.Prototype import *

class TestGraphics(unittest.TestCase):
    def test_road_initalization(self):
        graphics = Graphics("./InputFiles/test.xml")

        print(graphics.roads_Entity_objects)
        
        self.assertTrue(len(graphics.roads_Entity_objects) == 2)
        self.assertTrue(Entity(graphics.roads_Entity_objects[0]).position.y == 0)

    def test_restart_button(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        graphics.add_car_on_click()

        self.assertTrue(len(graphics.vehicles) == 1)

        graphics.on_restart_button_click()

        self.assertTrue(len(graphics.vehicles) == 0)

if __name__ == '__main__':
    unittest.main()