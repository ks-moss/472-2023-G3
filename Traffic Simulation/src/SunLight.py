from panda3d.core import DirectionalLight
from ursina import Entity

# SunLight
# custom class for the directional light
# used in GraphicsEngine.py. This replaces 
# Ursinas Directional Light with Pandas3Ds'
# Directional Light instead since that one
# can project shadows
class SunLight(Entity):
    def __init__(self, direction, resolution, focus):
        super().__init__()

        dlight = DirectionalLight('sun')
        dlight.setShadowCaster(True, resolution, resolution)

        # set shadow rendering lens
        lens = dlight.getLens()
        lens.setNearFar(-80, 200)
        lens.setFilmSize((500, 500))

        dlnp = render.attachNewNode(dlight)
        dlnp.lookAt(direction)
        render.setLight(dlnp)
        dlnp.setPos(focus.world_position)