from scipy.spatial import Delaunay
from matplotlib.image import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
import mahotas
import os

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
            
    def save(self, img, filename):
        out_img = np.zeros(img.shape)
        for t in self.triangles:
            #get mask
            pixels, positions = self.get_pixels(t, img, True)
            avg_color = np.mean(pixels, axis=0)
            for x,y in positions:
                out_img[x][y] = avg_color
        imsave(filename, out_img)
    


if __name__ == "__main__":
    img = imread("image.png")
    population = [Triangulation(200, img.shape[0], img.shape[1]) for x in range(100)]
    if not os.path.exists("images"):
        os.mkdir("images")
    logfile = open("fitnesslog.csv", "w")
    logfile.write("Generation, #1 Fitness, #10 Fitness, Worst Fitness\n")
    for gen in range(100):
        #Rank the current population
        print(f"Finding best triangulations in generation {gen}")
        population.sort(key = lambda x: x.calculate_error(img))
        #Print best score
        status = f"{gen},{population[0].fitness},{population[9].fitness},{population[-1].fitness}\n"
        logfile.write(status)
        print(status)
        #Save some of the best and worst from that generation
        print(f"Saving triangulations")
        dir_path = f"images/gen{gen}"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        for i in range(10):
            population[i].save(img, dir_path + f"/best{i}.png")
        population[-1].save(img, dir_path + "/worst.png")
        #Mutate the population and continue
        new_population = []
        [new_population.append(population[i]) for i in range(10)] #take 10 best from previous generation
        print(f"Mutating the 10 best triangulations")
        for i in range(10):
            parent = new_population[i]
            [new_population.append(parent.evolve()) for x in range(9)]
        print(f"New population size is {len(new_population)}")
        population = new_population