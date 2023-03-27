try:
    from ursina import *
    from ursina.prefabs.first_person_controller import FirstPersonController
except(e):
    print('Make sure to install Ursina Engine via "pip install ursina"')
    exit()

# Graphics Engine for 2.3 implementation with graphics.
# Using Ursina Engine
# Documentation for the Ursina engine can be found @ https://www.ursinaengine.org/api_reference.html#Ursina
# Make sure to install Ursina before running this file. 'pip install ursina'
# This class creates the window and displays the simulation to the screen.
class GraphicsEngine(Ursina):

    # FIELD VARIABLES
    MAP_SIZE = 20    # should automatically be set to longest road
    SCALE = 100     # the size of tiles (ex. 100 = 100x100 units)
    worldMap = []   # holds the texture values of the map tiles
    terrain = None

    # Called when the GraphicsEngine class is instantiated
    # this will be a child class of the Ursina game engine
    # setup the window & camera settings
    # then it will start the loading process of the game 'self.start()'
    def __init__(self):
        super().__init__(development_mode=True)
        # editor camera module settings
        eCamera = EditorCamera()

        # window module settings
        window.title = "Traffic Simulation 3D"
        window.vsync = True
        window.borderless = True
        window.fullscreen = False
        window.exit_button.visible = False
        window.fps_counter.enable = True

        # camera module settings
        fpController = FirstPersonController(gravity=0, cursor=Entity(), height=5)
        camera.rotation = (90, 0, 0)
        camera.origin_y = 100
        camera.position = (0, 100, 0)
        camera.fov = 120
        camera.clip_plane_near = 0.1
        mouse.locked = False

        self.start()

    # Called after the Ursina engine is setup and 
    # calls the functions that creates the scene up.
    def start(self):
        self.createWorldMap()
        self.createEnvironment()

    # Gathers the data from the input file and
    # creates the road layout based on the input.
    # the worldMap field should hold the grid layout of the road.
    def createWorldMap(self):
        self.worldMap = [['' for _ in range(self.MAP_SIZE)] for _ in range(self.MAP_SIZE)]

    # Creates the environment of the scene (Sky, Fog, Terrain)
    # Uses the worldMap field to create the road layout
    # createWorldMap function must be called before this function
    def createEnvironment(self):
        # create roads
        for x in range(self.MAP_SIZE):
            for z in range(self.MAP_SIZE):
                self.worldMap[x][z] != '' and Entity(model = 'quad', 
                                                     scale = self.SCALE, 
                                                     position = (x - (self.MAP_SIZE//2), 0, z - (self.MAP_SIZE//2)), 
                                                     rotation_x = 90, 
                                                     texture = self.worldMap[x][z])
        
        # terrain
        self.terrain = Entity(model = 'quad', 
                              scale = (self.MAP_SIZE*100, self.MAP_SIZE*100, 0), 
                              position = (0, -0.05, 0), 
                              texture = 'grass', 
                              rotation_x = 90)
        self.terrain.texture_scale = Vec2(10, 10)
        # camera.look_at(self.terrain)

        # sky
        scene.fog_density = 0.005
        Sky()

    # Called when an input is given to the application.
    # parameters:
    #   key -   the value that is inputted from the keyboard or mouse.
    #       keybinds:
    #           'backspace' -   quits & closes the game
    def input(self, key, is_raw=False):
        match key:
            case Keys.backspace:
                quit()
            case 'a':
                camera.x -= 0.1
        
        camera.x -= held_keys['a'] + 0.1
        print(key, held_keys[key])



# Start simulation by running this file
if __name__ == "__main__":
    simulation = GraphicsEngine()
    simulation.run()

def update():
    print(held_keys)