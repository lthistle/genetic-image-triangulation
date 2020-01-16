from imagetriangulation import Triangulation as imgtri
from scipy.spatial import Delaunay
from matplotlib.image import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
import mahotas
import os

#constants
NUM_GEN = 100
POP_SIZE = 100
NUM_POINTS = 200

#make needed directories and files
if not os.path.exists("results"):
    os.mkdir("results")
if not os.path.exists("results/images"):
    os.mkdir("results/images")
logfile = open("results/log.csv", "w")
logfile.write("generation,best_fitness,10_fitness,worst_fitness\n")

#Create the population
img = imread("image.png")
population = [imgtri(NUM_POINTS, img.shape[0], img.shape[1]) for x in range(POP_SIZE)]

for gen in range(NUM_GEN):
    #Rank the current population
    print(f"Finding best triangulations in generation {gen}")
    population.sort(key = lambda x: x.calculate_error(img))

    #Print best score
    status = f"{gen},{population[0].fitness},{population[9].fitness},{population[-1].fitness}\n"
    logfile.write(status)
    print(status)

    #Save some of the best and worst from that generation
    print(f"Saving triangulations")
    dir_path = f"results/images/gen{gen}"
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