import pygame as pg
from matrices import *

class Obj3d():
    def __init__(self, render, vertexes=np.array([]), faces=np.array([]), color=pg.Color('white')):
        self.render = render
        self.vertexes = vertexes
        self.faces = faces
        self.color_faces = [(color, face) for face in self.faces]
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.label = ''
        self.draw_vertices = False
        self.lines = False
        self.is_axis = False

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 4) | (vertexes < -4)] = 0

        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for color, face in self.color_faces:
            tri = vertexes[face]
            pg.draw.polygon(self.render.screen, color, tri, 0)
            pg.draw.polygon(self.render.screen, pg.Color("black"), tri, 1)

        for lightvec in self.render.lightvecs:
            for color_face in self.color_faces:
                color, face = color_face
                triangle = self.vertexes[face]
                lightvec.test_triangle(triangle, face)

            rend_face = lightvec.rendered_tri()
            if (rend_face is not None):
                rend_tri = vertexes[rend_face] 
                if not np.any((rend_tri == self.render.SCREEN_H // 2) | 
                            (rend_tri == self.render.SCREEN_W // 2)):
                    pg.draw.polygon(self.render.screen, pg.Color('red'), rend_tri, 0)
                    pg.draw.polygon(self.render.screen, pg.Color("black"), rend_tri, 1)
                    if self.draw_vertices:
                        for vertex in rend_tri:
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


class Axes(Obj3d):
    def __init__(self, render):
        super().__init__(render)
        self.vertexes = np.array([
                (0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)
            ])
        self.faces = np.array([
                (0, 1), (0, 2), (0, 3)
            ])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.lines = True
        self.label = 'XYZ'
        self.is_axis = True
    
    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 8) | (vertexes < -8)] = 0

        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            line = vertexes[face]
            if not np.any((line == self.render.SCREEN_H // 2) | 
                          (line == self.render.SCREEN_W // 2)):
                start, end = line
                pg.draw.line(self.render.screen, color, start, end, 2)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, line[-1])
