# Genetic Image Triangulation

### About
This is a genetic algorithm that tries to optimize the locations of points such that their Delaunay triangulation most closely resembles a source image.

### Installation
All dependencies are managed by Pipenv. With Pipenv installed, navigate to the root directory and run `pipenv install`. Following which, run `pipenv shell` to activate the virtual environment. Note: if the dependencies aren't working, try adding `--ignore-pipfile` to the install command.

### Example
The process of recreating the images looks something like what's below. Starting with a random set of N points, the 4 vertices of the images are added and the Delaunay triangulation is calculated. Following which, we take a source image and calculate the average color for each triangle.
![Example of the process][fig1]

Currently, the only mutation that can occur is for a point to slightly shift by a small amount. By creating a small population and keeping the top 10 triangulations of each generation, then creating the rest of the population by mutating these top triangulations, we can slowly increase the fitness of the population. This serves as the basis of the genetic algorithm. Over 100 generations, the best triangulation from the first, 50th, and last generations are shown.
![Best pictures over 100 generations][fig2]

The following graph shows the fitnesses over these 100 generations.
![Fitness chart][fig3]



[fig1]: ./demos/delaunaydemo.png
[fig2]: ./demos/progress.png
[fig3]: ./demos/fitness.png