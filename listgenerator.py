import cv2
import numpy as np
from random import seed
from random import randint

class ListGenerator:
    def __init__(self, seed, frame):
        self.frame = frame
        self.seed = seed
        self.width = frame.shape[1]
        self.height = frame.shape[0]

    def generate(self):
        pcount = self.width
        plist = np.zeros(shape=(3, pcount, 4))
        seed(self.seed)
        for i in range(0, 3):
            for j in range(0, pcount):
                for k in range(0, 4):
                    if (k < 2):
                        plist[i][j][k] = randint(0, self.width - 1)
                    else:
                        plist[i][j][k] = randint(0, self.height - 1)
        print(plist)

        return plist
    
frame = cv2.imread("image.jpg")

with open('seed.txt') as f:
    myseed = f.readline()
myseed = int(myseed, base=16)
    
listgen = ListGenerator(myseed, frame)
listgen.generate()
