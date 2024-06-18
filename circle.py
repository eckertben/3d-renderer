import numpy as np


class Circle():
    def __init__(self, center, radius, num_triangle):
        self.center = center
        self.radius = radius
        self.nt = num_triangle
        self.vertexes = np.array([])
        self.faces = np.array([])

    def generate(self):
        vertexes = []
        faces = []
        
        for i in range(self.nt+1):
            lon = ((i / self.nt) * (2*np.pi)) - (np.pi/2)
            for j in range(self.nt+1):
                lat = ((j / self.nt) * (2*np.pi)) - (np.pi/2)

                xc = self.radius * np.sin(lon) * np.cos(lat)
                yc = self.radius * np.sin(lon) * np.sin(lat)
                zc = self.radius * np.cos(lon)
                vertexes.append([xc, yc, zc, 1])
                
                if ((i+1)*self.nt) + j+2 <= self.nt ** 2:
                    faces.append([(i* self.nt)+j, (i * self.nt)+j+1, ((i+1)*self.nt)+j+1, ((i+1)*self.nt)+j+2])
        self.vertexes = np.array(vertexes)
        self.faces = faces
        print(faces)

    def loc(self):
        self.vertexes -= np.array(self.center)
