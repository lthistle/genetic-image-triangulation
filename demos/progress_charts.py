from matplotlib.image import imread
import matplotlib.pyplot as plt
import pandas as pd
fig, axes = plt.subplots(1, 3, figsize=(16, 16))

my_ax = axes[0]
img = imread(f"results/images/gen0/best0.png")
my_ax.imshow(img)
my_ax.set_title(f"1st Generation")

my_ax = axes[1]
img = imread(f"results/images/gen50/best0.png")
my_ax.imshow(img)
my_ax.set_title(f"50th Generation")

my_ax = axes[2]
img = imread(f"results/images/gen99/best0.png")
my_ax.imshow(img)
my_ax.set_title(f"99th Generation")

fig.suptitle("Evolution of the triangulations")
plt.show()