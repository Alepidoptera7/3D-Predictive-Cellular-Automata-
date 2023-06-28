# -*- coding: utf-8 -*-
"""Probabilistic 3-D Conway's Game of Life

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p9Yv_Jgi2LWoXMyuFKcCnKxd-n2J4plI

The purpose of this code is to develop a three dimensional representation of Conway's Game of Life. 

As the standard rules are meant for a 2-D environment and do not generalize to 3 dimensions readily, I've chosen to implement a probablistic model. 

This choice of implementation will cause the results to be non-deterministic. 

Original Rules: 

1) Any live cell with two or three live neighbours survives.

2) Any dead cell with three live neighbours becomes a live cell.

3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.

My rules are the following: 

1) Two contiguous cells will generate a third cell in a randomly chosed direction contiguous to either of the original cells.

2) If two live cells attempt to occupy the same space, one will die. 

3) If an empty cell has every diagonal cell occupied, it will become occupied. 

4) If an occupied cell has every contiguous neighbor cell occupied, it will die.
"""

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np 
from numpy import random 
from matplotlib import animation

class Life:

    def __init__(self):
        self.bernoulli_calc = 0
        self.cell_cull = 0

    def initial_cells(self):
        """
        This function will only develop the initial data used to generate the initial state.

        Input: None
        Output: Initial cell state
        
        """
        initial_live_cells = np.random.choice([0,1], size=(25, 25, 25), p=[0.99, 0.01])
        return initial_live_cells


    def propagation_parameter_check_and_update(self, data):
        
        """
        This function is designed to                     
        Detect neighboring indicies in a cell oriented positionally related matrix 
                         
        case for corners, 3 neighboring cells and end of array 
        case for edges, 4 neighboring cells and end of array 
        case for boundary planes, 5 neighboring cells and end of array 
                            
        For all if statements, 
        cell position in matrix by indcies,
        then assess if a cell is alive, 
        then assess the number of neighbors 
        to determine if a live cell will be generated
        in an unoccupied cell or die if it was smothered
        as result of the previous state.                   

        This is the function which implements the rules of my game of life. 

        Every time this function is called, the cells will be propagated towards 
        a depiction of the next state. 

        As such, this function does the following: 

        *check the positions of the initial set of cubes
        *cubes which are isolated of smothered will die
        *cubes meeting reproduction conditions will cause another cube to be generated 

        Input:The current state data, a 3-d matrix of numpy vectors 
        Output: The augmented state data
    
        """
 
        x_lim,y_lim,z_lim = data.shape
        
        #preprocess edge cases            
        #preclude edge and corner cases

        #front_corners_cell_status = data[0][::data.shape[0]-1, ::data.shape[1]-1]
        #back_corners_cell_status = data[x_lim-1][::data.shape[0]-1, ::data.shape[1]-1]
        
        #matrix_corner_indicies = [data[0][0][0], data[0][0][z_lim-1], data[0][y_lim-1][z_lim-1], data[x_lim-1][0][0],
        #                          data[x_lim-1][y_lim-1][0], data[x_lim-1][0][z_lim-1], data[0][y_lim-1][0], data[x_lim-1][y_lim-1][z_lim-1]]

        #for corner in matrix_corner_indicies:
        #    corner = 0

        #gather the cells which compose each matrix boundary face 

        matrix_face_back= [(0,j,k) for j in range(0, y_lim) for k in range(0, z_lim)]
        matrix_face_left = [(i,0,k) for i in range(0, x_lim) for k in range(0, z_lim)]
        matrix_face_right = [(i,j,0) for i in range(0, x_lim) for j in range(0, y_lim)]

        matrix_face_front = [(x_lim-1,j,k) for j in range(0, y_lim) for k in range(0, z_lim)]
        matrix_face_top = [(i,j,z_lim-1) for i in range(0, x_lim) for j in range(0, y_lim)]
        matrix_face_bottom = [(i,y_lim-1,k) for i in range(0, x_lim) for k in range(0, z_lim)]

        for a,b,c in zip(matrix_face_back, matrix_face_left, matrix_face_right):
            cell_a_x = a[0]
            cell_a_y = a[1]
            cell_a_z = a[2]
            data[cell_a_x][cell_a_y][cell_a_z] = 0
            cell_b_x = b[0]
            cell_b_y = b[1]
            cell_b_z = b[2]
            data[cell_b_x][cell_b_y][cell_b_z] = 0
            cell_c_x = c[0]
            cell_c_y = c[1]
            cell_c_z = c[2]
            data[cell_c_x][cell_c_y][cell_c_z] = 0

        for a,b,c in zip(matrix_face_front, matrix_face_bottom, matrix_face_top):
            cell_a_x = a[0]
            cell_a_y = a[1]
            cell_a_z = a[2]
            data[cell_a_x][cell_a_y][cell_a_z] = 0
            cell_b_x = b[0]
            cell_b_y = b[1]
            cell_b_z = b[2]
            data[cell_b_x][cell_b_y][cell_b_z] = 0
            cell_c_x = c[0]
            cell_c_y = c[1]
            cell_c_z = c[2]
            data[cell_c_x][cell_c_y][cell_c_z] = 0
                 
        #base case -- cells away from edges and corners of data matrix
        for i in range(1, x_lim-1):
            for j in range(1, y_lim-1):
                for k in range(1,z_lim-1):

                    #is the current cell living or dead?
                    cell_status = data[i][j][k]
                    if cell_status == 1:
                            
                        front_neighbor_status_data_tup = ((i,j, k+1), data[i][j][k+1])
                        back_neighbor_status_data_tup = ((i,j,k-1), data[i][j][k-1])
                        left_neighbor_status_data_tup = ((i,j+1,k), data[i][j+1][k])
                        right_neighbor_status_data_tup = ((i,j-1,k),data[i][j-1][k])
                        top_neighbor_status_data_tup = ((i+1,j,k),data[i+1][j][k])
                        bottom_neighbor_status_data_tup = ((i-1,j,k),data[i-1][j][k])

                        diag1 = ((i+1,j+1,k+1), data[i+1][j+1][k+1])
                        diag2 = ((i+1,j+1,k), data[i+1][j+1][k])
                        diag3 = ((i+1,j,k+1), data[i+1][j][k+1])
                        diag4 = ((i,j+1,k+1), data[i][j+1][k+1])
                        diag5 = ((i-1,j-1,k-1), data[i-1][j-1][k])
                        diag6 = ((i-1,j-1,k), data[i-1][j][k-1])
                        diag7 = ((i-1,j,k-1), data[i][j-1][k-1])
                        diag8 = ((i,j-1,k-1), data[i-1][j-1][k-1])
                    
                        neighbor_list = [diag1, diag2, diag3, diag4, diag5, diag6, diag7, diag8, 
                                         front_neighbor_status_data_tup,back_neighbor_status_data_tup,
                                         left_neighbor_status_data_tup, right_neighbor_status_data_tup,
                                         top_neighbor_status_data_tup, bottom_neighbor_status_data_tup]

                        #assess which neighbors are living or not, record results in lists                          
                        live_neighbor_coords_tup_list = [neighbor for neighbor in neighbor_list if neighbor[1] == 1]
                        dead_neighbor_coords_tup_list = [neighbor for neighbor in neighbor_list if neighbor[1] == 0]

                        if not live_neighbor_coords_tup_list:
                            #isolation death 
                            data[i][j][k] = 0   
                            self.cell_cull += 1

                        if not dead_neighbor_coords_tup_list:
                            #overcrowding death
                            data[i][j][k] = 0 
                            self.cell_cull += 1
                            
                        if live_neighbor_coords_tup_list and dead_neighbor_coords_tup_list:
                            #generation at random unoccupied neighbor cell

                            empty_coord_list = [x[0] for x in dead_neighbor_coords_tup_list]

                            index = random.randint(0,len(empty_coord_list))

                            birth_cell_location = empty_coord_list[index]
                            
                            birth_x = birth_cell_location[0]
                            birth_y = birth_cell_location[1]
                            birth_z = birth_cell_location[2]

                            data[birth_x][birth_y][birth_z] = 1
                            self.bernoulli_calc += 1
                                    
        return data


    def print_Bernoulli(self):
         print("Surviving cells: ", self.bernoulli_calc)
         print("Total Cell cull: ", self.cell_cull)
         print("Percent of indicies occupied: ", self.bernoulli_calc / 15625)


    def matrix_generator(self, data):
        """The purpose of this function is to develop a 3 dimensional graph
         from the given coordinate data.
         
         Input: Coordinate data
         Output: 3-d graph 
         
         """

        #plotting voxels
        fig = plt.figure()
        axis = fig.gca(projection="3d")

        fig.set_size_inches(10, 8)

        axis.set_xlabel('x')
        axis.set_ylabel('y')
        axis.set_zlabel('z')
 
        axis.voxels(data, facecolors='red', edgecolors='pink')
        
        plt.show()


def main():

    number_of_iterations = 9

    linker = Life()
    initial_data = linker.initial_cells()
    linker.matrix_generator(initial_data)
    updated_data = linker.propagation_parameter_check_and_update(initial_data)

    for step in range(number_of_iterations):   
        updated_data = linker.propagation_parameter_check_and_update(updated_data)
        linker.matrix_generator(updated_data)
        linker.print_Bernoulli()       

if __name__ == '__main__':
    main()

