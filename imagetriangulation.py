from scipy.spatial import Delaunay
from matplotlib.image import imsave
import numpy as np
import mahotas

class Triangulation:
    def retriangulate(self):
        self.triangles = self.points[Delaunay(self.points).simplices]

    def __init__(self, num_points, width, height, source_points = None):
        self.width = width
        self.height = height
        if source_points is not None:
            self.points = np.copy(source_points)
        else:
            x_coords = np.random.randint(width, size=(num_points, 1))
            y_coords = np.random.randint(height, size=(num_points, 1))
            points = np.hstack((x_coords, y_coords))
            self.points = np.append(points, np.array([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]]), axis=0)
        self.retriangulate()
    
    def evolve(self, mutate = True, max_dist = 5):
        t = Triangulation(len(self.points), self.width, self.height, self.points)
        if mutate:
            for i in np.arange(len(t.points) - 4).tolist():
                #for x and y, slightly change coordinate
                for j in range(2):
                    dimension = t.width if j == 0 else t.height
                    change = np.random.rand() * 2 - 1
                    new_location = t.points[i][j] + max_dist * change
                    while(new_location < 0 or new_location >= dimension):
                        change = np.random.rand() * 2 - 1
                        new_location = t.points[i][j] + max_dist * change
                    t.points[i][j] = new_location
        t.retriangulate()
        return t
        
    def get_pixels(self, t, img, locations = False):
        """Return the pixels bounded by the vertices of triangle, t, in an image, img \n 
        If locations is set to True, a list of pixels will also be returned as a tuple"""
        #find bounding box coordinates
        min_x, min_y = np.amin(t, axis=0)
        max_x, max_y = np.amax(t, axis=0)
        x_size = max_x - min_x + 1
        y_size = max_y - min_y + 1  
        #create a mask
        new_tri = [(x - min_x, y - min_y) for (x,y) in t]
        grid = np.zeros((x_size, y_size), dtype=np.int8)
        mahotas.polygon.fill_polygon(new_tri, grid)
        #get bounding box from original image
        box = img[min_x:max_x + 1,min_y:max_y + 1]
        pixels = np.array([box[x,y] for x,y in zip(*np.where(grid))])
        if locations: 
            return (pixels, [(x + min_x,y + min_y) for x,y in zip(*np.where(grid))])
        return pixels

    def calculate_error(self, img):
        total_error = 0
        for t in self.triangles:    
            pixels = self.get_pixels(t, img)
            avg_intensity = np.tile(np.mean(pixels, axis=0), (pixels.shape[0],1))
            error = (np.square(pixels - avg_intensity)).mean(axis=None)
            total_error += error * len(pixels)
        self.fitness = total_error
        return total_error
            
    def save(self, img, filename, return_img = False):
        out_img = np.zeros(img.shape)
        for t in self.triangles:
            #get mask
            pixels, positions = self.get_pixels(t, img, True)
            avg_color = np.mean(pixels, axis=0)
            for x,y in positions:
                out_img[x][y] = avg_color
        if return_img: 
            return out_img
        else:
            imsave(filename, out_img)