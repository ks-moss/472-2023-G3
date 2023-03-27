from ursina import *

class GraphicsEngine(Ursina):

    # FIELD VARIABLES
    MAP_SIZE = 20   # should automatically be set to longest road
    SCALE = 100     # the size of tiles
    worldMap = []   # holds the texture values of the map tiles

    # Called when the GraphicsEngine class is instantiated
    # this will be a child class of the Ursina game engine
    # setup the window & camera settings
    # then it will start the loading process of the game 'self.start()'
    # Documentation for the Ursina engine can be found @ https://www.ursinaengine.org/api_reference.html#Ursina
    def __init__(self):
        super().__init__()
        # editor camera module settings
        eCamera = EditorCamera()
        eCamera.pan_speed = Vec2(5, 0)

        # window module settings
        window.title = "Traffic Simulation 3D"
        window.vsync = True
        window.borderless = True
        # window.fullscreen = True
        window.exit_button.visible = False

        # camera module settings
        camera.position = (0, 40, self.MAP_SIZE/-1.5)
        camera.fov = 120
        camera.clip_plane_near = 0.1

        self.start()

    # Creates the environment of the scene (Sky, Fog, Terrain)
    # Uses the worldMap field to create the road layout
    # createWorldMap function must be called before this function
    def createEnvironment(self):
        for x in range(self.MAP_SIZE):
            for z in range(self.MAP_SIZE):
                if self.worldMap[x][z] != '':
                    Entity(model='quad', scale=self.SCALE, position=(x - (self.MAP_SIZE//2), 0, z - (self.MAP_SIZE//2)), rotation_x=90, texture=self.worldMap[x][z])
        
        terrain = Entity(model='quad', scale=self.MAP_SIZE*100, position=(0, -0.05, 0), texture='grass', rotation_x=90)
        terrain.texture_scale = Vec2(10, 10)
        camera.look_at(terrain)

        scene.fog_density = (50, 200)
        Sky()

    # Gathers the data from the input file and
    # creates the road layout based on the input.
    # the worldMap field should hold the grid layout of the road.
    def createWorldMap(self):
        self.worldMap = [['' for _ in range(self.MAP_SIZE)] for _ in range(self.MAP_SIZE)]

    # Called after the Ursina engine is setup and 
    # calls the functions that creates the scene up.
    def start(self):
        self.createWorldMap()
        self.createEnvironment()

    # Called when an input is given to the application.
    # parameters:
    #   key -   the value that is inputted from the keyboard or mouse.
    #       keybinds:
    #           'backspace' -   quits & closes the game
    def input(self, key):
        if key == Keys.backspace:
            quit()


# Start simulation by running this file
if __name__ == "__main__":
    simulation = GraphicsEngine()
    simulation.run()