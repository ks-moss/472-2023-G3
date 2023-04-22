#2.3
# importing Ursina Engine
try:
    from ursina import *
    from ursina.shaders import lit_with_shadows_shader
    from ursina.prefabs.first_person_controller import FirstPersonController
    
except Exception as e:
    print('Make sure to install Ursina Engine via "pip install ursina"', e)
    exit()
    
# source modules
from AutomaticSimulation import AutomaticSimulation
from src.RoadGen import RoadGen
from src.VehicleFactory import VehicleFactory
from src.TrafficLights import TrafficLights
from src.SunLight import SunLight

# python modules
from types import MethodType
from threading import Thread



# what to do next
#TODO add vehicle generator
#TODO clean and reset scene
#TODO 4.1 GUI for simulation
#TODO 4.2 GUI for traffic lights
#TODO 4.3 GUI for vehicle generator


# Camera Class
# inherits the FirstPersonController from Ursina module
# converts the 1st person camera to 3rd person and modifies the
# default controls to be clamped between the ground at normal of ground
class Camera(FirstPersonController):

    CAM_SPEED = 50

    # Called when instantiated in @GraphicsEngine.__init__
    # modifies the default FirstPersonController fields
    # and mouse settings
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor.color = color.rgba(0, 0, 0, 0)
        mouse.locked = False

        # default camera rotation
        self.rotation_y = -45
        self.camera_pivot.rotation_x = -45
        
        # global camera settings
        camera.rotation_x = 90
        camera.y = 100  # distance from origin
        camera.fov = 120
        self.focusTimer = 0
    

    # called when the left mouse button is clicked
    # checks to see if the mouse is clicking on a road
    # if there is a collision then the target x&z values are 
    # updated to the entities position
    # the focus timer is reset to 0
    def focus(self):
        mouse.find_collision()
        if len(mouse.collisions) == 0:
            return
        
        self.targetx = mouse.collisions[0].entity.world_x
        self.targetz = mouse.collisions[0].entity.world_z
        self.focusTimer = self.CAM_SPEED
        self.oldx = self.x
        self.oldz = self.z



    # Update called every frame of the GraphicsEngine automatically
    # moves the camera rotation based on the mouse only when the mouse
    # is locked which is when the right mouse button is held down
    # mouse will be locked/unlocked in @GraphicsEngine.input
    #
    # if the focus timer is < 100 it will update the cameras position
    # to the target position within 100 frame updates.
    def update(self):
        if mouse.locked:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
            self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 0)

        if self.focusTimer > 0:
            self.focusTimer -= 1
            t = self.focusTimer / self.CAM_SPEED
            self.x = lerp(self.targetx, self.oldx, t)
            self.z = lerp(self.targetz, self.oldz, t)
        


# Graphics Engine for 2.3 implementation with graphics.
# Using Ursina Engine
# Documentation for the Ursina engine can be found @ https://www.ursinaengine.org/api_reference.html#Ursina
# Make sure to install Ursina before running this file. 'pip install ursina'
# This class creates the window and displays the simulation to the screen.
class GraphicsEngine(Ursina):

    # CLASS VARIABLES
    ROAD_WIDTH = 6         # block size of road (ex. 50 => road.len = 100 => 2 blocks)
    ZOOM_SENSITIVITY = 10    # sensitivity of zoooooom

    # Called when the GraphicsEngine class is instantiated
    # this will be a child class of the Ursina game engine
    # setup the window & camera settings
    # then it will start the loading process of the game 'self.start()'
    def __init__(self):
        super().__init__(development_mode=True)

        # window module settings
        window.title = "Traffic Simulation 3D"
        window.vsync = True
        window.borderless = False
        window.fullscreen = False
        window.exit_button.disable()
        window.fps_counter.disable()
        window.cog_button.disable()

        # create custom camera class
        self.cam = Camera(gravity = 0)

        # create simulation data object
        self.simData = AutomaticSimulation("./InputFiles/trafficSim3.xml")

        self.createScene()



    # Called after the Ursina engine is setup and 
    # calls the functions that creates the scene up.
    def createScene(self):
        Entity.default_shader = lit_with_shadows_shader
        try:
            thread = Thread(target = self.load_assets, args = '')
            thread.start()
        except Exception as e:
            print("error starting thread", e)
        self.createEnvironment()
        self.createWorldMap()
        thread.join()
        self.addDefaultVehicles()
        self.createTrafficLights()

    
    def load_assets(self):
        models = ['bus.glb', 'firetruck.glb', 'policecar.glb', 'sedan.glb', 'trafficlight.glb']
        for m in models:
            load_model(m)



    # Gathers the data from the input file and
    # creates the road layout based on the input.
    # the worldMap field should hold the grid layout of the road.
    def createWorldMap(self):
        RoadGen.roadWidth = self.ROAD_WIDTH
        self.Map = RoadGen(self.simData)
        self.Map.placeRoads()
        self.startingPoints = self.Map.startingPoints




    # Creates the environment of the scene (Sky, Fog, Terrain, Roads)
    # Uses the worldMap field to create the road layout
    # createWorldMap function must be called before this function
    def createEnvironment(self):
        # terrain
        self.terrain = Entity(model = 'quad', 
                              scale = (10000, 10000, 0), 
                              position = (0, 0, 0), 
                              texture = 'softgrass', 
                              rotation_x = 90,
                              collider = None)
        self.terrain.texture_scale = Vec2(100, 100)

        # sky
        sun = SunLight(direction = (-0.7, -0.9, 0.5),
                       resolution= 3072 * 4,
                       focus = self.terrain)
        scene.fog_density = 0.002
        Sky()
    
    
    # addDefaultVehicles
    # creates a VehicleFactory object and adjusts the 
    # necessary static fields. The object
    # should automatically create the starting vehicles
    # from the AutomaticSimulation class
    def addDefaultVehicles(self):
        self.vFactory = VehicleFactory(self.simData, self.startingPoints)
        self.vFactory.createInitVehicles()



    def createTrafficLights(self):
        self.trafficLights = TrafficLights(self.simData, self.startingPoints)
        self.trafficLights.createTrafficLights()


    # resetSimulation
    # called when the user wants to reset the simulation and start over
    # it resets the map and creates a new scene for the simulation
    def resetSimulation(self):
        del self.Map
        for obj in self.sceneObjs:
            destroy(obj)
        destroy(self.terrain)
        self.cam.x, self.cam.z = 0, 0

        print('scene cleared')
        self.createScene()



    # Called when an input is given to the application on key down.
    # parameters:
    #   key -   the value that is inputted from the keyboard or mouse.
    #       keybinds:
    #           'mouse1'    -   sets focus to a road tile
    #           'esc'       -   quits & closes the app
    #           'wheel_up'  -   zooms in
    #           'wheel_down'-   zooms out
    #           'mouse3'    -   rmb : locks mouse
    def input(self, key, is_raw=False):
        match key:
            case 'mouse1':
                self.cam.focus()
            case Keys.escape:
                quit()
            case 'wheel_up':
                if camera.y > 1:
                    camera.y -= self.ZOOM_SENSITIVITY
            case 'wheel_down':
                camera.y += self.ZOOM_SENSITIVITY
            case 'mouse3':
                mouse.position = Vec3(0, 0, 0)
                mouse.locked = True
            case 'r':
                self.resetSimulation()



    # Called when an input is given to the application on key up
    # parameters:
    #   key -   the value that is inputted from the keyboard or mouse.
    #       keybinds:
    #           'mouse3' -  rmb : unlocks mouse
    def input_up(self, key, is_raw=False):
        match key:
            case 'mouse3':
                mouse.locked = False



# Start simulation by running this file
if __name__ == "__main__":
    simulation = GraphicsEngine()
    # simulation.wireframe_on()
    simulation.run()