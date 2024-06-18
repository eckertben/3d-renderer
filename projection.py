import math
import numpy as np

class Projection:
    def __init__(self, render):
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = math.tan(render.camera.FOV_H / 2)
        LEFT = -RIGHT
        TOP = math.tan(render.camera.FOV_V / 2)
        BOTTOM = -TOP

        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * (NEAR * FAR) / (FAR - NEAR)
        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        self.to_screen_matrix = np.array([
            [render.SCREEN_W // 2, 0, 0, 0],
            [0, -render.SCREEN_H // 2, 0, 0],
            [0, 0, 1, 0],
            [render.SCREEN_W // 2, render.SCREEN_H // 2, 0, 1]
        ])