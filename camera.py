import pygame as pg
from matrices import *

class Camera:
    def __init__(self, render, pos):
        self.render = render
        self.pos = np.array([*pos, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        
        self.near_plane = 0.1
        self.far_plane = 100.0
        self.FOV_H = np.pi/4
        self.FOV_V = self.FOV_H * self.render.SCREEN_H / self.render.SCREEN_W

        self.move = 0.02
        self.rotation_speed = 0.01

        self.angleX = 0
        self.angleY = 0

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.pos -= self.right * self.move
        if key[pg.K_d]:
            self.pos += self.right * self.move
        if key[pg.K_w]:
            self.pos += self.forward * self.move
        if key[pg.K_s]:
            self.pos -= self.forward * self.move
        if key[pg.K_e]:
            self.pos += self.up * self.move
        if key[pg.K_q]:
            self.pos -= self.up * self.move
        
        if key[pg.K_LEFT]:
            self.angleY -= self.rotation_speed
        if key[pg.K_RIGHT]:
            self.angleY += self.rotation_speed
        if key[pg.K_UP]:
            self.angleX -= self.rotation_speed
        if key[pg.K_DOWN]:
            self.angleX += self.rotation_speed
    

    def reset_axes(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axes(self):
        rotate = rotate_x(self.angleX) @ rotate_y(self.angleY)
        self.reset_axes()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate
            

    def translate_matrix(self):
        x, y, z, w = self.pos

        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
    
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        ux, uy, uz, w = self.up
        fx, fy, fz, w = self.forward

        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self):
        self.camera_update_axes()
        return self.translate_matrix() @ self.rotate_matrix()