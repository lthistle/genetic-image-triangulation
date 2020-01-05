from scipy.spatial import Delaunay
from matplotlib.image import imread
import matplotlib.pyplot as plt
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import cv2
import mahotas
all_points = set()
dupe_points = set()
class Triangulation:
    def __init__(self, num_points, width, height):
        x_coords = np.random.randint(width, size=(num_points, 1))
        y_coords = np.random.randint(height, size=(num_points, 1))
        points = np.hstack((x_coords, y_coords))
        self.points = np.append(points, np.array([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]]), axis=0)
        self.triangles = self.points[Delaunay(self.points).simplices]

    def retriangulate(self):
        self.triangles = self.points[Delaunay(self.points).simplices]

    def calculate_error(self, img):
        for t in self.triangles:    
            min_x, min_y = np.amin(t, axis=0)
            max_x, max_y = np.amax(t, axis=0)
            x_size = max_x - min_x + 1
            y_size = max_y - min_y + 1  

            #create a mask
            new_tri = [(x - min_x, y - min_y) for (x,y) in t]
            grid = np.zeros((x_size, y_size), dtype=np.int8)
            mahotas.polygon.fill_polygon(new_tri, grid)

            #cut the bounding box of the image we're working with
            box = img[min_x:max_x + 1,min_y:max_y + 1]

            #use the mask to add valid pixels to a list
            pixels = np.array([box[x,y] for x,y in zip(*np.where(grid))])
            avg_intensity = np.tile(np.mean(pixels, axis=0), (pixels.shape[0],1))
            error = (np.square(pixels - avg_intensity)).mean(axis=None)
            return error
            
    def save(self, filename):
        



img = imread("image2.png")
t = Triangulation(10, img.shape[0], img.shape[1])
t.calculate_error(img)
