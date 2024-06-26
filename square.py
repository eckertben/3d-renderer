import numpy as np
from obj3d import Obj3d

class Square(Obj3d):
    def __init__(self, render, center, size, color):
        self.center = center
        vertexes = np.array([
            (0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
            (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1),
        ])
        vertexes = vertexes * size + np.array([center])
        
        faces = np.array([
            (0, 1, 2), (0, 3, 2), (4, 5, 6), (4, 7, 6), (0, 1, 5), (1, 5, 4),
            (2, 3, 7), (2, 7, 6), (1, 2, 6), (1, 6, 5), (0, 3, 7), (0, 7, 4)
        ])
        super().__init__(render, vertexes, faces, color)