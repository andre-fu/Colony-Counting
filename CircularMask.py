from skimage import data, feature, exposure, io
from skimage.color import rgb2gray
from skimage.filters import gaussian
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

def createCircularMask(h, w, center=None, radius=None):
    
    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls 
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask


imgO = io.imread('image_one.jpg')
img = gaussian(imgO, 2)
img = rgb2gray(img)

h, w = img.shape[:2]
mask = createCircularMask(h, w)
masked_img = img.copy()
masked_img[~mask] = 0

#fig, ax = plt.subplots(1)
#ax.imshow(masked_img)
#plt.show()


A = feature.blob_dog(masked_img, min_sigma = 0.6, max_sigma = 13, threshold = 0.1, overlap = 0.8)
fig, ax = plt.subplots(1)
ax.set_aspect('equal')

ax.imshow(imgO)

for i in range(len(A)):
    circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='r', fill=False , lw=0.5)
    fig = plt.gcf()
    ax = fig.gca()
    ax.add_artist(circle)

plt.show()
