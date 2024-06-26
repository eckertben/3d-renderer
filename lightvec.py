import numpy as np
from matrices import *

class LightVec():
    def __init__(self, origin, direction, anglex, angley):
        self.origin = np.array(origin[:3])

        self.anglex = anglex
        self.angley = angley

        self.dir = np.array(direction)
        self.change_dir(direction)

        self.min_dist = 100
        self.tri_rend = []
    
    def test_triangle(self, triangle, face):
        vec1, vec2, vec3 = triangle
        vec1 = vec1[:3]
        vec2 = vec2[:3]
        vec3 = vec3[:3]
        norm = np.cross((vec3 - vec1)[:3], (vec2 - vec1)[:3])

        if np.dot(norm, self.dir[:3]) > 0:
            x0, y0, z0 = vec1
            x1, y1, z1 = self.origin
            d1, d2, d3 = self.dir[:3]
            a, b, c = norm
            t = (a*(x0-x1) + b*(y0-y1) + c*(z0-z1)) / (a*d1 + b*d2 + c*d3)
            p = self.origin + (self.dir[:3] * t)

            dist = np.linalg.norm(p)
            if dist < self.min_dist:
                e1 = vec2 - vec1
                e2 = vec3 - vec2
                e3 = vec1 - vec3

                if (np.dot(norm, np.cross(e1, p - vec1)) < 0 and
                    np.dot(norm, np.cross(e2, p - vec2)) < 0 and
                    np.dot(norm, np.cross(e3, p - vec3)) < 0):
                    self.min_dist = min(dist, self.min_dist)
                    self.tri_rend.append((triangle, dist, face))
                    return True
            return False

    def rendered_tri(self):
        for triangle, dist, face in self.tri_rend:
            if dist == self.min_dist:
                return face
            
    def change_dir(self, forward):
        rotate = rotate_x(self.anglex) @ rotate_y(self.angley)
        self.dir = forward @ rotate


