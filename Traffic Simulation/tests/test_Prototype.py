import unittest
from ursina import *
from src.Prototype import *

class TestGraphics(unittest.TestCase):
    def test_road_initalization(self):
        graphics = Graphics("./InputFiles/test.xml")
        
        self.assertTrue(len(graphics.roads_Entity_objects) == 2)
        self.assertTrue(Entity(graphics.roads_Entity_objects[0]).position.y == 0)



    def test_initialize_intersections(self):
        graphics = Graphics("./InputFiles/test.xml")

        self.assertTrue(len(graphics.lights_Entity_objects) == 2)
        self.assertTrue(Entity(graphics.lights_Entity_objects[0]).position.y == Entity(graphics.roads_Entity_objects[0]).position.y)



    def test_add_ambulance_on_click(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        vehicle_count = len(graphics.vehicles)

        graphics.add_ambulance_on_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count + 1)
        vehicle_count += 1



    def test_add_bus_on_click(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        vehicle_count = len(graphics.vehicles)

        graphics.add_bus_on_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count + 1)
        vehicle_count += 1



    def test_add_fire_truck_on_click(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        vehicle_count = len(graphics.vehicles)

        graphics.add_fire_truck_on_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count + 1)
        vehicle_count += 1



    def test_add_police_van_on_click(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        vehicle_count = len(graphics.vehicles)

        graphics.add_police_van_on_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count + 1)
        vehicle_count += 1        



    def test_road_on_click(self):
        graphics = Graphics("./InputFiles/test.xml")

        graphics.road_on_click()
        self.assertTrue(graphics.selectedRoad == "")

        mouse.hovered_entity = Entity(name = "test")
        graphics.road_on_click()
        self.assertTrue(graphics.selectedRoad == "test")
    
    
    
    def test_add_vehicle_button_clicked(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedVehicleType = 'car'

        # Checks no road selected
        vehicle_count = len(graphics.vehicles)
        graphics.on_add_vehicle_button_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count)

        # Checks selected position > road length
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        graphics.selectedPosition = 120
        vehicle_count = len(graphics.vehicles)
        graphics.on_add_vehicle_button_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count)

        # Checks vehicle obstructing
        graphics.selectedPosition = 0
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        graphics.on_add_vehicle_button_click()
        vehicle_count = len(graphics.vehicles)
        graphics.on_add_vehicle_button_click()
        self.assertTrue(len(graphics.vehicles) == vehicle_count)
    
    
    
    def test_add_traffic_light_button_clicked(self):
        graphics = Graphics("./InputFiles/test.xml")

        # Checks traffic light added unsuccessfully due to no selected road
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count)

        # Checks traffic light added to NS road successfully
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count + 1)

        # Checks traffic light added to EW road successfully
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count + 1)

        # Checks traffic light added unsuccessfully due to traffic light to close
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count)

        # Checks traffic light added unsuccessfully due to intersection to close
        graphics.selectedPosition = 50
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count)

        # Checks traffic light added unsuccessfully due to bus stop to close
        graphics.selectedPosition = 75
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count)        

        # Checks traffic light added unsuccessfully due to selected position > road length
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        graphics.selectedPosition = 120
        light_count = len(graphics.lights_Entity_objects)
        graphics.add_traffic_light_button_click()
        self.assertTrue(len(graphics.lights_Entity_objects) == light_count)



    def test_add_bus_stop_button_clicked(self):
        graphics = Graphics("./InputFiles/test.xml")

        # Checks bus stop added unsuccessfully due to no selected road
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count)

        # Checks bus stop added to NS road successfully
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count + 1)

        # Checks bus stop added to EW road successfully
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count + 1)

        # Checks bus stop added unsuccessfully due to traffic light to close
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count)

        # Checks bus stop added unsuccessfully due to intersection to close
        graphics.selectedPosition = 50
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count)

        # Checks bus stop added unsuccessfully due to bus stop to close
        graphics.selectedPosition = 75
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count)        

        # Checks bus stop added unsuccessfully due to selected position > road length
        graphics.selectedRoad = graphics.trafficSystem.road_list[1]
        graphics.selectedPosition = 120
        stop_count = len(graphics.bus_stop_Entity_objects)
        graphics.add_bus_stop_button_click()
        self.assertTrue(len(graphics.bus_stop_Entity_objects) == stop_count)

    
    
    def test_restart_button(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        graphics.add_car_on_click()

        self.assertTrue(len(graphics.vehicles) == 1)

        graphics.on_restart_button_click()

        self.assertTrue(len(graphics.vehicles) == 0)

    def test_update(self):
        graphics = Graphics("./InputFiles/test.xml")
        graphics.selectedRoad = graphics.trafficSystem.road_list[0]
        graphics.selectedPosition = 0
        graphics.add_car_on_click()
        entity_x = Entity(graphics.vehicles[0]).position.x

        app = Ursina()
        update()
        self.assertTrue(graphics.trafficSystem.vehicle_list[0]["position"] != graphics.selectedPosition)
        self.assertTrue(Entity(graphics.vehicles[0]).position.x != entity_x)

if __name__ == '__main__':
    unittest.main()