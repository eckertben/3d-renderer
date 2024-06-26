import numpy as np
from obj3d import Obj3d


class Circle(Obj3d):
    def __init__(self, render, center, radius, num_triangle, color):
        self.radius = radius
        self.nt = num_triangle
        vertexes, faces = self.generate()
        vertexes += np.array(center)
        super().__init__(render, vertexes, faces, color)

    def generate(self):
        vertexes = []
        faces = []
        
        for i in range(self.nt+1):
            lon = ((i / self.nt) * (2*np.pi))
            for j in range(self.nt+1):
                lat = ((j / self.nt) * (2*np.pi))

                xc = self.radius * np.sin(lon) * np.cos(lat)
                yc = self.radius * np.sin(lon) * np.sin(lat)
                zc = self.radius * np.cos(lon)
                vertexes.append([xc, yc, zc, 1])
                
                rowi = ((i) * self.nt) + j
                rowf = ((i + 1) * self.nt) + j
                if rowf <= self.nt ** 2:
                    faces.append([rowf+1, rowi+1, rowi])
                    faces.append([rowi, rowf, rowf+1])
        
        return np.array(vertexes), faces
