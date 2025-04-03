# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 12:48:04 2023

@author: hbs
"""

#   A program to solve Sudoku puzzles in the way that humans do
#%%
import sys
import os
file_path = os.path.abspath(__file__)
sys.path.append(file_path[:-9])
import matplotlib.pyplot as plt
import numpy as np
import copy
import itertools
from puzzles import *
import rules
# test github in vs code


# Create a 9x9 numpy array to represent the Sudoku


# possible_board is a 9x9x9 numpy array of all possible values for a cell
# if possible value = value that is possible which is the value of the third dim
# if value is not possible value = 0

verbose = True
# Draw the grid
def draw_board(puzzle):
    # Draws sudoku board and fill with numbers and possibilities
    # using matplot, board and possible_board
    fig, ax = plt.subplots()
    ax.set_xlim([0, 9])
    ax.set_ylim([0, 9])
    for x in range(10):
        if x % 3 == 0:
            ax.axhline(x, lw=2, color="k", zorder=5)
            ax.axvline(x, lw=2, color="k", zorder=5)
        else:
            ax.axhline(x, lw=1, color="k", zorder=5)
            ax.axvline(x, lw=1, color="k", zorder=5)

    # Draw the boxes
    for y in range(3):
        for x in range(3):
            ax.add_patch(
                plt.Rectangle(
                    (y * 3, x * 3), 3, 3, fill=None, lw=2, color="k", zorder=4
                )
            )

    # Add the numbers
    for y in range(9):
        for x in range(9):
            if puzzle.values[x, y] != 0:
                ax.text(
                    y + 0.5,
                    x + 0.5,
                    str(puzzle.values[x, y]),
                    fontsize=20,
                    ha="center",
                    va="center",
                )
            else:
                for i, num in enumerate(range(1, 10)):
                    if puzzle.possible_values[x, y, i] != 0:
                        value = puzzle.possible_values[x, y, i]
                        ax.text(
                            y + 0.2 + (i % 3) * 0.3,
                            x + 0.8 - (i // 3) * 0.3,
                            str(value),
                            fontsize=7,
                            ha="center",
                            va="center",
                            alpha=0.4,
                        )

    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()


def input_puzzle():
    # user inputs a puzzle, 0 = blank space
    puzzle = []
    for row in range(9):
        x = [int(x) for x in input("input row " + str(row) + " : ").split()]
        if len(x) != 9:
            return print("wrong number of entries")
        if max(x) > 9 or min(x) < 0:
            return print("entry out of range")
        puzzle.append(x)
        # make numpy array of puzzle
        output = np.array(puzzle)
    return output

def input_sudoku():
    #user inputs one cell at a time
    values = np.zeros([9,9], dtype=int)
    for row in range(9):
        for col in range(9):
            values[row,col] = input("input cell value (0 for unt known)")
            draw_part_of_board(values, row,col)
    draw_board_values_only(values)
    return values

def draw_part_of_board(values, row, col):
    # draws a sudoku board with known values only no possible values
    # Draws sudoku board and fill with numbers and possibilities
    # using matplot, board and possible_board
    fig, ax = plt.subplots()
    ax.set_xlim([0, 9])
    ax.set_ylim([0, 9])
    for x in range(10):
        if x % 3 == 0:
            ax.axhline(x, lw=2, color="k", zorder=5)
            ax.axvline(x, lw=2, color="k", zorder=5)
        else:
            ax.axhline(x, lw=1, color="k", zorder=5)
            ax.axvline(x, lw=1, color="k", zorder=5)

    # Draw the boxes
    for y in range(3):
        for x in range(3):
            ax.add_patch(
                plt.Rectangle(
                    (y * 3, x * 3), 3, 3, fill=None, lw=2, color="k", zorder=4
                )
            )

    # Add the numbers
    for x in range(row+1):
        for y in range(9):
            if x != row:
                ax.text(
                    y + 0.5,
                    x + 0.5,
                    str(values[x, y]),
                    fontsize=20,
                    ha="center",
                    va="center",
                )
                
            elif x == row and y <= col:                 
                ax.text(
                    y + 0.5,
                    x + 0.5,
                    str(values[x, y]),
                    fontsize=20,
                    ha="center",
                    va="center",
                )
                
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()
        
def draw_board_values_only(values):
    # draws a sudoku board with known fvalues only no possible values
    # Draws sudoku board and fill with numbers and possibilities
    # using matplot, board and possible_board
    fig, ax = plt.subplots()
    ax.set_xlim([0, 9])
    ax.set_ylim([0, 9])
    for x in range(10):
        if x % 3 == 0:
            ax.axhline(x, lw=2, color="k", zorder=5)
            ax.axvline(x, lw=2, color="k", zorder=5)
        else:
            ax.axhline(x, lw=1, color="k", zorder=5)
            ax.axvline(x, lw=1, color="k", zorder=5)

    # Draw the boxes
    for y in range(3):
        for x in range(3):
            ax.add_patch(
                plt.Rectangle(
                    (y * 3, x * 3), 3, 3, fill=None, lw=2, color="k", zorder=4
                )
            )

    # Add the numbers
    for y in range(9):
        for x in range(9):
            if values[x, y] != 0:           
                ax.text(
                    y + 0.5,
                    x + 0.5,
                    str(values[x, y]),
                    fontsize=20,
                    ha="center",
                    va="center",
                )
            
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()


class Puzzle:
    # makes puzzle instance
    def __init__(self, puzzle_inputs):
        self.values = copy.deepcopy(puzzle_inputs)
        all_values = np.arange(1, 10)  # puts in values 1 thru 9 in an array
        self.possible_values = np.tile(
            all_values, (9, 9, 1)
        )  # makes a 3D array with values 1 to 9 in third dimension

        self.possible_values = find_init_possible_values(self)
        self.stuck = False
    def __call__(self):
        self.draw()  # draws puzzle with Puzzle()

    def get_row(self, row_num):
        # gets row data
        # returns list of ints
        return self.values[row_num]

    def get_column(self, col_num):
        # gets column number con_num
        # returns list of ints
        return [self.values[x][col_num] for x in range(9)]

    def get_square_values(self, sq_num):
        # gets values in square(unknown values are 0)
        # squares are numbered  0-8 starting left upper = 0 right lower = 8
        # returns a list of ints
        return [
            self.values[row][col]
            for row in range(sq_num // 3 * 3, sq_num // 3 * 3 + 3)
            for col in range(sq_num % 3 * 3, sq_num % 3 * 3 + 3)
        ]

    def get_square_number(self, row, col):
        # finds the number of the square for row and column
        return row // 3 * 3 + col // 3
    
    def get_square_cell_numbers(self,row, col):
        # Determine the square number (0 to 8)
        # and cell number given row and col
        square_number = (row // 3) * 3 + (col // 3)
        # Determine the cell number (0 to 8) within the square
        cell_number = (row % 3) * 3 + (col % 3)
        return square_number, cell_number

    def get_square_coordinates(self, square_number, index_num):
        # gets row and column from square number and index
        # inputs square number int 0-8 and index int 0-8
        # returns list [row,column]
        row = square_number // 3 * 3 + index_num // 3
        column = square_number % 3 * 3 + index_num % 3
        return [row, column]

    def same_square(self, row1, col1, row2, col2):
        # sees if two coordinates are in the same square
        square1 = self.get_square_number(row1, col1)
        square2 = self.get_square_number(row2, col2)
        return square1 == square2

    def possible_values_square(self, sq_num):
        # gets square possible values data
        # squares are numbered  0-8 starting left upper = 0 right lower = 8
        # returns a list of lists of ints
        
        return np.array([self.possible_values[row][col]
                    for row in range(sq_num // 3 * 3, sq_num // 3 * 3 + 3)
                        for col in range(sq_num % 3 * 3, sq_num % 3 * 3 + 3)])
        
    def get_possible_values(self):
        # returns all possible_values
        return(self.possible_values)

    def get_poss_values_cell(self,row,col,number= None):
        '''
        gets possible_values
        if no number iw given returns all possible_values for cell
        if number is given returns the possible_values for that number in the cell
        '''
        if number == None:
            return self.possible_values[row,col]
        else:
            return self.possible_values[row,col,number-1]
    
    def set_possible_values(self,row,col,poss_value, value):
        self.possible_values[row,col,poss_value] = value

    def __get__(self, row, col):
        return self.values[row][col]

    def __set__(self, row, col, num):
        self.values[row][col] = num
        return self.values[row][col]
    
    def get_values(self):
        '''
        Get all values
        '''
        return (self.values)
        

    # Draw the grid
    def draw(self):
        # Draws sudoku board and fill with numbers and possibilities
        # using matplot, board and possible_board
        fig, ax = plt.subplots()
        ax.set_xlim([0, 9])
        ax.set_ylim([0, 9])
        for x in range(10):
            if x % 3 == 0:
                ax.axhline(x, lw=2, color="k", zorder=5)
                ax.axvline(x, lw=2, color="k", zorder=5)
            else:
                ax.axhline(x, lw=1, color="k", zorder=5)
                ax.axvline(x, lw=1, color="k", zorder=5)
        # Draw the boxes
        for y in range(3):
            for x in range(3):
                ax.add_patch(
                    plt.Rectangle(
                        (y * 3, x * 3), 3, 3, fill=None, lw=2, color="k", zorder=4
                    )
                )

            # Add the numbers
            for y in range(9):
                for x in range(9):
                    if self.values[x, y] != 0:
                        ax.text(
                            y + 0.5,
                            x + 0.5,
                            str(self.values[x, y]),
                            fontsize=20,
                            ha="center",
                            va="center",
                        )
                    else:
                        for i, num in enumerate(range(1, 10)):
                            if self.possible_values[x, y, i] != 0:
                                value = self.possible_values[x, y, i]
                                ax.text(
                                    y + 0.2 + (i % 3) * 0.3,
                                    x + 0.8 - (i // 3) * 0.3,
                                    str(value),
                                    fontsize=7,
                                    ha="center",
                                    va="center",
                                    alpha=0.4,
                                )

            ax.invert_yaxis()
            ax.set_aspect("equal")
            ax.axis("off")
            plt.show()


def find_init_possible_values(puzzle):
    # find poss values looking in row, column and block only.
    # deletes not possible values from array possible_values

    for row_num in range(9):
        # row = puzzle.get_row(row_num)
        # row_output = []  # init for poss values for each value in row
        for col_num in range(9):
            value = puzzle.__get__(row_num, col_num)
            # col = puzzle.get_column(col_num)  # col is the values in the col_num
            # square = puzzle.get_square(puzzle.get_square_number(row_num, col_num))
            if value > 0:
                puzzle.possible_values[row_num, col_num] = 0
            else:
                # checking column
                for d3 in range(9):  # d3 goes down the third dim of possible_values
                    p_value = puzzle.__get__(row_num, d3)
                    if p_value > 0:
                        puzzle.possible_values[row_num, col_num, p_value - 1] = 0
                        # print(row_num,col_num,p_value)
                # checking row
                for d3 in range(9):  # d3 goes down the third dim of possible_values
                    p_value = puzzle.__get__(d3, col_num)
                    if p_value > 0:
                        puzzle.possible_values[row_num, col_num, p_value - 1] = 0
                    # print('row =',row_num,'col_num =',col_num,p_value)
                # checking square
                sq_num = puzzle.get_square_number(row_num, col_num)
                sq_values = puzzle.get_square_values(sq_num)
                for index, sq_value in enumerate(sq_values):
                    if sq_value > 0:
                        puzzle.possible_values[row_num, col_num, sq_value - 1] = 0

    return puzzle.possible_values



def solve(sudoku,step = False):
    #function to solve sudoku puzzle
    puzzle = Puzzle(sudoku)
    solved = False
    puzzle.stuck = False
    puzzle.draw()
    rule1 = rules.Rule1()
    rule2 = rules.Rule2()
    rule3 = rules.Rule3()
    rule4 = rules.Rule4()
    rule5 = rules.Rule5()
    rule6 = rules.Rule6()
    rule7 = rules.Rule7()
    rule7b = rules.Rule7b()
    rule7c = rules.Rule7c()
    rule8 = rules.Rule8()
    rule9 = rules.Rule9()
    rule10 = rules.Rule10()
    rule11 = rules.Rule11()

    while not solved and not puzzle.stuck:  
        puzzle.stuck = True
        rule1.check_for_one_number(puzzle) # rule 1
        rule2.check_for_only_poss_cell(puzzle) # rule 2
        rule3.check_for_two_in_same_square(puzzle) # rule 3
        rule4.check_for_two_numbers(puzzle) #rule 4
        rule5.check_two_values_in_two_cells(puzzle) #rule 5
        rule6.check_3_in_cells(puzzle)
        rule7.check_for_three_threes(puzzle)
        rule7b.check_for_three_threes(puzzle)
        rule7c.check_for_three_threes(puzzle)
        rule8.check_for_two_threes(puzzle)
        rule9.check_rule9(puzzle)
        rule10.check_rule10(puzzle)
        rule11.check_rule11(puzzle)
        puzzle.draw()
        solved = check_if_done(puzzle)
        if solved:
            print("Finished")
            check_solution(puzzle)
            return
        if step:
            user_input = input("Enter 1 or 0 or Y or N")
            user_input = user_input.lower()
            if user_input in ["0", "n"]:
                return
            elif user_input in ["1", "y"]:
                pass
            else:
                print("Invalid input.")
                return
        if puzzle.stuck:  
            print('Solver is stuck')

def solve_old(puzzle,step = False):
    #function to solve sudoku puzzle
    solved = False
    puzzle.stuck = False
    puzzle.draw()
    rule1 = rules.Rule1()
    rule2 = rules.Rule2()
    rule3 = rules.Rule3()
    rule4 = rules.Rule4()
    rule5 = rules.Rule5()
    rule6 = rules.Rule6()
    rule7 = rules.Rule7()
    rule7b = rules.Rule7b()
    rule7c = rules.Rule7c()
    rule8 = rules.Rule8()
    rule9 = rules.Rule9()
    rule10 = rules.Rule10()
    rule11 = rules.Rule11()
    while not solved and not puzzle.stuck:  
        puzzle.stuck = True
        rule1.check_for_one_number(puzzle) # rule 1
        rule2.check_for_only_poss_cell(puzzle) # rule 2
        rule3.check_for_two_in_same_square(puzzle) # rule 3
        rule4.check_for_two_numbers(puzzle) #rule 4
        rule5.check_two_values_in_two_cells(puzzle) #rule 5
        rule6.check_3_in_cells(puzzle)
        rule7.check_for_three_threes(puzzle)
        rule7b.check_for_three_threes(puzzle)
        rule7c.check_for_three_threes(puzzle)
        rule8.check_for_two_threes(puzzle)
        rule9.check_rule9(puzzle)
        rule10.check_rule10(puzzle)
        rule11.check_rule11(puzzle)
        puzzle.draw()
        solved = check_if_done(puzzle)
        if solved:
            print("Finished")
            check_solution(puzzle)
            return
        if step:
            user_input = input("Enter 1 or 0 or Y or N")
            user_input = user_input.lower()
            if user_input in ["0", "n"]:
                return
            elif user_input in ["1", "y"]:
                pass
            else:
                print("Invalid input.")
                return
        if puzzle.stuck:  
            print('Solver is stuck')

def solve_one(sudoku,step = False):
    #function to solve sudoku puzzle
    puzzle = Puzzle(sudoku)
    solved = False
    puzzle.stuck = False
    puzzle.draw()
    rule1 = rules.Rule1()
    rule2 = rules.Rule2()
    rule3 = rules.Rule3()
    rule4 = rules.Rule4()
    rule5 = rules.Rule5()
    rule6 = rules.Rule6()
    rule7 = rules.Rule7()
    rule7b = rules.Rule7b()
    rule7c = rules.Rule7c()
    rule8 = rules.Rule8()
    rule9 = rules.Rule9()
    rule10 = rules.Rule10()
    rule11 = rules.Rule11()

    while not solved and not puzzle.stuck:  
        puzzle.stuck = True
        if puzzle.stuck:
            rule1.check_for_one_number(puzzle) # rule 1
        if puzzle.stuck:
            rule2.check_for_only_poss_cell(puzzle) # rule 2
        if puzzle.stuck:
            rule3.check_for_two_in_same_square(puzzle) # rule 3
        if puzzle.stuck:
            rule4.check_for_two_numbers(puzzle) #rule 4
        if puzzle.stuck:
            rule5.check_two_values_in_two_cells(puzzle) #rule 5
        if puzzle.stuck:
            rule6.check_3_in_cells(puzzle)
        if puzzle.stuck:
            rule7.check_for_three_threes(puzzle)
        if puzzle.stuck:
            rule7b.check_for_three_threes(puzzle)
        if puzzle.stuck:
            rule7c.check_for_three_threes(puzzle)
        if puzzle.stuck:
            rule8.check_for_two_threes(puzzle)
        if puzzle.stuck:
            rule9.check_rule9(puzzle)
        if puzzle.stuck:
            rule10.check_rule10(puzzle)
        if puzzle.stuck:
            rule11.check_rule11(puzzle)
        puzzle.draw()
        solved = check_if_done(puzzle)
        if solved:
            print("Finished")
            check_solution(puzzle)
            return
        if step:
            user_input = input("Enter 1 or 0 or Y or N")
            user_input = user_input.lower()
            if user_input in ["0", "n"]:
                return
            elif user_input in ["1", "y"]:
                pass
            else:
                print("Invalid input.")
                return
        if puzzle.stuck:  
            print('Solver is stuck')

def check_if_done(puzzle):
    #See if puzzle is completed
    #returns True if done and False if not done
    if 0 not in puzzle.values:
        return True
    return False

def check_solution(puzzle):
    """ 
    Checks if the puzzle's solution is correct
    returns True or False value of the correctness
    """
    #rows
    for row_num in range (9):
        row = puzzle.get_row(row_num)
        row_set = set(row)
        if len(row_set) != 9 or 0 in row_set:
            print('solution not valid')
            return False
    #columns
    for col_num in range (9):
        col = puzzle.get_column(col_num)
        col_set = set(col)
        if len(col_set) != 9 or 0 in col_set:
            print('solution not valid')
            return False
    #squares
    for squ_num in range (9):
        squ_values = puzzle.get_square_values(squ_num)
        squ_set = set(squ_values)
        if len(squ_set) != 9 or 0 in squ_set:
            print('solution not valid')
            return False
    if np.max(puzzle.get_values()) >9 or np.min(puzzle.get_values()) < 1:
        print('solution not valid') 
        return False
    print('Solution is valid')
    return True

   


#%%
