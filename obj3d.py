import pygame as pg
from matrices import *
from circle import *

class obj3d():
    def __init__(self, render, vertexes, faces):
        self.render = render
        self.vertexes = vertexes
        self.faces = faces
        self.color_faces = [(pg.Color('white'), face) for face in self.faces]
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.label = ''
        self.draw_vertices = False
        self.lines = False

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0

        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]
        
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]
            if self.lines: thick = 3
            else: thick = 0
            if not np.any((polygon == self.render.SCREEN_H // 2) | 
                          (polygon == self.render.SCREEN_W // 2)):
                pg.draw.polygon(self.render.screen, color, polygon, thick)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])
        
        if self.draw_vertices:
            for vertex in vertexes:
                if not np.any((vertex == self.render.SCREEN_H // 2) | 
                            (vertex == self.render.SCREEN_W // 2)):
                    pg.draw.circle(self.render.screen, 
                                    pg.Color("white"), vertex, 6)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)
    
    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)
    
    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)
    
    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)
    
    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)


class Axes(obj3d):
    def __init__(self, render):
        super().__init__(render, 
                         vertexes=np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]), 
                         faces=np.array([(0, 1, 0, 1), (0, 2, 0, 2), (0, 3, 0, 3)]))
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.lines = True
        self.label = 'XYZ'
