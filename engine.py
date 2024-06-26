import pygame as pg
import numpy as np
from camera import *
from obj3d import *
from projection import *
from circle import Circle
from square import Square
from lightvec import LightVec

WHITE = (255, 255, 255)
BLACK = (0,0,0)

class Rendering:

    def __init__(self):
        pg.init()
        self.SCREEN_W, self.SCREEN_H = 1200, 800
        self.screen = pg.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.surf = pg.surface.Surface((self.SCREEN_W, self.SCREEN_H))
        self.fps = 60
        self.clock = pg.time.Clock()

        self.origin = [0.5, 1, -4]
        self.forward = [0, 0, 1, 1]
        self.create_objects()
        self.create_lightvecs()

    def create_lightvecs(self):
        nlv = 2
        self.lightvecs = []
        self.lightvecs.append(LightVec(self.origin, self.forward, 0, 0))
        '''for i in range(nlv):
            lon = (((i / nlv) * (np.pi))-np.pi/3)/8
            for j in range(nlv):
                lat = (((j / nlv) * (np.pi)) - np.pi/3)/8

                self.lightvecs.append(LightVec(self.origin, self.forward, lon, lat))'''

    def create_objects(self):
        self.camera = Camera(self, self.origin)
        self.projection = Projection(self)
        self.object = []

        ground_arr = np.array([
            [0, 0, 0, 1], [5, 0, 0, 1], [5, 0, 5, 1], [0, 0, 5, 1]
        ])
        ground = Obj3d(self, ground_arr, [[0, 1, 2], [0, 2, 3]], (100, 100, 100))
        self.object.append(ground)

        
        circle = Circle(self, [1, 1, 1, 0], 1, 10, 'grey')
        self.object.append(circle)

        """circle2 = Circle(self, [1, 3, 3, 0], 0.5, 10, 'grey')
        self.object.append(circle2)

        square = Square(self, [1, 0, 1.5, 0], 0.5, pg.Color('blue'))
        self.object.append(square)"""

        self.world_axes = Axes(self)
        self.world_axes.scale(5)
        self.world_axes.translate((0.0001, 0.0001, 0.0001))

    def draw(self):
        self.screen.fill(BLACK)
        self.world_axes.draw()
        for object in self.object:
            object.draw()
        pg.draw.circle(self.screen, pg.Color('white'), 
                       (self.SCREEN_W//2, self.SCREEN_H//2), 6)

    def run(self):
        running = True
        while running:
            self.draw()
            for lightvec in self.lightvecs:
                lightvec.origin = self.camera.pos[:3]
                lightvec.change_dir(self.camera.forward)
                lightvec.min_dist = 100
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.camera.control()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.fps)



if __name__ == "__main__":
    app = Rendering()
    app.run()


