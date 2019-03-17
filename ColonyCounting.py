class ColonyCounting:

#this class requires many different types of packages to be installed
#i personally reccomend you install them globally; if not you can uncomment out the code below & place it outside the class before it is called! 

#from skimage import data, feature, exposure, io
#from skimage.color import rgb2gray
#from skimage.filters import gaussian
#import matplotlib
#import matplotlib.pyplot as plt
#from matplotlib.patches import Circle
#import numpy as npS

    def __init__(self, imgO):
        self.imgO = imgO
        #self.imgO = io.imread('IMG.jpg/png whatever') #this is so you can import the imgO via its name

    def choose(self, choice): #choice is an int from 0, 1, 2, 3 corresponding to full img, R, G, B channels
        if (choice = 0):
            self.img = self.img0
        if (choice = 1): #red chosen
            self.imgG = self.imgO.copy()
            self.imgG[:, :, 0] = 0 #setting  red channel to 0 (black)
            self.imgG[:, :, 2] = 0 #blue to 0
            
            self.img = self.imgR
            del self.imgR
        if (choice = 2): #green chosen
            self.imgR = self.imgO.copy()
            self.imgR[:, :, 1] = 0
            self.imgR[:, :, 2] = 0

            self.img = self.imgG
            del self.imgG
        if (choice = 3): #blue chosen
            self.imgB = self.imgO.copy()
            self.imgB[:, :, 0] = 0
            self.imgB[:, :, 1] = 0
            
            self.img = self.imgB
            del self.imgB
        else:
            print ("Something needs to be chosen! Give an int: 0 = full img, 1 = Red, 2 = Green, 3 = Blue ")

    def preprocess(self):
        self.img = gaussian(self.img, 2)
        self.img = rgb2gray(self.img)

    def process(self):
        h, w = self.img.shape[:2]
        #radius = ##some number set for PLUM##
        self.mask = createCircularMask(h, w) #radius must be adjusted for the size of PLUM plate - can be done by entering the radius manually
        self.masked_img = self.img.copy()
        self.masked_img[~self.mask] = 0

        self.A = feature.blob_dog(self.masked_img, min_sigma = 0.6, max_sigma = 18, threshold = 0.1, overlap = 0.8) #very computaionally heavy depending be careful here
        self.size = len(self.A) #total number of colonies detected; we can do location and colony picking & area later or if needed at all
        #I can also give the size of the colony, or other averages std dev etc if thats needed?
    
    def createCircularMask(self, h, w, center=None, radius=None):
        if center is None: # use the middle of the image
            center = [int(self.w/2), int(self.h/2)]
        if radius is None: # use the smallest distance between the center and image walls 
            radius = min(center[0], center[1], self.w-center[0], self.h-center[1])

        Y, X = np.ogrid[:self.h, :self.w]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

        mask = dist_from_center <= radius
        return mask

    def image(self): #showing the image 
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')

        ax.imshow(self.imgO)

        for i in range(len(self.A)):
            circle = plt.Circle((self.A[i,1], self.A[i,0]), 2*self.A[i,2], color='r', fill=False , lw=0.5)
            fig = plt.gcf()
            ax = fig.gca()
            ax.add_artist(circle)

        plt.show()
    