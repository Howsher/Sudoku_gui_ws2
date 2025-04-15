#%%

import numpy as np
import itertools

verbose = True

class Rules():
    #class for rules
    def __init__(self):
        pass


class Rule1(Rules):
    '''
        checks to see if only one number is possible in a cell
        finds the first instance only
    '''
    def __init__(self):
        pass

    def check_for_one_number(self,puzzle):
       
        for row in range (9):
            for col in range(9):
                # check for only one value
                if np.count_nonzero(puzzle.possible_values[row,col]) == 1:
                    value = np.sum(puzzle.possible_values[row,col]) #value of the one check_for_one_number
                    if verbose: print('Rule 1 at ', row,col, 'number =', value)
                    self.update_for_new_value (puzzle,value,row,col)
                    return True
        return False


    def update_for_new_value(self,puzzle,value,row,col ):
        '''updates the values and possible_values for puzzle given new value = value'''
        puzzle.stuck = False
        puzzle.values[row,col] = value  #enter new value in values
        puzzle.possible_values[row,col] = 0 #make all the possible_values = 0 for cell[row,col]
        #update column
        for r in range (9): 
            puzzle.possible_values[r,col, value-1] = 0
        #update row
        for c in range(9):
            puzzle.possible_values[row,c, value -1] = 0
        #update square
        sq_num = puzzle.get_square_number(row,col)
        for index in range (9):
            r,c = puzzle.get_square_coordinates(sq_num,index)
            puzzle.possible_values[r,c,value-1] = 0
    
class Rule2(Rules):
    '''
        checks to see if a number occurs in only one cell
        check in row/column/square
    '''
    def __init__(self):
        pass

    def check_for_only_poss_cell(self,puzzle):
        #check row
        for row in range(9):
            for value in range(1,10):
                if np.sum(puzzle.possible_values[row,:,value-1]) == value:  #for all poss_values check if there are more than on in row
                    for col in range(9):   
                        if puzzle.possible_values[row,col,value-1] == value:
                            if verbose: print('Rule 2 row at ', row,col, 'number =', value)
                            self.update_for_new_value(puzzle,value,row,col)
                            return True
        #check in column              
        for col in range(9):
            for value in range(1,10):
                if np.sum(puzzle.possible_values[:,col,value-1]) == value:  #for all poss_values check if there are more than on in row
                    for row in range(9):   
                        if puzzle.possible_values[row,col,value-1] == value:
                            if verbose: print('Rule 2 column at ', row,col, 'number =', value)
                            self.update_for_new_value(puzzle,value,row,col)
                            return True
        #check in square
        for sq in range (0,9):
            sq_poss_values = puzzle.possible_values_square(sq)
            for value in range(1,10):
                if np.sum(sq_poss_values[:,value-1]) == value:  #for all poss_values check if there are more than on in square
                    row, col = [puzzle.get_square_coordinates(sq, r) for r in range(9) if value in sq_poss_values[r,:]][0]
                    if verbose: print('Rule 2 in square', sq,' at position', row,col, 'number =', value)
                    self.update_for_new_value(puzzle,value,row,col)
                    return True
        return False
        
    def update_for_new_value(self,puzzle,value,row,col ):
        #updates the values and possible_values for puzzle given new value = value
        puzzle.stuck = False
        puzzle.values[row,col] = value  #enter new value in values
        puzzle.possible_values[row,col] = 0 #make all the possible_values = 0 for cell[row,col]
        #update column
        for r in range (9): 
            puzzle.possible_values[r,col, value-1] = 0
        #update row
        for c in range(9):
            puzzle.possible_values[row,c, value -1] = 0
        #update square
        sq_num = puzzle.get_square_number(row,col)
        for index in range (9):
            r,c = puzzle.get_square_coordinates(sq_num,index)
            puzzle.possible_values[r,c,value-1] = 0


class Rule3(Rules):
    '''
        looks for only 2 of same number in a row or col in the same square
        then remove the number from elsewhere in the square
    '''
    def __init__(self):
        pass

    def check_for_two_in_same_square(self,puzzle):
        

        #check rows
        for row in range(9):
            #num_times is vector with number of times each digit occurs in row
            num_times = np.count_nonzero(puzzle.possible_values[row], axis = 0)
            two_times = np.where(num_times == 2)[0]
            for num in two_times:
                col_pos = np.nonzero(puzzle.possible_values[row,:,num])[0]
                # col_pos is the 2 columns with the same number in array[2,]
                #print('Two numbers number =',num+1, 'row =', row, 'columns = ', col_pos)
                if puzzle.same_square(row,col_pos[0],row,col_pos[1]):
                    self.update_two_in_same_square(puzzle,num+1,row,col_pos[0],row,col_pos[1])
                    if puzzle.stuck == False:
                        return True
        
        
        #check columns    
        for col in range(9):
            #num_times is vector with number of times each digit occurs in row
            num_times = np.count_nonzero(puzzle.possible_values[:,col], axis = 0)
            two_times = np.where(num_times == 2)[0]
            for num in two_times:
                row_pos = np.nonzero(puzzle.possible_values[:,col,num])[0]
                # col_pos is the 2 columns with the same number in array[2,]
                #print('Two numbers number =',num+1, 'col =', col, 'columns = ', col_pos)
                if puzzle.same_square(row_pos[0],col,row_pos[1],col):
                    self.update_two_in_same_square(puzzle,num+1,row_pos[0],col,row_pos[1],col)
                    #if verbose: print('found one with rule 3 col at ', row_pos,col, 'numbers =',num+1 )
                    if puzzle.stuck == False:
                        return True
        
        #check squares
        for sq_num in range(9):
            twos = self.two_numbers_in_square(puzzle,sq_num)
            #twos are a array of the numbers that there are 2 of in the square
            for num in twos:
                r1,c1,r2,c2 = self.find_positions_of_nums(puzzle,sq_num,num+1) # returns [r1,c1,r2,c2]
                if r1 == r2:
                    self.update_row_for_one_in_sq(puzzle,num+1,r1,c1,c2)
                    if puzzle.stuck == False:
                        return True
                if c1 == c2:
                    self.update_col_for_one_in_sq(puzzle,num+1,r1,r2,c1)
                    if puzzle.stuck == False:
                        return True
        return False

        

    def two_numbers_in_square(self,puzzle,sq_num):
        #checks to see if there are two of the same number in sq_num possible_values
        #returns an array with the poitions where there are 2 nums (the nums are position +1)
        poss_values =  puzzle.possible_values_square(sq_num)
        num_times = np.count_nonzero(poss_values, axis = 0)
        two_times = np.where(num_times == 2)[0]
        return two_times

    def find_positions_of_nums(self,puzzle,sq_num,num):
        poss_values = puzzle.possible_values_square(sq_num)
        r1 = c1 = r2= c2= 10  # 10 is position not set yet
        for cell in range(9):
            if num in poss_values[cell]:
                if r1 == 10:            
                    r1, c1 = puzzle.get_square_coordinates(sq_num,cell)
                else:
                    r2, c2 = puzzle.get_square_coordinates(sq_num,cell)
                    return [r1,c1,r2,c2]
                
    def update_row_for_one_in_sq(self,puzzle,number,row1,col1,col2):
        #row1 should = row2
        for col in range(9):
            if col !=col1 and col !=col2:
                if puzzle.possible_values[row1,col,number-1] != 0:
                    puzzle.stuck = False
                    if verbose: print('Rule 3 row in square at ', row1,col, 'numbers =',number )
                puzzle.possible_values[row1,col,number-1] = 0
                

    def update_col_for_one_in_sq(self,puzzle,number,row1,row2,col1):
        for row in range(9):
            if row !=row1 and row !=row2:
                if puzzle.possible_values[row,col1,number-1] != 0:
                    puzzle.stuck = False
                    if verbose: print('Rule 3 col in square at ', row,col1, 'numbers =',number )
                puzzle.possible_values[row,col1,number-1] = 0
                
            
                
    def update_two_in_same_square(self,puzzle,number,row1,col1,row2,col2):
        # remove number from square except [row1, col1] and [row2,col2]
        square, cell1 = puzzle.get_square_cell_numbers(row1,col1)
        _, cell2 = puzzle.get_square_cell_numbers(row2,col2)
        for cell in range(9):
            row,col = puzzle.get_square_coordinates(square,cell)
            #print('cell=',cell,'row = ',row,'col = ',col)
            #delete values in other cells in row
            if  cell != cell1 and cell != cell2:
                if puzzle.possible_values[row,col,number-1] != 0:
                    puzzle.stuck = False
                    if verbose: print('Rule 3 square at ', row1,col1,'and', row2,col2, 'number =',number )
                puzzle.possible_values[row,col,number-1] = 0
                #print('cell=',cell,'cell1 =',cell1,'cell2 =,cell2,row = ',row,'col = ',col)
 
class Rule4(Rules):
    #looks for two cells with the same two numbers in them and only two #s in them
    #then updates the possible values to remove them from other cells
    
    def __init__(self):
        pass

    def check_for_two_numbers(self,puzzle):
        
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    def check_rows(self,puzzle):
        #check rows
        for row in range (9):
            #array to keep cells with two possible_values or 0 if not two values
            twos = np.zeros([9,2], dtype=int)  
            for col in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                    
                if poss_nums.shape[0] == 2:  #number of poss_nums are 2
                    two_nums = np.nonzero(puzzle.possible_values[row,col])[0] +1
                    twos[col,:] = two_nums  
            #now have to compare rows of twos[col,:] to see if ==
            
            for col in range(9):
                matches =np.where((twos == twos[col]).all(axis=1))[0]
                if matches.shape[0] == 2 and twos[col,0] != 0:  #checks that there is a match and not 0s
                    self.update_twos_row(puzzle,twos[col,0],twos[col,1], row, matches)
                    if puzzle.stuck == False:
                        return True
                            
    def check_columns(self, puzzle):
        #check columns
        for col in range (9):
            #array to keep cells with two possible_values or 0 if not two values
            twos = np.zeros([9,2], dtype=int)  
            for row in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                    
                if poss_nums.shape[0] == 2:  #number of poss_nums are 2
                    two_nums = np.nonzero(puzzle.possible_values[row,col])[0] +1
                    twos[row,:] = two_nums      
            #now have to compare col of twos[:,row] to see if ==
            for row in range(9):
                matches =np.where((twos == twos[row]).all(axis=1))[0]
                if matches.shape[0] == 2 and twos[row,0] != 0:  #checks that there is a match and not 0
                    self.update_twos_column(puzzle,twos[row,0],twos[row,1], col, matches)
                    if puzzle.stuck == False:
                        return True
         
    def check_squares(self,puzzle):           
        #check squares
        for square in range (9):
            #array to keep cells with two possible_values or 0 if not two values
            twos = np.zeros([9,2], dtype=int)
            poss_values = puzzle.possible_values_square(square)
            for cell in range(9):
                #find number of possible_values in cell
                    
                poss_nums = np.nonzero(poss_values[cell])[0]           
                if poss_nums.shape[0] == 2:  #number of poss_nums are 2
                    two_nums = np.nonzero(poss_values[cell])[0] +1
                    twos[cell,:] = two_nums
            #now have to compare col of twos[:,cell] to see if ==
            for cell in range(9):
                matches =np.where((twos == twos[cell]).all(axis=1))[0]
                if matches.shape[0] == 2 and twos[cell,0] != 0:  #checks that there is a match and not 0s
                    self.update_twos_square(puzzle,twos[cell,0],twos[cell,1], square, matches)
                    if puzzle.stuck == False:
                        return True
                    
    def update_twos_row(self,puzzle,num_1,num_2,row,cols_matches):
        #updates possible_values
        #inputs: num_1: int first of two values
        #        num_2 int second of two values
        #        row: int
        #        cols_match: np.array shape [2,] that gives the columns that match
        for col in range(9):
            #delete values in other cells in row
            if col not in cols_matches:
                if puzzle.possible_values[row,col,num_1-1] != 0 or puzzle.possible_values[row,col,num_2-1] != 0:
                    puzzle.stuck = False
                    if verbose: print('Rule 4 row at ', row,col, 'numbers =',num_1,num_2 ) 
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                if puzzle.stuck == False:
                        return True
            
                

    def update_twos_column(self,puzzle,num_1,num_2,col,rows_matches):
        #updates possible_values for both cols and rows in square
        #inputs: num_1: int first of two values
        #        num_2 int second of two values
        #        row: int
        #        row_match: np.array shape [2,] that gives the rows that match
        for row in range(9):
            #delete values in other cells in row
            if row not in rows_matches:
                if puzzle.possible_values[row,col,num_1-1] != 0 or puzzle.possible_values[row,col,num_2-1] != 0:
                    puzzle.stuck = False
                    if verbose: print('Rule 4 column at ', row,col, 'numbers =',num_1,num_2 )
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                if puzzle.stuck == False:
                        return True
    def update_twos_square(self,puzzle,num_1,num_2,square,cell_matches):
        #updates possible_values
        #inputs: num_1: int first of two values
        #        num_2 int second of two values
        #        square: int 0-8
        #        cell: int 0-8
        #        cell_match: np.array shape [2,] that gives the cells that match
        for cell in range(9):
            #delete values in other cells in row
            if  cell not in cell_matches:
                row,col = puzzle.get_square_coordinates(square,cell)
                if puzzle.possible_values[row,col,num_1-1] != 0 or puzzle.possible_values[row,col,num_2-1] != 0:
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 4 square at ', square,cell, 'numbers =',num_1,num_2 )
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                if puzzle.stuck == False:
                        return True

class Rule5(Rules):
    """ 
        makes rule5 instance
        looks for the same two poss_values in two cells and only two cells
        but cells may have other poss_values in cells
    """
    def __init__(self):
        pass

    def check_two_values_in_two_cells(self,puzzle):
        # Rule #5       
        self.check_two_values_in_row(puzzle)
        self.check_two_values_in_col(puzzle)
        self.check_two_values_in_sq(puzzle)

    def check_two_values_in_row(self,puzzle):
        #looks for the same two poss_values in only two cels in same row
        poss_values = puzzle.get_possible_values()
        for row in range(9):
            twos = self.number_two_times(poss_values[row])
            combinations = list(itertools.combinations(twos, 2))
            for pair in combinations:
                if self.pairs_in_same_columns(poss_values[row],pair):
                    columns = np.where(poss_values[row] == pair[0] )[0]
                    col1,col2 = columns
                    
                    self.update_two_in_row(puzzle,pair[0],pair[1],row,col1,col2)

        
    def number_two_times (self,poss_values_row):
        # finds the numbers that occur 2 times in a row/col/square
        # returns numbers not array position
        num_times = self.number_times_occur(poss_values_row)
        return np.where(num_times == 2)[0] +1

    def number_times_occur(self,poss_values_row):
        #number of times a poss_value occurs
        #poss_values is an 2D array of poss_values in row, col or sq
        return np.count_nonzero(poss_values_row, axis = 0)

    def pairs_in_same_columns(self,poss_values_row,pair):
        col1 = np.where(poss_values_row == pair[0] )[0]
        col2 = np.where(poss_values_row == pair[1] )[0]
        return np.all(col1==col2)  #Check that both numbers are in the same columns

    def update_two_in_row(self,puzzle,num1,num2,row,col1,col2):
        
        if np.count_nonzero(puzzle.possible_values[row,col1]) >2 or np.count_nonzero(puzzle.possible_values[row,col2]) >2:
            puzzle.stuck = False
            if verbose: print('Rule 5 at row', row,'cols',col1,col2, 'numbers =',num1,num2 )
        puzzle.possible_values[row,col1] = 0    #remove all numbers in first column
        puzzle.possible_values[row,col1,num1-1] = num1  #add back two matching numbers
        puzzle.possible_values[row,col1,num2-1] = num2
        puzzle.possible_values[row,col2] = 0    #remove all numbers in second column
        puzzle.possible_values[row,col2,num1-1] = num1  #add back two matching numbers
        puzzle.possible_values[row,col2,num2-1] = num2

    def check_two_values_in_col(self,puzzle):
        #looks for the same two poss_values in only two cels in same col
        poss_values = puzzle.get_possible_values()
        for col in range(9):
            poss_values_col = poss_values[:,col]
            twos = self.number_two_times(poss_values_col)
            combinations = list(itertools.combinations(twos, 2))
            for pair in combinations:
                if self.pairs_in_same_columns(poss_values_col,pair):
                    rows = np.where(poss_values_col == pair[0] )[0]
                    row1,row2 = rows
                    self.update_two_in_col(puzzle,pair[0],pair[1],col,row1,row2)

    def update_two_in_col(self,puzzle,num1,num2,col,row1,row2):
        #removes all values except num1 and num2 from two cells    
        if np.count_nonzero(puzzle.possible_values[row1,col]) >2 or np.count_nonzero(puzzle.possible_values[row2,col]) >2:
            puzzle.stuck = False
            if verbose: print('Rule 5 at col', col,'rows',row1,row2, 'numbers =',num1,num2)
        puzzle.possible_values[row1,col] = 0    #remove all numbers in first column
        puzzle.possible_values[row1,col,num1-1] = num1  #add back two matching numbers
        puzzle.possible_values[row1,col,num2-1] = num2
        puzzle.possible_values[row2,col] = 0    #remove all numbers in second column
        puzzle.possible_values[row2,col,num1-1] = num1  #add back two matching numbers
        puzzle.possible_values[row2,col,num2-1] = num2

    def check_two_values_in_sq(self,puzzle):
        #looks for the same two poss_values in only two cells in same square
        for square in range(9):
            poss_values = puzzle.possible_values_square(square)
            twos = self.number_two_times(poss_values)
            combinations = list(itertools.combinations(twos, 2))
            for pair in combinations:
                if self.pairs_in_same_columns(poss_values,pair):               
                    cells = np.where(poss_values== pair[0] )[0]
                    cell1,cell2 = cells
                    row1,col1 = puzzle.get_square_coordinates(square,cell1)
                    row2,col2 = puzzle.get_square_coordinates(square,cell2)
                    self.update_two_in_sq(puzzle,pair[0],pair[1],row1,row2,col1,col2)

    def update_two_in_sq(self,puzzle,num1,num2,row1,row2,col1,col2):
        if np.count_nonzero(puzzle.possible_values[row1,col1]) >2 or np.count_nonzero(puzzle.possible_values[row2,col2]) >2:
            puzzle.stuck = False
            if verbose: print('Rule 5 square at rows',row1,row2,'cols',col1,col2, 'numbers =',num1,num2)
        puzzle.possible_values[row1,col1] = 0    #remove all numbers in first column
        puzzle.possible_values[row1,col1,num1-1] = num1  #add back two matching numbers
        puzzle.possible_values[row1,col1,num2-1] = num2
        puzzle.possible_values[row2,col2] = 0    #remove all numbers in second column
        puzzle.possible_values[row2,col2,num1-1] = num1  #add back two matching numbers
        puzzle.possible_values[row2,col2,num2-1] = num2



class Rule6(Rules):
    """ 
    Looks for same number in 3 and only cells in the same row or column 
    and in same square then can remove number from other cells in square
    """
    def __init__(self):
        pass

    def check_3_in_cells(self,puzzle):
        self.check_3_in_row(puzzle)
        self.check_3_in_column(puzzle)

    def check_3_in_row(self,puzzle):
        for row in range(9):
        #num_times is vector with number of times each digit occurs in row
            num_times = np.count_nonzero(puzzle.possible_values[row], axis = 0)
            three_times = np.where(num_times == 3)[0]
            for num in three_times:
                col_pos = np.nonzero(puzzle.possible_values[row,:,num])[0]
                # col_pos is the 3 columns with the same number in array[3,]
                #if verbose: print('Rule6 number =',num+1, 'row =', row, 'columns = ', col_pos)
                if (puzzle.same_square(row,col_pos[0],row,col_pos[1]) and
                    puzzle.same_square(row,col_pos[1],row,col_pos[2])):
                    
                    self.update_three_in_same_square(puzzle,num+1,row,col_pos[0],row,col_pos[1],row,col_pos[2])
                    
        
    def update_three_in_same_square(self,puzzle,number,row1,col1,row2,col2,row3,col3):
        # remove number from square except [row1, col1] and [row2,col2] and [row3,col3]
        #print('number = ', number, 'row =', row1,'row2 =',row2, 'col1=', col1,'col2 =',col2)
        square, cell1 = puzzle.get_square_cell_numbers(row1,col1)
        _, cell2 = puzzle.get_square_cell_numbers(row2,col2)
        _, cell3 = puzzle.get_square_cell_numbers(row3,col3)
        for cell in range(9):
            row,col = puzzle.get_square_coordinates(square,cell)
            #print('cell=',cell,'row = ',row,'col = ',col)
            #delete values in other cells in row
            if  cell != cell1 and cell != cell2 and cell != cell3:
                if puzzle.possible_values[row,col,number-1] != 0:
                    puzzle.stuck = False
                    puzzle.possible_values[row,col,number-1] = 0
                    #print('cell=',cell,'cell1 =',cell1,'cell2 =',cell2,'row = ',row,'col = ',col)
                    if verbose: 
                        print('Rule 6 row at ', row,col1,col2,col3, 'number =',number )
                        print('     removed number',number, 'at row', row, 'and column', col)
    
    #check columns
    def check_3_in_column(self,puzzle):    
        for col in range(9):
            #num_times is vector with number of times each digit occurs in row
            num_times = np.count_nonzero(puzzle.possible_values[:,col], axis = 0)
            three_times = np.where(num_times == 3)[0]
            for num in three_times:
                row_pos = np.nonzero(puzzle.possible_values[:,col,num])[0]
                # row_pos is the 3 columns with the same number in array[3,]
                
                if (puzzle.same_square(row_pos[0],col,row_pos[1],col) and
                    puzzle.same_square(row_pos[1],col,row_pos[2],col)):
                    self.update_three_in_same_square(puzzle,num+1,row_pos[0],col,row_pos[1],col,row_pos[2],col)
                    #if verbose: print('Rule6 Three numbers number =',num+1, 'col =', col, 'rows = ', row_pos)
class Rule7(Rules):
    """
    Looks for same 3 numbers in three cells only in row/row/square
     but one or two of the cells can only have two of the numbers but not same two numbers
     since that would evoke rule same two numbers in two cells. This is an
     expansion of two nums in two cells to three.
     """
    def __init__(self):
        pass

    def check_for_three_threes(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    def check_rows(self,puzzle):
        '''
        checks for three threes in rows
        '''
        for row in range(9):
            threes = np.zeros([9,3], dtype=int)  
            for col in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                    
                if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                    three_nums = np.nonzero(puzzle.possible_values[row,col])[0] +1
                    threes[col,:] = three_nums
            #now have to compare rows of threes[col,:] to see if ==
            #have to make sure there aren't 3 [0,0,0]
            for col in range(9):
                matches =np.where((threes == threes[col]).all(axis=1))[0]
                if matches.shape[0] == 3 and threes[col,0] != 0:  #checks that there is a match
                    self.update_threes_row(puzzle,threes[col,0],threes[col,1],threes[col,2],row, matches)
                    

    def update_threes_row(self,puzzle,num_1,num_2,num_3,row,cols_matches):
        """
        remove any of the 3 numbers from other cells in the row.
        (if all are in same square the update_threes_square will tkae care of them)
        updates possible_values
        inputs: num_1: int first of three values
                num_2 int second of three values
                num_3 int third of three values
                row: int
                cols_match: np.array shape [3,] that gives the columns that match
        """
        for col in range(9):
            #delete values in other cells in row
            if col not in cols_matches:
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 7 row at ', row, col, 'numbers =',num_1,num_2,num_3 )
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0
        
    def check_columns(self,puzzle):
        '''
        checks for three threes in rows
        '''
        for col in range(9):
            threes = np.zeros([9,3], dtype=int)  
            for row in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                    
                if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                    three_nums = np.nonzero(puzzle.possible_values[row,col])[0] +1
                    threes[row,:] = three_nums
            #now have to compare rows of threes[col,:] to see if ==
            for row in range(9):
                matches =np.where((threes == threes[row]).all(axis=1))[0]
                if matches.shape[0] == 3 and threes[row,0] != 0:  #checks that there is a match
                    self.update_threes_col(puzzle,threes[row,0],threes[row,1],threes[row,2],col, matches)

    def update_threes_col(self,puzzle,num_1,num_2,num_3,col,rows_matches):
        """
        remove any of the 3 numbers from other cells in the col.
        (if all are in same square the update_threes_square will tkae care of them)
{{ ... }}
        updates possible_values
        inputs: num_1: int first of three values
                num_2 int second of three values
                num_3 int third of three values
                col: int
                rows_match: np.array shape [3,] that gives the columns that match
        """
        for row in range(9):
            #delete values in other cells in row
            if row not in rows_matches:
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] !=0):
                    puzzle.stuck = False
                    if verbose: print('rule 7 col at ', row,col, 'numbers =',num_1,num_2,num_3 ) 
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0

    def check_squares(self,puzzle):           
            #check squares
            for square in range (9):
                #array to keep cells with two possible_values or 0 if not two values
                threes = np.zeros([9,3], dtype=int)
                poss_values = puzzle.possible_values_square(square)
                for cell in range(9):
                    #find number of possible_values in cell
                        
                    poss_nums = np.nonzero(poss_values[cell])[0]           
                    if poss_nums.shape[0] == 3:  #number of poss_nums are 2
                        three_nums = np.nonzero(poss_values[cell])[0] +1
                        threes[cell,:] = three_nums
                #now have to compare sq of threes[:,cell] to see if ==
                for cell in range(9):
                    matches =np.where((threes == threes[cell]).all(axis=1))[0]
                    if matches.shape[0] == 3 and threes[cell,0] != 0:  #checks that there is a match
                        self.update_threes_square(puzzle,threes[cell,0],threes[cell,1],threes[cell,2], square, matches)
                        
        
    def update_threes_square(self,puzzle,num_1,num_2, num_3,square,cell_matches):
        #updates possible_values
        #inputs: num_1: int first of three values
        #        num_2 int second of three values
        #        num_3 int third of three values
        #        square: int 0-8
        #        cell: int 0-8
        #        cell_match: np.array shape [3,] that gives the cells that match
        for cell in range(9):
            #delete values in other cells in row
            if  cell not in cell_matches:
                row,col = puzzle.get_square_coordinates(square,cell)
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                            print('Rule 7 square at ', square,cell, 'numbers =',num_1,num_2,num_3)
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0

class Rule7b(Rules):
    '''
    Looks for same 3 numbers in two cells only and two numbers in one cell in row/row/square.
    This is an expansion of two nums in two cells to three but one with two.
    '''
    def __init__(self):
        pass
    
    def check_for_three_threes(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    
    def check_rows(self,puzzle):
        '''
        checks for two threes and one two in rows
        '''
        for row in range(9):
            threes = np.zeros([9,3], dtype=int)
            twos =  np.zeros([9,2], dtype=int)
            for col in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                    

                if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                    three_nums = poss_nums +1
                    threes[col,:] = three_nums
                if poss_nums.shape[0] == 2:   #number of poss2 nums
                    two_nums = poss_nums +1
                    twos[col,:] = two_nums
            #now have to compare rows of threes[col,:] to see if ==
            #have to make sure there aren't 3 [0,0,0]
            for col in range(9):
                threes_matches =np.where((threes == threes[col]).all(axis=1))[0]  #checks that there is 2 matches but not 0s
                if threes_matches.shape[0] == 2 and threes[col,0] != 0:  
                    twos_match = self.check_if_two_match(threes[col], twos)
                    if twos_match: 
                        match332 = np.append(threes_matches,twos_match[0])                 
                        self.update_threes_row(puzzle,threes[col,0],threes[col,1],threes[col,2],row, match332)   #need to check row                 
    
    def check_if_two_match(self,three_nums,twos):
        """sees if both of the two numbers in the two_array
        match the three numbers in three_nums.  If so it returns
        the column that matches
        threes_numbs is a 1D array with 3 numbers to match in it
        twos is an 9X2 array with cells that have two possible values.
        It returns a list of columns that match"""
        matches = []
        for col in range (9):
            if twos[col,0] in three_nums and twos[col,1] in three_nums:
                matches.append(col)
        return matches

    

    def update_threes_row(self,puzzle,num_1,num_2,num_3,row,cols_matches):
            """
            remove any of the 3 numbers from other cells in the row.
            (if all are in same square the update_threes_square will tkae care of them)
            updates possible_values
            inputs: num_1: int first of three values
                    num_2 int second of three values
                    num_3 int third of three values
                    row: int
                    cols_match: np.array shape [3,] that gives the columns that match
            """
            for col in range(9):
                #delete values in other cells in row
                if col not in cols_matches:
                    if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                        puzzle.possible_values[row,col,num_2-1] != 0 or
                        puzzle.possible_values[row,col,num_3-1] != 0):
                        puzzle.stuck = False
                        if verbose: 
                            print('Rule 7b row at ', row,col, 'numbers =',num_1,num_2,num_3)
                            #print('row =',row,'columns =',matches,'threes =', threes,'three_nums =', three_nums) 
                    puzzle.possible_values[row,col,num_1-1] = 0
                    puzzle.possible_values[row,col,num_2-1] = 0
                    puzzle.possible_values[row,col,num_3-1] = 0

    def check_columns(self,puzzle):
        '''
        checks for two threes and one two in rows
        '''
        for col in range(9):
            threes = np.zeros([9,3], dtype=int)
            twos =  np.zeros([9,2], dtype=int)
            for row in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                    

                if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                    three_nums = poss_nums +1
                    threes[row,:] = three_nums
                if poss_nums.shape[0] == 2:   #number of poss2 nums
                    two_nums = poss_nums +1
                    twos[row,:] = two_nums
            #now have to compare rows of threes[col,:] to see if ==
            #have to make sure there aren't 3 [0,0,0]
            for row in range(9):
                matches =np.where((threes == threes[row]).all(axis=1))[0]  #checks that there is 2 matches but not 0s
                if matches.shape[0] == 2 and threes[row,0] != 0:  
                    twos_match = self.check_if_two_match(threes[row], twos)
                    if twos_match: 
                        match332 = np.append(matches,twos_match[0])                 
                        self.update_threes_col(puzzle,threes[row,0],threes[row,1],threes[row,2],col, match332)
                           
    def update_threes_col(self,puzzle,num_1,num_2,num_3,col,rows_matches):
            """
            remove any of the 3 numbers from other cells in the column.
            (if all are in same square the update_threes_square will take care of them)
            updates possible_values
            inputs: num_1: int first of three values
                    num_2 int second of three values
                    num_3 int third of three values
                    row: int
                    cols_match: np.array shape [3,] that gives the columns that match
            """
            for row in range(9):
                #delete values in other cells in row
                if  row not in rows_matches:
                    if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                        puzzle.possible_values[row,col,num_2-1] != 0 or
                        puzzle.possible_values[row,col,num_3-1] != 0):
                        puzzle.stuck = False
                        if verbose: 
                            print('Rule 7b column at ', row,col, 'numbers =',num_1,num_2,num_3)
                    puzzle.possible_values[row,col,num_1-1] = 0
                    puzzle.possible_values[row,col,num_2-1] = 0
                    puzzle.possible_values[row,col,num_3-1] = 0

    def check_squares(self,puzzle):           
            #check squares
            for square in range (9):
                #array to keep cells with two possible_values or 0 if not two values
                threes = np.zeros([9,3], dtype=int)
                twos =  np.zeros([9,2], dtype=int)
                poss_values = puzzle.possible_values_square(square)
                for cell in range(9):
                    #find number of possible_values in cell                       
                    poss_nums = np.nonzero(poss_values[cell])[0]           
                    if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                        three_nums = np.nonzero(poss_values[cell])[0] +1
                        threes[cell,:] = three_nums
                    if poss_nums.shape[0] == 2:   #number of poss2 nums
                        two_nums = poss_nums +1
                        twos[cell,:] = two_nums
                #now have to compare sq of threes[:,cell] to see if ==
                for cell in range(9):
                    matches =np.where((threes == threes[cell]).all(axis=1))[0]
                    if matches.shape[0] == 2 and threes[cell,0] != 0:  #checks that there is a match
                        twos_match = self.check_if_two_match(threes[cell], twos)
                        if twos_match: 
                            match332 = np.append(matches,twos_match[0])        
                            self.update_square(puzzle,threes[cell,0],threes[cell,1],threes[cell,2], square, match332)
                            
        
    def update_square(self,puzzle,num_1,num_2, num_3,square,cell_matches):
        #updates possible_values
        #inputs: num_1: int first of two values
        #        num_2 int second of two values
        #        num_2 int second of two values
        #        square: int 0-8
        #        cell: int 0-8
        #        cell_match: np.array shape [3,] that gives the cells that match
        for cell in range(9):
            #delete values in other cells in row
            if  cell not in cell_matches:
                row,col = puzzle.get_square_coordinates(square,cell)
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 7b square at ', square,cell, 'numbers =',num_1,num_2,num_3)
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0

class Rule7c(Rules):
    '''
    Looks for same 3 numbers in one cells only and two numbers in two cell in row/row/square.  The 2 two numbers
    can not be the same i.e. 1,2,3/1,2/1,3
    This is an expansion of two nums in two cells to three but one with two.
    '''
    def __init__(self):
        pass
    
    def check_for_three_threes(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    def check_rows(self,puzzle):
        '''
        checks for one three and two twos in rows
        '''
        for row in range(9):
            threes = np.zeros([9,3], dtype=int)
            twos =  np.zeros([9,2], dtype=int)
            for col in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                    three_nums = poss_nums +1
                    threes[col,:] = three_nums
                if poss_nums.shape[0] == 2:   #number of poss2 nums
                    two_nums = poss_nums +1
                    twos[col,:] = two_nums
                
            #now have to compare rows of threes[col,:] to see if ==
            #have to make sure there aren't 3 [0,0,0]
            for col in range(9):
                threes_matches =np.where((threes == threes[col]).all(axis=1))[0]  #checks that there is 1 matches but not 0s
                if threes_matches.shape[0] == 1 and threes[col,0] != 0:
                    twos_match = self.check_if_two_match(threes[col], twos)
                    if twos_match:
                        match322 = [threes_matches[0],twos_match[0],twos_match[1]]
                        #print(threes)          
                        self.update_threes_row(puzzle,threes[col,0],threes[col,1],threes[col,2],row, match322)
                        #print('match322 = ',match322)

    def check_if_two_match(self,three_nums,twos):
        """sees if there are 2 twos both of the two numbers in the two_array
        match the three numbers in three_nums but are not the same with each other.
        If so it returns the column that matches
        threes_numbs is a 1D array with 3 numbers to match in it
        twos is an 9X2 array with cells that have two possible values.
        It returns a list of columns that match"""
        #print('three_nums =',three_nums,'twos =',twos)
        matches = []
        twos_match_1 = -1 #column number of match with 2 numbers
        twos_match_2 = -1
        for col in range (9):
            if twos[col,0] in three_nums and twos[col,1] in three_nums:
                if twos_match_1 < 0:
                    twos_match_1 = col
                    matches.append(col)
                elif twos_match_2 < 0 :
                    twos_match_2 = col
                    matches.append(col)
            #print('twos_match_1=', twos_match_1,'twos_match_2=', twos_match_2,'matches = ',matches)
        #print('matches =', matches)
        if twos_match_1 > -1 and twos_match_2 >-1 and not np.array_equal(twos[twos_match_1],twos[twos_match_2]): 
            # there is 2 twos match and they are not ==
            #print('matches=',matches)
            return matches 
        else:
            return None   
       
    
    def update_threes_row(self,puzzle,num_1,num_2,num_3,row,cols_matches):
            """
            remove any of the 3 numbers from other cells in the row.
            (if all are in same square the update_threes_square will tkae care of them)
            updates possible_values
            inputs: num_1: int first of three values
                    num_2 int second of three values
                    num_3 int third of three values
                    row: int
                    cols_match: np.array shape [3,] that gives the columns that match
            """
            #print(num_1,num_2,num_3,row,cols_matches)
            for col in range(9):
                #delete values in other cells in row
                if col not in cols_matches:
                    if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                        puzzle.possible_values[row,col,num_2-1] != 0 or
                        puzzle.possible_values[row,col,num_3-1] != 0):
                        puzzle.stuck = False
                        if verbose: 
                            print('Rule 7c row at ', row,col, 'numbers =',num_1,num_2,num_3)
                            #print('row =',row,'columns =',matches,'threes =', threes,'three_nums =', three_nums) 
                    puzzle.possible_values[row,col,num_1-1] = 0
                    puzzle.possible_values[row,col,num_2-1] = 0
                    puzzle.possible_values[row,col,num_3-1] = 0

    def check_columns(self,puzzle):
        '''
        checks for one three and two twos in rows
        '''
        for col in range(9):
            threes = np.zeros([9,3], dtype=int)
            twos =  np.zeros([9,2], dtype=int)
            for row in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                    three_nums = poss_nums +1
                    threes[row,:] = three_nums
                if poss_nums.shape[0] == 2:   #number of poss2 nums
                    two_nums = poss_nums +1
                    twos[row,:] = two_nums
                #if col == 0:print(threes, twos)
            #now have to compare rows of threes[col,:] to see if ==
            #have to make sure there aren't 3 [0,0,0]
            for row in range(9):
                threes_matches =np.where((threes == threes[row]).all(axis=1))[0]  #checks that there is 1 matches but not 0s
                if threes_matches.shape[0] == 1 and threes[row,0] != 0:
                    twos_match = self.check_if_two_match(threes[row], twos)
                    if twos_match:
                        match322 = [threes_matches[0],twos_match[0],twos_match[1]]
                        #print(twos)          
                        self.update_threes_col(puzzle,threes[row,0],threes[row,1],threes[row,2],col, match322)
                        #print('match322 = ',match322)
    '''
    def check_if_two_match(self,three_nums,twos):
        """sees if there are 2 twos both of the two numbers in the two_array
        match the three numbers in three_nums but are not the same with each other.
        If so it returns the column that matches
        threes_numbs is a 1D array with 3 numbers to match in it
        twos is an 9X2 array with cells that have two possible values.
        It returns a list of columns that match"""
        #print('three_nums =',three_nums,'twos =',twos)
        matches = []
        twos_match_1 = -1 #column number of match with 2 numbers
        twos_match_2 = -1
        for row in range (9):
            if twos[row,0] in three_nums and twos[row,1] in three_nums:
                if twos_match_1 < 0:
                    twos_match_1 = row
                    matches.append(row)
                elif twos_match_2 < 0 :
                    twos_match_2 = row
                    matches.append(row)
            #print('twos_match_1=', twos_match_1,'twos_match_2=', twos_match_2,'matches = ',matches)
        #print('matches =', matches)
        if twos_match_1 > -1 and twos_match_2 >-1 and not np.array_equal(twos[twos_match_1],twos[twos_match_2]): 
            # there is 2 twos match and they are not ==
            print('matches=',matches)
            return matches 
        else:
            return None   
    ''' 
    
    def update_threes_col(self,puzzle,num_1,num_2,num_3,col,rows_matches):
            """
            remove any of the 3 numbers from other cells in the row.
            (if all are in same square the update_threes_square will tkae care of them)
            updates possible_values
            inputs: num_1: int first of three values
                    num_2 int second of three values
                    num_3 int third of three values
                    row: int
                    cols_match: np.array shape [3,] that gives the columns that match
            """
            #print(num_1,num_2,num_3,col,rows_matches)
            for row in range(9):
                #delete values in other cells in row
                if row not in rows_matches:
                    if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                        puzzle.possible_values[row,col,num_2-1] != 0 or
                        puzzle.possible_values[row,col,num_3-1] != 0):
                        puzzle.stuck = False
                        if verbose: 
                            print('Rule 7c col at ', row,col, 'numbers =',num_1,num_2,num_3)
                            #print('row =',row,'columns =',matches,'threes =', threes,'three_nums =', three_nums) 
                    puzzle.possible_values[row,col,num_1-1] = 0
                    puzzle.possible_values[row,col,num_2-1] = 0
                    puzzle.possible_values[row,col,num_3-1] = 0
    
    
    def check_squares(self,puzzle):           
            #check squares
            for square in range (9):
                #array to keep cells with two possible_values or 0 if not two values
                threes = np.zeros([9,3], dtype=int)
                twos =  np.zeros([9,2], dtype=int)
                poss_values = puzzle.possible_values_square(square)
                for cell in range(9):
                    #find number of possible_values in cell                       
                    poss_nums = np.nonzero(poss_values[cell])[0]           
                    if poss_nums.shape[0] == 3:  #number of poss_nums are 3
                        three_nums = np.nonzero(poss_values[cell])[0] +1
                        threes[cell,:] = three_nums
                    if poss_nums.shape[0] == 2:   #number of poss2 nums
                        two_nums = poss_nums +1
                        twos[cell,:] = two_nums
                #now have to compare sq of threes[:,cell] to see if ==
                for cell in range(9):
                    matches =np.where((threes == threes[cell]).all(axis=1))[0]
                    if matches.shape[0] == 1 and threes[cell,0] != 0:  #checks that there is a match
                        twos_match = self.check_if_two_match(threes[cell], twos)
                        if twos_match: 
                            match322 = [matches[0],twos_match[0],twos_match[1]]      
                            self.update_square(puzzle,threes[cell,0],threes[cell,1],threes[cell,2], square, match322)
                            
        
    def update_square(self,puzzle,num_1,num_2, num_3,square,cell_matches):
        #updates possible_values
        #inputs: num_1: int first of two values
        #        num_2 int second of two values
        #        num_2 int second of two values
        #        square: int 0-8
        #        cell: int 0-8
        #        cell_match: np.array shape [3,] that gives the cells that match
        for cell in range(9):
            #delete values in other cells in row
            if  cell not in cell_matches:
                row,col = puzzle.get_square_coordinates(square,cell)
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 7b square at ', square,cell, 'numbers =',num_1,num_2,num_3)
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0

"""
class Rule8(Rules):
    '''
    Looks for same 3 numbers in three cells but can have other numbers in cells in row/row/square.  
    
    '''
    def __init__(self):
        pass
    
    def check_for_three_threes(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    def check_rows(self,puzzle):
        #looks for the same three poss_values in only three cells in same row
        poss_values = puzzle.get_possible_values()
        for row in range(9):
            threes = self.number_three_times(poss_values[row])
            combinations = list(itertools.combinations(threes, 3))
            for triple in combinations:
                
                if self.triples_in_same_columns(poss_values[row],triple):
                    col1,col2,col3 = np.where(poss_values[row] == triple[0] )[0]                
                    self.update_three_in_row(puzzle,triple,row,col1,col2,col3)

        
    def number_three_times (self,poss_values_row):
        # finds the numbers that occur 3 times in a row/col/square
        # returns numbers not array position
        num_times = self.number_times_occur(poss_values_row)
        return np.where(num_times == 3)[0] +1

    def number_times_occur(self,poss_values_row):
        #number of times a poss_value occurs
        #poss_values is an 2D array of poss_values in row, col or sq
        return np.count_nonzero(poss_values_row, axis = 0)

    def triples_in_same_columns(self,poss_values_row,triple):
        col1 = np.where(poss_values_row == triple[0] )[0]
        col2 = np.where(poss_values_row == triple[1] )[0]
        col3 = np.where(poss_values_row == triple[2] )[0]
        if (len(col1) == 3 and len(col2) == 3 and len(col3) == 3): # check length == 3
            return np.all(col1==col2) and np.all(col2 == col3)  #Check that numbers are in the same columns
        else:
            return False
    def update_three_in_row(self,puzzle,numbers,row,col1,col2,col3):
        num1,num2,num3 = numbers
        if (np.count_nonzero(puzzle.possible_values[row,col1]) >3 or 
            np.count_nonzero(puzzle.possible_values[row,col2]) >3 or
            np.count_nonzero(puzzle.possible_values[row,col3]) >3):
            puzzle.stuck = False
            if verbose: print('Rule 8 at row', row,'cols',col1,col2,col3, 'numbers =',num1,num2,num3 )
            for col in (col1,col2,col3):
                puzzle.possible_values[row,col] = 0    #remove all numbers in first column
                puzzle.possible_values[row,col,num1-1] = num1  #add back three matching numbers
                puzzle.possible_values[row,col,num2-1] = num2
                puzzle.possible_values[row,col,num3-1] = num3 
    
    def check_columns(self,puzzle):
        #looks for the same three poss_values in only three cells in same row
        poss_values = puzzle.get_possible_values()
        for col in range(9):
            threes = self.number_three_times(poss_values[:,col])
            combinations = list(itertools.combinations(threes, 3))
            for triple in combinations:                
                if self.triples_in_same_columns(poss_values[:,col],triple):
                    row1,row2,row3 = np.where(poss_values[:,col] == triple[0] )[0]                
                    self.update_three_in_col(puzzle,triple,col,row1,row2,row3)

        
    def number_three_times (self,poss_values_row):
        # finds the numbers that occur 3 times in a row/col/square
        # returns numbers not array position
        num_times = self.number_times_occur(poss_values_row)
        return np.where(num_times == 3)[0] +1

    def number_times_occur(self,poss_values_row):
        #number of times a poss_value occurs
        #poss_values is an 2D array of poss_values in row, col or sq
        return np.count_nonzero(poss_values_row, axis = 0)

    def triples_in_same_columns(self,poss_values_row,triple):
        col1 = np.where(poss_values_row == triple[0] )[0]
        col2 = np.where(poss_values_row == triple[1] )[0]
        col3 = np.where(poss_values_row == triple[2] )[0]
        if (len(col1) == 3 and len(col2) == 3 and len(col3) == 3): # check length == 3
            return np.all(col1==col2) and np.all(col2 == col3)  #Check that numbers are in the same columns
        else:
            return False
    def update_three_in_col(self,puzzle,numbers,col,row1,row2,row3):
        num1,num2,num3 = numbers
        if (np.count_nonzero(puzzle.possible_values[row1,col]) >3 or 
            np.count_nonzero(puzzle.possible_values[row2,col]) >3 or
            np.count_nonzero(puzzle.possible_values[row3,col]) >3):
            puzzle.stuck = False
            if verbose: print('Rule 8 at column', col,'rows',row1,row2,row3, 'numbers =',num1,num2,num3 )
            for row in (row1,row2,row3):
                puzzle.possible_values[row,col] = 0    #remove all numbers in first column
                puzzle.possible_values[row,col,num1-1] = num1  #add back three matching numbers
                puzzle.possible_values[row,col,num2-1] = num2
                puzzle.possible_values[row,col,num3-1] = num3 

    def check_squares(self,puzzle):
        #looks for the same two poss_values in only two cells in same square
        for square in range(9):
            poss_values = puzzle.possible_values_square(square)
            threes = self.number_three_times(poss_values)
            combinations = list(itertools.combinations(threes, 3))
            for triples in combinations:
                if self.triples_in_same_columns(poss_values,triples):               
                    cell1,cell2,cell3 = np.where(poss_values== triples[0] )[0]
                    row1,col1 = puzzle.get_square_coordinates(square,cell1)
                    row2,col2 = puzzle.get_square_coordinates(square,cell2)
                    row3,col3 = puzzle.get_square_coordinates(square,cell3)
                    numbers = [triples[0],triples[1],triples[2]]
                    self.update_three_in_sq(puzzle,numbers,row1,row2,row3,col1,col2,col3)

    def update_three_in_sq(self,puzzle,numbers,row1,row2,row3,col1,col2,col3):
        num1,num2,num3 = numbers
        if (np.count_nonzero(puzzle.possible_values[row1,col1]) >3 or 
            np.count_nonzero(puzzle.possible_values[row2,col2]) >3 or
            np.count_nonzero(puzzle.possible_values[row3,col3]) >3):
            puzzle.stuck = False
            if verbose: 
                print('Rule 8 square at rows',row1,row2,row3,'cols',col1,col2,col3, 'numbers =',num1,num2,num3)
            for  row, col in zip([row1,row2,row3], [col1,col2,col3]):
                puzzle.possible_values[row,col] = 0    #remove all numbers in column
                puzzle.possible_values[row,col,num1-1] = num1  #add back three matching numbers
                puzzle.possible_values[row,col,num2-1] = num2
                puzzle.possible_values[row,col,num3-1] = num3
"""            

class Rule8(Rules):
    '''
    Looks for same 3 numbers in two cells and two or one of the numbers in one cell
    but can have other numbers in cells in row/row/square.  
    
    '''
    def __init__(self):
        pass

    def check_for_two_threes(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    def check_rows(self,puzzle):
        #looks for the same three poss_values in only three cells in same row
        poss_values = puzzle.get_possible_values()
        for row in range(9):
            for col in range(9):
                poss_values_cell = self.get_poss_values_cell(poss_values,row,col)
                if poss_values_cell.shape[0] > 2:
                    combinations = list(itertools.combinations(poss_values_cell, 3))
                    for triple in combinations:
                        #Need to check that one column has all three numbers in triple
                        poss_values = puzzle.get_possible_values()
                        columns = self.check_for_same_numbers(triple, poss_values,row)
                        if columns:
                            self.update_row(puzzle,triple,row,columns)

    def check_for_same_numbers (self,triple,poss_values,row):
        '''check for numbers in triple 3 or 2 or 1
        checks for another triple (3 numbers) in row
        '''
        columns = []
        #check that there are between 1-3 occurances of the numbers in triple
        if ((0 < np.count_nonzero(poss_values[row,:,triple[0]-1]) < 4) and
            (0 < np.count_nonzero(poss_values[row,:,triple[1]-1]) < 4) and
            (0 < np.count_nonzero(poss_values[row,:,triple[2]-1]) < 4)):
            #print('all nums in triple occur between 1 and 3 times')
            for cell in range(9):
                #if cell != col:  #need to be different col
                poss_values_cell = self.get_poss_values_cell(poss_values,row,cell)
                if np.any(np.isin(triple,poss_values_cell)):
                    columns.append(cell)
        #Check that numbers are in the same 3 columns
        #print(columns)
        if (0 < len(columns) < 4 and
            self.check_ones_same(triple,poss_values,row,columns) and
            self.at_least_one_triple(triple,poss_values,row,columns)):
            return columns
        else:
            return [] 
    
    def get_poss_values_cell(self,poss_values,row,col):
        return np.nonzero(poss_values[row,col])[0]+1

    def check_ones_same (self,triple,poss_values,row, columns):
        """
        checks to see that any columns with only one match with triple
        are different ie no two ones with the same number.
        Returns true if no two columns with one number have the
        same one numbers 
        """
        match0 = set(triple) & set(poss_values[row,columns[0]])
        match1 = set(triple) & set(poss_values[row,columns[1]])
        match2 = set(triple) & set(poss_values[row,columns[2]])
        #print(match0,match1,match2)
        if len(match0)==1 and len(match1)==1 and match0 == match1:
            return False
        elif len(match0)==1 and len(match2)==1 and match0 == match2:
            return False
        elif len(match1)==1 and len(match2)==1 and match1 == match2:
            return False
        else:
            return True

    def at_least_one_triple(self,triple,poss_values,row,columns):
        """
        checks to see that one of the columns has all three numbers 
        of the triple
        """
        match0 = set(triple) & set(poss_values[row,columns[0]])
        match2 = set(triple) & set(poss_values[row,columns[1]])
        match1 = set(triple) & set(poss_values[row,columns[2]])
        if len(match0) == 3 or len(match1) == 3 or len(match2) == 3:
            return True
        return False

    
    def update_row(self,puzzle,numbers,row,columns):
        num1,num2,num3 = numbers
        col1,col2,col3 = columns
        other_nums = {1,2,3,4,5,6,7,8,9} - set(numbers)
        #numbers to be removed
        remove_nums1 = set(puzzle.possible_values[row,col1]) & other_nums
        remove_nums2 = set(puzzle.possible_values[row,col2]) & other_nums
        remove_nums3 = set(puzzle.possible_values[row,col3]) & other_nums
        remove_nums = (remove_nums1,remove_nums2,remove_nums3) 
        #check for possible_values that are not in numbers
        if (remove_nums1 or remove_nums2 or remove_nums3):
            puzzle.stuck = False
            if verbose: print('Rule 8 at row', row,'cols',col1,col2,col3, 'numbers =',num1,num2,num3 )
            for col, remove_num in zip(columns,remove_nums):
                for num in remove_num:
                    puzzle.possible_values[row,col,num - 1] = 0    #remove all numbers in column col excecpt nums
                
    def check_columns(self,puzzle):
        #looks for the same three poss_values in only three cells in same row
        poss_values = puzzle.get_possible_values()
        for col in range(9):
            for row in range(9):
                poss_values_cell = self.get_poss_values_cell(poss_values,row,col)
                if poss_values_cell.shape[0] > 2:
                    combinations = list(itertools.combinations(poss_values_cell, 3))
                    for triple in combinations:
                        poss_values = puzzle.get_possible_values()  #need update poss_values
                        #Need to check that one column has all three numbers in triple
                        rows = self.check_for_same_numbers_col(triple, poss_values,col)
                        if rows:
                            self.update_column(puzzle,triple,rows,col)

    def check_for_same_numbers_col (self,triple,poss_values,col):
        '''check for numbers in triple 3 or 2 or 1
           checks for another triple (3 numbers) in square
        '''
        rows = []
        #check that there are between 1-3 occurances of the numbers in triple
        if ((0 < np.count_nonzero(poss_values[:,col,triple[0]-1]) < 4) and
            (0 < np.count_nonzero(poss_values[:,col,triple[1]-1]) < 4) and
            (0 < np.count_nonzero(poss_values[:,col,triple[2]-1]) < 4)):
            #print('all nums in triple occur between 1 and 3 times')
            for cell in range(9):
                #if cell != col:  #need to be different col
                poss_values_cell = self.get_poss_values_cell(poss_values,cell,col)
                if np.any(np.isin(triple,poss_values_cell)):
                    rows.append(cell)
        #Check that numbers are in the same 3 columns
        #print(columns)
        if (0 < len(rows) < 4 and
            self.check_ones_same_col(triple,poss_values,rows,col) and
            self.at_least_one_triple_col(triple,poss_values,rows,col)):
            return rows
        return [] 
    
    '''def get_poss_values_cell(self,poss_values,row,col):
        return np.nonzero(poss_values[row,col])[0]+1'''

    def check_ones_same_col (self,triple,poss_values,rows, col):
        """
        checks to see that any columns with only one match with triple
        are different ie no two ones with the same number.
        Returns true if no two columns with one number have the
        same one numbers 
        """
        match0 = set(triple) & set(poss_values[rows[0],col])
        match2 = set(triple) & set(poss_values[rows[1],col])
        match1 = set(triple) & set(poss_values[rows[2],col])
        #print(match0,match1,match2)
        if len(match0)==1 and len(match1)==1 and match0 == match1:
            return False
        elif len(match0)==1 and len(match2)==1 and match0 == match2:
            return False
        elif len(match1)==1 and len(match2)==1 and match1 == match2:
            return False
        else:
            return True

    def at_least_one_triple_col(self,triple,poss_values,rows,col):
        """
        checks to see that one of the rows has all three numbers 
        of the triple
        """
        match0 = set(triple) & set(poss_values[rows[0],col])
        match2 = set(triple) & set(poss_values[rows[1],col])
        match1 = set(triple) & set(poss_values[rows[2],col])
        if len(match0) == 3 or len(match1) == 3 or len(match2) == 3:
            return True
        return False

    
    def update_column(self,puzzle,numbers,rows,col):
        '''
        Looks for 3 cells with 3,2,1 number in column 
        '''
        num1,num2,num3 = numbers
        row1,row2,row3 = rows
        other_nums = {1,2,3,4,5,6,7,8,9} - set(numbers)
        #numbers to be removed
        remove_nums1 = set(puzzle.possible_values[row1,col]) & other_nums
        remove_nums2 = set(puzzle.possible_values[row2,col]) & other_nums
        remove_nums3 = set(puzzle.possible_values[row3,col]) & other_nums
        remove_nums = (remove_nums1,remove_nums2,remove_nums3) 
        #check for possible_values that are not in numbers
        if (remove_nums1 or remove_nums2 or remove_nums3):
            puzzle.stuck = False
            if verbose: print('Rule 8 at rows', row1,row2,row3, 'col',col, 'numbers =',num1,num2,num3 )
            for row, remove_num in zip(rows,remove_nums):
                for num in remove_num:
                    puzzle.possible_values[row,col,num - 1] = 0    #remove all numbers in column col excecpt nums
                
    def check_squares(self,puzzle):
        #looks for the same three poss_values in only three cells in same square
        for square in range(9):
            poss_values = puzzle.possible_values_square(square)
            for cell in range(9):
                poss_values_cell = self.get_poss_values_cell_square(poss_values,cell)
                if poss_values_cell.shape[0] > 2:
                    combinations = list(itertools.combinations(poss_values_cell, 3))
                    for triple in combinations:
                        #Need to check that one column has all three numbers in triple
                        poss_values = puzzle.possible_values_square(square) #update poss_value
                        cells = self.check_for_same_numbers_sq(triple, poss_values)
                        if cells:
                            row1,col1 = puzzle.get_square_coordinates(square,cells[0])
                            row2,col2 = puzzle.get_square_coordinates(square,cells[1])
                            row3,col3 = puzzle.get_square_coordinates(square,cells[2])
                            rows = [row1,row2,row3]
                            cols =[col1,col2,col3]
                            self.update_square(puzzle,triple,rows,cols)

    def check_for_same_numbers_sq (self,triple,poss_values):
        '''check for numbers in triple 3 or 2 or 1
        checks for another triple (3 numbers) in row
        '''
        cells = []
        #check that there are between 1-3 occurances of the numbers in triple
        if ((0 < np.count_nonzero(poss_values[:,triple[0]-1]) < 4) and
            (0 < np.count_nonzero(poss_values[:,triple[1]-1]) < 4) and
            (0 < np.count_nonzero(poss_values[:,triple[2]-1]) < 4)):
            #print('all nums in triple occur between 1 and 3 times')
            for cell in range(9):
                #if cell != col:  #need to be different col
                poss_values_cell = self.get_poss_values_cell_square(poss_values,cell)
                if np.any(np.isin(triple,poss_values_cell)):
                    cells.append(cell)
        #Check that numbers are in the same 3 columns
        #print(columns)
        if (0 < len(cells) < 4 and
            self.check_ones_same_sq(triple,poss_values,cells) and
            self.at_least_one_triple_sq(triple,poss_values,cells)):
            return cells
        else:
            return [] 
    
    def get_poss_values_cell_square(self,poss_values,cell):
        """
        gets possible values of a cell in the values of the square 
        given by poss_values with zero values removed.
        returns 1D numpy array.
          """
        return np.nonzero(poss_values[cell])[0]+1

    def check_ones_same_sq (self,triple,poss_values,cells):
        """
        checks to see that any cells with only one match with triple
        are different ie no two ones with the same number.
        Returns true if no two columns with one number have the
        same one numbers 
        """
        match0 = set(triple) & set(poss_values[cells[0]])
        match2 = set(triple) & set(poss_values[cells[1]])
        match1 = set(triple) & set(poss_values[cells[2]])
        #print(match0,match1,match2)
        if len(match0)==1 and len(match1)==1 and match0 == match1:
            return False
        elif len(match0)==1 and len(match2)==1 and match0 == match2:
            return False
        elif len(match1)==1 and len(match2)==1 and match1 == match2:
            return False
        else:
            return True

    def at_least_one_triple_sq(self,triple,poss_values,cells):
        """
        checks to see that one of the columns has all three numbers 
        of the triple
        """
        match0 = set(triple) & set(poss_values[cells[0]])
        match2 = set(triple) & set(poss_values[cells[1]])
        match1 = set(triple) & set(poss_values[cells[2]])
        if len(match0) == 3 or len(match1) == 3 or len(match2) == 3:
            return True
        return False

    
    def update_square(self,puzzle,numbers,rows,cols):
        num1,num2,num3 = numbers
        row1,row2,row3 = rows
        col1,col2,col3 = cols
        other_nums = {1,2,3,4,5,6,7,8,9} - set(numbers)
        #numbers to be removed
        remove_nums1 = set(puzzle.possible_values[row1,col1]) & other_nums
        remove_nums2 = set(puzzle.possible_values[row2,col2]) & other_nums
        remove_nums3 = set(puzzle.possible_values[row3,col3]) & other_nums
        remove_nums = (remove_nums1,remove_nums2,remove_nums3) 
        #check for possible_values that are not in numbers
        if (remove_nums1 or remove_nums2 or remove_nums3):
            puzzle.stuck = False
            if verbose:
                print('Rule 8 square', 'rows=', row1,row2,row3,'columns=', col1,col2,col3, 'numbers =',num1,num2,num3 )
            for row,col, remove_num in zip(rows,cols,remove_nums):
                for num in remove_num:
                    puzzle.possible_values[row,col,num - 1] = 0    #remove all numbers in cell excecpt nums

class Rule9(Rules):
    '''
    Looks for 2 numbers in three cells with total of 3 numbers inthe 3 cells
    i.e. (1,2),(1,3),(2,3).  
    '''
    def __init__(self):
        pass

    def check_rule9(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
        self.check_squares(puzzle)

    def check_rows(self,puzzle):
        '''
        checks for three twos in rows
        '''
        for row in range(9):
            twos = np.zeros([9,2], dtype=int)  
            for col in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                #put cells with 2 values in twos    
                if poss_nums.shape[0] == 2:  #number of poss_nums are 2
                    two_nums = np.nonzero(puzzle.possible_values[row,col])[0] +1
                    twos[col,:] = two_nums
            #check that there are at least 3 cells with two possible_values
            twos_rows = sum([np.any(row) for row in twos])
            if twos_rows > 2: #3 or more twos
                #get all combinations of 3 twos
                twos_only = twos[~np.all(twos == 0, axis=1)]
                #print('twos_only', twos_only,'twos', twos)
                combinations = list(itertools.combinations(twos_only, 3))
                for three_arrays in combinations:
                    triple = set([element for array in three_arrays  for element in array])
                    #check that there are 3 different numbers in the 3 cells and
                    # check that on two cells are the same
                    if len(triple) == 3 and self.no_two_equal(three_arrays): 
                        columns = self.match_columns(three_arrays, twos)
                        #print('three_arrays =', three_arrays,'columns=',columns)
                        self.update_row(puzzle,triple,row,columns)

    def no_two_equal(self,three_arrays):
        #makes sure no two arrays have the same elements
        #returns True if none are equal, False if any are equal
        #print('three_arrays', three_arrays)
        if (np.all(three_arrays[0] == three_arrays[1]) or
            np.all(three_arrays[0] == three_arrays[2]) or
            np.all(three_arrays[2] == three_arrays[1])):
            return False
        return True
        
    def match_columns(self,three_array, twos):
        # finds the columns that the elements of three_arrays are from
        # returns a list of three ints which are the array indices.
        matches = []
        for array in three_array:
            matches.append( np.where(np.all(twos == array, axis=1))[0][0])
        return matches

    def update_row(self,puzzle,triple,row,cols_matches):
        """
        remove any of the 3 numbers from other cells in the row.
        (if all are in same square the update_threes_square will tkae care of them)
        updates possible_values
        inputs: num_1: int first of three values
                num_2 int second of three values
                num_3 int third of three values
                row: int
                cols_match: np.array shape [3,] that gives the columns that match
        """
        num_1,num_2,num_3 = triple
        #print(num_1,num_2,num_3,row,cols_matches)
        for col in range(9):
            #delete values in other cells in row
            if col not in cols_matches:
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 9 row at ', row,col, 'numbers =',num_1,num_2,num_3)
                        #print('row =',row,'columns =',matches,'threes =', threes,'three_nums =', three_nums) 
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0       

    def check_columns(self,puzzle):
        '''
        checks for three twos in columns
        '''
        for col in range(9):
            twos = np.zeros([9,2], dtype=int)  
            for row in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(puzzle.possible_values[row,col])[0]
                #put cells with 2 values in twos    
                if poss_nums.shape[0] == 2:  #number of poss_nums are 2
                    two_nums = np.nonzero(puzzle.possible_values[row,col])[0] +1
                    twos[row,:] = two_nums
            #check that there are at least 3 cells with two possible_values
            twos_rows = sum([np.any(row) for row in twos])
            if twos_rows > 2: #3 or more twos
                #get all combinations of 3 twos
                twos_only = twos[~np.all(twos == 0, axis=1)]
                #print('twos_only', twos_only,'twos', twos)
                combinations = list(itertools.combinations(twos_only, 3))
                for three_arrays in combinations:
                    triple = set([element for array in three_arrays  for element in array])
                    #check that there are 3 different numbers in the 3 cells and
                    # check that on two cells are the same
                    if len(triple) == 3 and self.no_two_equal(three_arrays): 
                        rows_matches = self.match_columns(three_arrays, twos)
                        self.update_column(puzzle,triple,col,rows_matches)
    
    def update_column(self,puzzle,triple,col,rows_matches):
        """
        remove any of the 3 numbers from other cells in the row.
        (if all are in same square the update_threes_square will tkae care of them)
        updates possible_values
        inputs: num_1: int first of three values
                num_2 int second of three values
                num_3 int third of three values
                row: int
                cols_match: np.array shape [3,] that gives the columns that match
        """
        num_1,num_2,num_3 = triple
        #print(num_1,num_2,num_3,row,cols_matches)
        for row in range(9):
            #delete values in other cells in row
            if row not in rows_matches:
                if (puzzle.possible_values[row,col,num_1-1] != 0 or 
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 9 row at ', row,col, 'numbers =',num_1,num_2,num_3)
                        #print('row =',row,'columns =',matches,'threes =', threes,'three_nums =', three_nums) 
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0  

    def check_squares(self,puzzle):
        '''
        checks for three twos in squares
        '''
        for square in range(9):
            poss_values = puzzle.possible_values_square(square)
            twos = np.zeros([9,2], dtype=int)  
            for cell in range(9):
                #find number of possible_values in cell
                poss_nums = np.nonzero(poss_values[cell])[0] +1
                #put cells with 2 values in twos    
                if poss_nums.shape[0] == 2:  #number of poss_nums are 2
                    two_nums = poss_nums
                    twos[cell,:] = poss_nums
            #check that there are at least 3 cells with two possible_values
            twos_rows = sum([np.any(row) for row in twos])
            if twos_rows > 2: #3 or more twos
                #get all combinations of 3 twos
                twos_only = twos[~np.all(twos == 0, axis=1)]
                #print('twos_only', twos_only,'twos', twos)
                combinations = list(itertools.combinations(twos_only, 3))
                for three_arrays in combinations:
                    triple = set([element for array in three_arrays  for element in array])
                    #check that there are 3 different numbers in the 3 cells and
                    # check that on two cells are the same
                    if len(triple) == 3 and self.no_two_equal(three_arrays): 
                        cell_matches = self.match_columns(three_arrays, twos)
                        self.update_square(puzzle,triple,square,cell_matches)
                        #print(triple,cell_matches)
    
    def update_square(self,puzzle,triple,square,cell_matches):
        """
        remove any of the 3 numbers from other cells in the square.
        updates possible_values
        inputs: triple a set that has the 3 numbers
                square: int
                cell_match: np.array shape [3,] that gives the cell number in the square that match
        """
        num_1,num_2,num_3 = triple
        row1,col1 = puzzle.get_square_coordinates(square,cell_matches[0])
        row2,col2 = puzzle.get_square_coordinates(square,cell_matches[1])
        row3,col3 = puzzle.get_square_coordinates(square,cell_matches[2])
        #print(num_1,num_2,num_3,row,cols_matches)
        for cell in range(9):
            #delete values in other cells in row
            if cell not in cell_matches:
                row,col = puzzle.get_square_coordinates(square,cell)
                #check if number in ther cells
                if (puzzle.possible_values[row,col,num_1-1] != 0 or
                    puzzle.possible_values[row,col,num_2-1] != 0 or
                    puzzle.possible_values[row,col,num_3-1] != 0):
                    puzzle.stuck = False
                    if verbose: 
                        print('Rule 9 row at ', row,col, 'numbers =',num_1,num_2,num_3)
                        #print('row =',row,'columns =',matches,'threes =', threes,'three_nums =', three_nums) 
                puzzle.possible_values[row,col,num_1-1] = 0
                puzzle.possible_values[row,col,num_2-1] = 0
                puzzle.possible_values[row,col,num_3-1] = 0
            
    def get_poss_values_cell_square(self,poss_values,cell):
        """
        gets possible values of a cell in the values of the square 
        given by poss_values with zero values removed.
        returns 1D numpy array.
          """
        return np.nonzero(poss_values[cell])[0]+1

class Rule10(Rules):
    '''
    Looks for one number in 4 cells in a square pattern, ie in same 2 rows and 2 columns.
    The number can not appear elsewhere in the rows or in the columns (not both).
    When found remove the number from other cells in the rows or columns. 
    '''

    def __init__(self):
        pass

    def check_rule10(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)

    def check_rows(self, puzzle):
        #look for all numbers forming a square with only 2 occurances in row

        #find all numbers with two occurances in a row
        row_twos = [] # list of numbers in row occurrung twice (number, row, col1, col2)
        row_freq = np.count_nonzero(puzzle.possible_values, axis = 1) #number of times numbers occurs in row returns 9x9 array
        for row in range(9):
            for twos in np.where(row_freq[row] ==2)[0]: # loops thru the positions of 2 occurances of numbers
                columns = np.where(puzzle.possible_values[row,:,twos] == twos +1)[0] #finds the columns where twos occur 
                if columns.shape[0] > 0:  # some value of twos found
                    row_twos.append ({'number':twos +1,'row':row, 'col1':columns[0],'col2':columns[1]})

        #check if numbers in same column
        for i in range(len(row_twos)):
            two = row_twos[i]
            rest_twos = row_twos[i+1:] 
            #num, row, col1,col2 = two
            other_rows = [lst for lst in rest_twos if lst['number'] == two['number']]
            #print('two',two,'other',other_rows)
            for other in other_rows:
                if (two['col1']== other['col1'] and
                    two['col2'] == other['col2']):
                    self.update_rows(puzzle,two,other)

    def update_rows(self,puzzle, two1, two2):
        number = two1['number']
        row1 = two1['row']
        row2 = two2['row']
        col1 = two1['col1']
        col2 = two1['col2']
        col_freq = np.count_nonzero(puzzle.possible_values, axis = 0)
        #check col1
        if col_freq[col1,number-1] > 2:
            puzzle.stuck = False
            for row, value in enumerate(puzzle.possible_values[:,col1,number-1]):
                if value == number and row not in [row1, row2]:
                    puzzle.possible_values[row,col1,number-1] = 0
                    if verbose: 
                        print('Rule10 removed row', row, 'col', col1, 'number', number)
        #check col2
        if col_freq[col2,number-1] > 2:
            puzzle.stuck = False
            for row, value in enumerate(puzzle.possible_values[:,col2,number-1]):
                if value == number and row not in [row1, row2]:
                    puzzle.possible_values[row,col2,number-1] = 0
                    if verbose: 
                        print('Rule10 removed row', row, 'col', col2, 'number', number)
               
        

    def check_columns(self, puzzle):
        #look for all numbers forming a square with only 2 occurances in row

        #find all numbers with two occurances in a row
        col_twos = [] # list of numbers in row occurrung twice (number, row, col1, col2)
        col_freq = np.count_nonzero(puzzle.possible_values, axis = 0) #number of times numbers occurs in row returns 9x9 array
        for col in range(9):
            for twos in np.where(col_freq[col] ==2)[0]: # loops thru the positions of 2 occurances of numbers
                rows = np.where(puzzle.possible_values[:,col,twos] == twos +1)[0] #finds the columns where twos occur 
                if rows.shape[0] > 0:
                    col_twos.append ({'number':twos +1,'col':col, 'row1':rows[0],'row2':rows[1]})
        

        #check if numbers in same row
        for i in range(len(col_twos)):
            two = col_twos[i]
            rest_twos = col_twos[i+1:] 
            #num, row, col1,col2 = two
            other_cols = [lst for lst in rest_twos if lst['number'] == two['number']]
            for other in other_cols:
                if (two['row1']== other['row1'] and
                    two['row2'] == other['row2']):
                    self.update_columns(puzzle,two,other)

    def update_columns(self,puzzle, two1, two2):
        number = two1['number']
        row1 = two1['row1']
        row2 = two1['row2']
        col1 = two1['col']
        col2 = two2['col']
        row_freq = np.count_nonzero(puzzle.possible_values, axis = 1)
        #check row1
        if row_freq[row1,number-1] > 2:
            puzzle.stuck = False
            for col, value in enumerate(puzzle.possible_values[row1,:,number-1]):
                if value == number and col not in [col1, col2]:
                    puzzle.possible_values[row1,col,number-1] = 0
                    if verbose: 
                        print('Rule10 removed row', row1, 'col', col, 'number', number)
        #check row2
        if row_freq[row2,number-1] > 2:
            puzzle.stuck = False
            for col, value in enumerate(puzzle.possible_values[row2,:,number-1]):
                if value == number and col not in [col1, col2]:
                    puzzle.possible_values[row2,col,number-1] = 0
                    if verbose: 
                        print('Rule10 removed row', row2, 'col', col, 'number', number)
               
class Rule11(Rules):
    '''
    Looks for one number in 4 cells in a square pattern, ie in same 2 rows and 2 columns.
    The number can not appear elsewhere in the rows or in the columns (not both).
    When found remove the number from other cells in the rows or columns. 
    '''

    def __init__(self):
        pass

    def check_rule11(self,puzzle):
        self.check_rows(puzzle)
        self.check_columns(puzzle)
    
    def check_rows(self, puzzle):
        #look for three rows with 2 or 3 occurances of a number in the row (need one row with 3)

        #find all numbers with three or twos occurances in a row
        row_twos_threes = [] # list of numbers in row occurrung twice (number, row, col1, col2)
        row_freq = np.count_nonzero(puzzle.possible_values, axis = 1) #number of times numbers occurs in row returns 9x9 array       
        for row in range(9): # looking for rows wothe 2 or 3 of a number in them
            twos_list = np.where(row_freq[row] ==2)[0] # loops thru the positions of 2 occurances of numbers
            threes_list = np.where(row_freq[row] ==3)[0]
            twos_and_threes = np.concatenate((twos_list, threes_list))
            for two_three in twos_and_threes: # loops thru the positions of 2/3 occurances of numbers
                columns = np.where(puzzle.possible_values[row,:,two_three] == two_three +1)[0] #finds the columns where twos/threes occur 
                #print(columns)
                if columns.shape[0] > 0 and len(columns) == 2:  # some value of twos found
                    row_twos_threes.append ({'number':two_three +1,'row':row, 'col1':columns[0],'col2':columns[1], 'col3':None})
        
                if columns.shape[0] > 0 and len(columns) == 3:  # some value of twos found
                    row_twos_threes.append ({'number':two_three +1,'row':row, 'col1':columns[0],'col2':columns[1],'col3':columns[2]})
        #print(row_twos_threes)
        
        #check if numbers in same column
        for i in range(len(row_twos_threes)):
            row_two_three = row_twos_threes[i]
            if row_two_three['col3']: #if there are three columns with same number in row
                rest = row_twos_threes[0:i] + row_twos_threes[i+1:] 
                other_rows = [lst for lst in rest if lst['number'] == row_two_three['number']]          
                matches = self.two_matches(row_two_three, other_rows) #checks if there are matched in other rows
                if len(matches) == 3:
                    self.update_rows(puzzle,matches)

    def two_matches (self,row1,others):
        '''
        checks if other matches for 2 of 3 of same number in other rows
        '''
        output_matches = [row1]
        for i in range (len(others)):
            other = others[i]
            rest = others[0:i] + others[i+1:]
            row1_cols = set([row1['col1'],row1['col2'], row1['col3']])
            row1_cols.discard(None)
            other_cols = set([other['col1'],other['col2'], other['col3']])
            other_cols.discard(None)
            #print('row1_col =',row1_cols,'row=', other['row'],'other_cols=',other_cols)
            matches = row1_cols & other_cols
            total_cols = row1_cols |  other_cols
            #print('matches=',matches, 'total_cols', total_cols)
            if (len(matches) ==  2 or len(matches) == 3) and len(total_cols) == 3:
                output_matches.append(other)
        #print('output_matches=',output_matches)
        return output_matches
    
    def update_rows(self,puzzle, matches):
        number = matches[0]['number']
        match1 = matches[0]
        match2 = matches[1]
        match3 = matches[2]
        row1 = match1['row']
        row2 = match2['row']
        row3 = match3['row']
        col1 = match1['col1']
        col2 = match1['col2']
        col3 = match1['col3']
        col_freq = np.count_nonzero(puzzle.possible_values, axis = 0)
        match_col1_freq = self.match_col_freq(puzzle,number,col1,row1,row2,row3)
        match_col2_freq = self.match_col_freq(puzzle,number,col2,row1,row2,row3)
        match_col3_freq = self.match_col_freq(puzzle,number,col3,row1,row2,row3)
        #check col1
        if col_freq[col1,number-1] > match_col1_freq: #greater than the number of matches in that column
            puzzle.stuck = False
            for row, value in enumerate(puzzle.possible_values[:,col1,number-1]):
                if value == number and row not in [row1, row2, row3]:
                    puzzle.possible_values[row,col1,number-1] = 0
                    if verbose: 
                        print('Rule11 removed row', row, 'col', col1, 'number', number)
        #check col2
        if col_freq[col2,number-1] > match_col2_freq:
            puzzle.stuck = False
            for row, value in enumerate(puzzle.possible_values[:,col2,number-1]):
                if value == number and row not in [row1, row2, row3]:
                    puzzle.possible_values[row,col2,number-1] = 0
                    if verbose: 
                        print('Rule11 removed row', row, 'col', col2, 'number', number)
        #check col3
        if col_freq[col3,number-1] > match_col3_freq: #greater than the number of matches in that column
            puzzle.stuck = False
            for row, value in enumerate(puzzle.possible_values[:,col3,number-1]):
                if value == number and row not in [row1, row2, row3]:
                    puzzle.possible_values[row,col3,number-1] = 0
                    if verbose: 
                        print('Rule11 removed row', row, 'col', col3, 'number', number)
   
    def match_col_freq(self, puzzle, number, col, row1,row2,row3):
        if puzzle.get_poss_values_cell(row1,col,number) == 0: #no number in column
            num1 = 0
        else:
             num1 = 1
        if puzzle.get_poss_values_cell(row2,col,number) == 0: 
            num2 = 0
        else:
             num2 = 1
        if puzzle.get_poss_values_cell(row3,col,number) == 0: 
            num3 = 0
        else:
             num3 = 1
        return num1 + num2 +num3

    def check_columns(self, puzzle):
        #look for three columns with 2 or 3 occurances of a number in the column (need one row with 3)

        #find all numbers with three or twos occurances in a row
        col_twos_threes = [] # list of numbers in row occurrung twice (number, row, col1, col2)
        col_freq = np.count_nonzero(puzzle.possible_values, axis = 0) #number of times numbers occurs in row returns 9x9 array       
        for col in range(9): # looking for rows wothe 2 or 3 of a number in them
            twos_list = np.where(col_freq[col] ==2)[0] # loops thru the positions of 2 occurances of numbers
            threes_list = np.where(col_freq[col] ==3)[0]
            twos_and_threes = np.concatenate((twos_list, threes_list))
            for two_three in twos_and_threes: # loops thru the positions of 2/3 occurances of numbers
                rows = np.where(puzzle.possible_values[:,col,two_three] == two_three +1)[0] #finds the rows where twos/threes occur 
                #print(columns)
                if rows.shape[0] > 0 and len(rows) == 2:  # some value of twos found
                    col_twos_threes.append ({'number':two_three +1,'col':col, 'row1':rows[0],'row2':rows[1], 'row3':None})
        
                if rows.shape[0] > 0 and len(rows) == 3:  # some value of twos found and 3 rows found
                    col_twos_threes.append ({'number':two_three +1,'col':col, 'row1':rows[0],'row2':rows[1],'row3':rows[2]})
        #print(row_twos_threes)
        
        #check if numbers in same row
        for i in range(len(col_twos_threes)):
            col_two_three = col_twos_threes[i]
            if col_two_three['row3']: #if there are three columns with same number in row
                rest = col_twos_threes[0:i] + col_twos_threes[i+1:] 
                other_cols = [lst for lst in rest if lst['number'] == col_two_three['number']]
                #print('row_two_three',col_two_three,'other',other_cols)        
                matches = self.two_matches_cols(col_two_three, other_cols) #checks if there are matched in other cols
                if len(matches) == 3:
                    self.update_columns(puzzle,matches)
    
    def two_matches_cols (self,col1,others):
        '''
        checks if other matches for 2 of 3 of same number in other rows
        '''
        output_matches = [col1]
        for i in range (len(others)):
            other = others[i]
            rest = others[0:i] + others[i+1:]
            col1_rows = set([col1['row1'],col1['row2'], col1['row3']])
            col1_rows.discard(None)
            other_rows = set([other['row1'],other['row2'], other['row3']])
            other_rows.discard(None)
            matches = col1_rows & other_rows
            total_rows = col1_rows |  other_rows
            if (len(matches) ==  2 or len(matches) == 3) and len(total_rows) == 3: #matches in 2 or 3 rows and 3 rows have num total
                output_matches.append(other)
        return output_matches
        
    def update_columns(self,puzzle, matches):
        '''removes number number not in the 3 columns from rows
            inputs: puzzle instance of Puzzle class
                matches list of dictionarires with number, rows and columns of a match
        '''
        number = matches[0]['number']
        match1 = matches[0]
        match2 = matches[1]
        match3 = matches[2]
        col1 = match1['col']
        col2 = match2['col']
        col3 = match3['col']
        row1 = match1['row1']
        row2 = match1['row2']
        row3 = match1['row3']
        row_freq = np.count_nonzero(puzzle.possible_values, axis = 1)
        match_row1_freq = self.match_row_freq(puzzle,number,row1,col1,col2,col3)
        match_row2_freq = self.match_row_freq(puzzle,number,row2,col1,col2,col3)
        match_row3_freq = self.match_row_freq(puzzle,number,row3,col1,col2,col3)
        #check col1
        if row_freq[row1,number-1] > match_row1_freq: #greater than the number of matches in that column
            puzzle.stuck = False
            for col, value in enumerate(puzzle.possible_values[row1,:,number-1]):
                if value == number and col not in [col1, col2, col3]:
                    puzzle.possible_values[row1,col,number-1] = 0
                    if verbose: 
                        print('Rule11 removed row', row1, 'col', col, 'number', number)
        #check col2
        if row_freq[row2,number-1] > match_row2_freq:
            puzzle.stuck = False
            for col, value in enumerate(puzzle.possible_values[row2,:,number-1]):
                if value == number and col not in [col1, col2, col3]:
                    puzzle.possible_values[row2,col,number-1] = 0
                    if verbose: 
                        print('Rule11 removed row', row2, 'col', col, 'number', number)
        #check col3
        if row_freq[row3,number-1] > match_row3_freq:
            puzzle.stuck = False
            for col, value in enumerate(puzzle.possible_values[row3,:,number-1]):
                if value == number and col not in [col1, col2, col3]:
                    puzzle.possible_values[row3,col,number-1] = 0
                    if verbose: 
                        print('Rule11 removed row', row3, 'col', col, 'number', number)
            
    def match_row_freq(self,puzzle,number,row,col1,col2,col3):
        if puzzle.get_poss_values_cell(row,col1,number) == 0:  #no number in cell
            num1 = 0
        else:
             num1 = 1
        if puzzle.get_poss_values_cell(row,col2,number) == 0: 
            num2 = 0
        else:
             num2 = 1
        if puzzle.get_poss_values_cell(row,col3,number) == 0: 
            num3 = 0
        else:
             num3 = 1
        return num1 + num2 +num3   
        
          

#%%