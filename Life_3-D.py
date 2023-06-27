import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import random

class Life:

    def __init__(self):


        #the environment which contains all points is a dynamic 3-D matrix
        environment = 1


    def matrix_generator(self):
        axis = plt.axes(projection="3d")
        axis.scatter(1,1,1)
        plt.plot()
        plt.show()

def main():

    linker = Life()
    linker.matrix_generator()

if __name__ == '__main__':
    main()
