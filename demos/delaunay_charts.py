from context import imagetriangulation as imgtri
from matplotlib.image import imread
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(6, 16))

#create sample image triangulation
img = imread("image.png")
t = imgtri.Triangulation(50, img.shape[0], img.shape[1])
points = t.points

#create first subplot
axes[0, 0].scatter(points[:,1], points[:,0], color='red')
axes[0, 0].set_title("A random set of 50 points")
axes[0, 0].set_ylim(img.shape[0], 0)
axes[0, 0].set_xlim(0, img.shape[1])

#create second subplot
axes[0, 1].set_title("Their Delaunay triangulation")
tri = Delaunay(points)
axes[0, 1].triplot(points[:,1], points[:,0], tri.simplices.copy(), color = 'blue')
axes[0, 1].plot(points[:,1], points[:,0], 'o', color='red')
axes[0, 1].set_ylim(img.shape[0], 0)
axes[0, 1].set_xlim(0, img.shape[1])

#create third subplot
axes[1, 0].imshow(img)
axes[1, 0].set_title("A sample image")

#create fourth subplot
tri_img = t.save(img, "", return_img = True)
axes[1, 1].imshow(tri_img)
axes[1, 1].set_title("The resulting triangulation")

#display plot
plt.show()