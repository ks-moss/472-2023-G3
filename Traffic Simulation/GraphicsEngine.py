#2.3
from AutomaticSimulation import *
import random as rng

# importing Ursina Engine
try:
    from ursina import *
    # from ursina.camera import Camera
    from ursina.prefabs.first_person_controller import FirstPersonController
except(e):
    print('Make sure to install Ursina Engine via "pip install ursina"')
    exit()




# Camera Class
# inherits the FirstPersonController from Ursina module
# converts the 1st person camera to 3rd person and modifies the
# default controls to be clamped between the ground at normal of ground
class Camera(FirstPersonController):

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
        camera.clip_plane_near = 0.1

    # Update called every frame of the GraphicsEngine automatically
    # moves the camera rotation based on the mouse only when the mouse
    # is locked which is when the right mouse button is held down
    # mouse will be locked/unlocked in @GraphicsEngine.input
    def update(self):
        if mouse.locked:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
            self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 0)





# Graphics Engine for 2.3 implementation with graphics.
# Using Ursina Engine
# Documentation for the Ursina engine can be found @ https://www.ursinaengine.org/api_reference.html#Ursina
# Make sure to install Ursina before running this file. 'pip install ursina'
# This class creates the window and displays the simulation to the screen.
class GraphicsEngine(Ursina):

    # CLASS VARIABLES
    SCALE = 50             # the size of tiles (ex. 100 = 100x100 units)
    ZOOM_SENSITIVITY = 5

    # Called when the GraphicsEngine class is instantiated
    # this will be a child class of the Ursina game engine
    # setup the window & camera settings
    # then it will start the loading process of the game 'self.start()'
    def __init__(self):
        super().__init__(development_mode=True)
        rng.seed(rng.random())

        # window module settings
        window.title = "Traffic Simulation 3D"
        window.vsync = True
        window.borderless = True
        window.fullscreen = False
        window.exit_button.visible = False
        window.fps_counter.enable = True

        # create custom camera class
        Camera(gravity = 0)

        # create simulation data object
        self.simData = AutomaticSimulation()

        self.createScene()



    # Called after the Ursina engine is setup and 
    # calls the functions that creates the scene up.
    def createScene(self):
        self.createWorldMap()
        self.createEnvironment()



    # Gathers the data from the input file and
    # creates the road layout based on the input.
    # the worldMap field should hold the grid layout of the road.
    def createWorldMap(self):

        # create 2D map with size of the road with maximum length
        self.mapSizeX = ceil(max([r['length'] for r in self.simData.road_list]) / self.SCALE)
        self.mapSizeY = self.mapSizeX
        self.worldMap = [[color.green for _ in range(self.mapSizeX)] for _ in range(self.mapSizeY)]
        self.worldMap[0][0] = ''

        # place roads onto world map randomly
        roads = self.simData.road_list
        croads = self.simData.intersection_list

        # only used in method @createWorldMap
        # places a texture onto the map grid based on the x & y inputs
        # will extend the grid if x | y falls out of bounds
        # parameters:
        #   x       - x position of tile
        #   y       - y position of tile
        #   texture - texture of tile
        #   map     - grid map containing the textures used for the roads
        #   startx  - starting x of a road (changes if map is extended to left)
        #   starty  - starting y of a road (changes if map is extended to down)
        # return:
        #   startx  - same as startx | different if map is expanded
        #   starty  - same as starty | different if map is expanded
        #   map     - updated map with expansions & textures
        def setTile(x, y, texture, map, startx, starty):
            # if x or y out of bounds
            if (x >= self.mapSizeX):                                        # extend right
                for row in range(len(map)): 
                    map[row].extend([color.white])
            elif (x < 0):                                                   # extend left
                for row in range(len(map)): 
                    map[row] = [color.white, *map[row]]
                startx += 1
            if (y >= self.mapSizeY):                                        # extend up
                map = [*map, [color.white for _ in range(self.mapSizeX)]]
            elif (y < 0):                                                   # extend down
                map = [[color.white for _ in range(self.mapSizeX)], *map]
                starty += 1

            self.mapSizeX = len(map[0])
            self.mapSizeY = len(map)
            x = clamp(x, 0, self.mapSizeX)
            y = clamp(y, 0, self.mapSizeY)

            map[y][x] = texture
            return startx, starty, map

        #TODO add method for shrinking map for empty rows or columns

        # create intersections
        for i in croads:
            ix = rng.randint(0, self.mapSizeX)
            iy = rng.randint(0, self.mapSizeY)
            setTile(ix, iy, color.black, self.worldMap, ix, iy)

            # create roads for those intersections
            for iroad in [0, 1]:
                # find road in road list
                for r in roads:
                    if r['name'] == i[iroad]['road']:
                        road = r
                        break
                
                # get the length of the road split by the intersection
                frontDist = (road['length'] - i[iroad]['position']) // self.SCALE
                backDist = i[iroad]['position'] // self.SCALE

                # place road behind intersection
                for n in range(1, backDist - 1):
                        ix, iy, self.worldMap = setTile(ix if iroad else ix - n, 
                                                        (iy - n) if iroad else iy, 
                                                        color.blue if iroad else color.red, 
                                                        self.worldMap, ix, iy)

                # place road ahead intersection
                for n in range(1, frontDist - 1):
                        ix, iy, self.worldMap = setTile(ix if iroad else ix + n, 
                                                        (iy + n) if iroad else iy, 
                                                        color.blue if iroad else color.red, 
                                                        self.worldMap, ix, iy)
            
            #TODO add remaining roads

    # Creates the environment of the scene (Sky, Fog, Terrain, Roads)
    # Uses the worldMap field to create the road layout
    # createWorldMap function must be called before this function
    def createEnvironment(self):
        # terrain
        self.terrain = Entity(model = 'quad', 
                              scale = (self.mapSizeX*200, self.mapSizeX*200, 0), 
                              position = (0, -1, 0), 
                              texture = 'grass', 
                              rotation_x = 90)
        self.terrain.texture_scale = Vec2(50, 50)


        # create roads
        for x in range(self.mapSizeX):
            for y in range(self.mapSizeY):
                if self.worldMap[y][x] != '':
                    Entity( model = 'quad', 
                            scale = self.SCALE, 
                            x = (self.mapSizeX // 2 - x) * self.SCALE,
                            y = 0,
                            z = (self.mapSizeY // 2 - y) * self.SCALE, 
                            rotation_x = 90, 
                            color = self.worldMap[y][x],
                            # texture = self.worldMap[x][z], <-- we will use this in final implementation
                            collider = None)
        

        # sky
        scene.fog_density = 0.001
        Sky()



    # Called when an input is given to the application on key down.
    # parameters:
    #   key -   the value that is inputted from the keyboard or mouse.
    #       keybinds:
    #           'esc'       -   quits & closes the app
    #           'wheel_up'  -   zooms in
    #           'wheel_down'-   zooms out
    #           'mouse3'    -   rmb : locks mouse
    def input(self, key, is_raw=False):
        match key:
            case 'mouse1':
                quit()
            case Keys.escape:
                quit()
            case 'wheel_up':
                camera.y -= self.ZOOM_SENSITIVITY
            case 'wheel_down':
                camera.y += self.ZOOM_SENSITIVITY
            case 'mouse3':
                mouse.position = Vec3(0, 0, 0)
                mouse.locked = True



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
    simulation.run()