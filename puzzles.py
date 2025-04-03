#%%
import numpy as np

sudoku0 = np.array(
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
)
sudoku1 = np.array(
    [
        [0, 0, 0, 7, 0, 0, 5, 0, 0],
        [0, 2, 9, 0, 3, 0, 0, 8, 0],
        [7, 1, 0, 6, 8, 0, 0, 0, 0],
        [0, 6, 7, 0, 0, 0, 3, 0, 5],
        [9, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0, 7, 9],
        [6, 4, 2, 8, 0, 3, 0, 1, 7],
        [3, 7, 0, 4, 0, 9, 2, 5, 8],
        [0, 0, 0, 2, 0, 1, 6, 0, 0],
    ]
)

sudoku2 = np.array(
    [
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [2, 5, 0, 1, 0, 7, 6, 0, 0],
        [0, 0, 0, 3, 4, 0, 9, 0, 0],
        [8, 0, 0, 4, 7, 0, 0, 0, 0],
        [7, 2, 0, 8, 5, 0, 3, 9, 4],
        [0, 0, 0, 0, 2, 0, 0, 1, 0],
        [0, 7, 9, 0, 0, 5, 0, 0, 3],
        [0, 0, 0, 7, 0, 0, 0, 0, 9],
        [5, 0, 0, 0, 0, 9, 0, 4, 0],
    ]
)

sudoku3 = np.array(
    [
        [0, 6, 3, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 8, 0, 0, 9, 0, 0],
        [8, 0, 0, 6, 7, 0, 0, 0, 5],
        [3, 8, 0, 0, 0, 0, 6, 9, 0],
        [0, 1, 0, 2, 0, 4, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 8, 0, 0],
        [7, 3, 0, 0, 1, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 3, 0, 0, 1],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

sudoku4 = np.array(
    [
        [4, 0, 0, 6, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 9, 8, 0, 2],
        [0, 7, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [1, 0, 5, 9, 0, 0, 0, 4, 0],
        [5, 0, 0, 0, 0, 0, 0, 8, 0],
        [2, 0, 8, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 3, 0],
    ]
)

sudoku5 = np.array(
    [
        [0, 0, 9, 0, 0, 7, 0, 0, 4],
        [0, 0, 0, 5, 0, 4, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [5, 4, 7, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 6, 0],
        [0, 9, 0, 0, 0, 0, 0, 3, 2],
        [0, 0, 1, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 1, 8, 0],
        [7, 0, 0, 0, 9, 0, 0, 0, 0],
    ]
)

sudoku6 = np.array([[5,0,0,6,0,0,9,0,7],
                    [0,0,0,0,2,0,0,0,5],
                    [0,0,3,0,0,0,4,0,6],
                    [0,0,8,0,0,0,5,0,0],
                    [0,0,5,0,0,9,0,0,4],
                    [1,2,6,0,4,0,0,0,0],
                    [8,6,0,0,0,7,0,0,0],
                    [0,0,9,0,0,0,0,0,0],
                    [0,0,0,1,0,8,7,0,0]])

sudoku7 = np.array([[0,0,0,0,0,3,5,0,0],
                    [3,7,0,0,0,0,4,8,1],
                    [0,0,0,1,0,8,9,3,0],
                    [4,0,0,9,2,0,3,0,0],
                    [7,0,0,0,0,4,0,0,0],
                    [1,0,0,0,0,0,6,9,4],
                    [6,0,0,4,3,9,0,0,0],
                    [0,0,0,6,0,2,0,4,3],
                    [0,3,4,0,0,0,2,6,9]])

sudoku8 = np.array([[0,0,0,4,0,0,0,0,0],
                    [0,2,0,0,3,0,5,0,6],
                    [0,0,5,0,0,0,7,4,0],
                    [6,0,0,0,1,0,0,8,7],
                    [7,3,0,0,6,0,0,0,0],
                    [0,9,0,0,0,0,0,0,0],
                    [0,0,0,0,0,7,1,0,3],
                    [0,0,0,8,0,0,0,0,0],
                    [0,0,2,0,4,0,0,9,0]])

sudoku9 = np.array([[7,5,0,0,0,4,0,0,0],
                    [0,8,0,0,0,5,0,0,9],
                    [9,0,6,0,3,0,0,0,0],
                    [0,0,5,0,0,0,0,0,0],
                    [0,0,0,0,4,9,7,8,3],
                    [0,0,0,8,0,1,2,5,0],
                    [0,0,9,0,0,0,0,0,0],
                    [0,1,0,0,0,0,3,4,0],
                    [0,0,0,0,2,0,1,0,0]])

sudoku10 = np.array([[9,0,7,0,2,0,0,0,0],
                     [0,0,5,0,0,0,0,0,6],
                     [0,0,1,4,0,9,0,0,0],
                     [0,0,0,0,0,6,0,0,3],
                     [0,0,0,0,0,8,2,0,0],
                     [0,2,4,3,0,0,0,0,0],
                     [0,0,0,0,0,0,0,7,0],
                     [5,8,0,0,0,1,0,9,2],
                     [0,0,0,9,6,0,0,0,0]])

sudoku11 = np.array([[5,0,0,0,1,0,0,7,0],
                     [7,0,0,5,0,0,0,0,0],
                     [0,0,3,6,0,0,4,0,0],
                     [0,0,0,0,5,2,0,0,0],
                     [8,0,0,3,0,0,0,0,0],
                     [4,9,0,0,0,0,0,0,7],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,1,0,2,3,0,5,0],
                     [0,4,0,1,0,0,0,0,8]])

sudoku12 = np.array([[9,0,0,0,0,0,0,4,1],
                     [0,0,0,0,5,0,8,0,0],
                     [0,8,0,3,0,0,0,0,0],
                     [4,0,0,8,0,0,0,0,5],
                     [0,0,0,7,0,0,0,0,0],
                     [0,2,6,4,0,0,0,0,0],
                     [0,0,7,0,0,0,1,3,0],
                     [1,0,0,6,0,0,5,0,0],
                     [2,4,0,0,0,7,0,0,6]])

sudoku13 = np.array([[0,2,4,0,0,3,0,9,0],
                     [0,0,0,0,0,0,5,3,7],
                     [0,0,0,0,6,0,0,0,1],
                     [0,3,0,0,0,0,0,0,5],
                     [0,8,0,0,0,0,0,0,0],
                     [0,0,1,0,9,0,0,6,0],
                     [5,0,0,0,2,0,0,0,0],
                     [8,7,9,0,0,5,0,0,3],
                     [0,0,3,0,0,0,0,0,0]])

sudoku14 = np.array([[0,0,0,0,0,0,0,0,0],
                     [0,9,5,2,3,4,6,7,0],
                     [0,3,0,0,0,0,0,9,0],
                     [0,2,0,9,1,3,0,4,0],
                     [0,5,0,7,0,2,0,3,0],
                     [0,6,0,4,8,5,0,1,0],
                     [0,7,0,0,0,0,0,8,0],
                     [0,8,3,6,2,7,9,5,0],
                     [0,0,0,0,0,0,0,0,0]])

sudoku15 = np.array([[5,0,9,0,0,0,0,0,0],
                     [0,2,0,0,1,0,6,0,7],
                     [0,0,8,0,0,0,2,0,0],
                     [0,0,0,0,0,0,0,0,2],
                     [3,0,2,9,0,0,5,0,0],
                     [0,6,0,0,8,0,0,7,0],
                     [0,4,0,0,7,0,0,0,0],
                     [0,0,0,6,4,1,0,0,0],
                     [0,0,0,0,0,3,0,0,0]])

sudoku16 = np.array([[0,0,0,9,0,0,0,5,0],
                     [0,0,3,0,4,0,1,0,6],
                     [0,4,0,2,0,0,0,8,0],
                     [7,0,8,0,0,0,0,0,0],
                     [0,3,0,0,0,0,0,6,0],
                     [0,0,0,0,0,0,5,0,4],
                     [0,6,0,0,0,1,0,7,0],
                     [4,0,2,0,5,0,3,0,0],
                     [0,9,0,0,0,8,0,0,0]])

sudoku17 = np.array([[0, 0, 0, 4, 0, 3, 0, 0, 0],
                  [0, 0, 3, 0, 8, 0, 7, 0, 0],
                  [0, 5, 0, 0, 0, 0, 0, 1, 0],
                  [5, 0, 0, 0, 1, 0, 0, 0, 9],
                  [0, 1, 0, 5, 0, 8, 0, 2, 0],
                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
                  [0, 6, 0, 0, 0, 0, 0, 9, 0],
                  [0, 0, 7, 0, 4, 0, 2, 0, 0],
                  [0, 0, 0, 7, 0, 9, 0, 0, 0]])

sudoku18 = np.array([[0,4,0,0,0,2,6,0,0],
                     [0,0,2,3,0,0,0,0,9],
                     [0,9,3,0,0,0,0,0,0],
                     [0,0,5,0,0,0,0,9,4],
                     [0,1,8,0,0,0,0,0,0],
                     [7,0,0,5,0,3,0,0,0],
                     [0,0,1,0,0,7,3,0,5],
                     [0,0,0,2,0,0,0,7,0],
                     [0,0,0,0,0,8,1,0,0]])

sudoku19 = np.array([[0,0,9,7,0,0,0,0,1],
                     [0,0,6,3,0,0,0,8,0],
                     [8,0,0,0,0,0,7,0,0],
                     [0,3,0,0,0,6,0,0,4],
                     [0,0,5,0,0,0,9,0,0],
                     [1,0,0,2,0,0,0,3,0],
                     [0,0,4,0,0,0,0,0,5],
                     [0,7,0,0,0,1,4,0,0],
                     [6,0,0,0,0,5,2,0,0]])

sudoku20 = np.array([[0,0,0,0,0,0,0,0,0],
                     [0,0,9,0,2,0,7,0,6],
                     [0,0,0,8,0,3,0,4,0],
                     [0,0,4,0,8,0,5,0,9],
                     [0,0,0,0,0,0,0,0,0],
                     [3,0,8,0,4,0,2,0,0],
                     [0,5,0,6,0,2,0,0,0],
                     [7,0,3,0,1,0,9,0,0],
                     [0,0,0,0,0,0,0,0,0]])

sudoku21 = np.array([[0,9,8,0,0,0,0,0,2],
                     [6,0,0,4,7,0,0,0,9],
                     [0,0,0,0,0,1,3,0,0],
                     [5,0,3,0,0,0,0,6,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,7,0,0,0,0,5,0,4],
                     [0,0,6,1,0,0,0,0,0],
                     [3,0,0,0,9,2,0,0,8],
                     [2,0,0,0,0,0,4,3,0]])

sudoku22 = np.array([[0,0,0,2,0,0,7,0,0],
                    [0,0,5,0,9,0,0,4,0],
                    [0,4,0,5,0,0,0,0,8],
                    [0,0,4,0,0,0,0,9,0],
                    [0,0,0,6,0,7,0,0,0],
                    [0,7,0,0,0,0,2,0,0],
                    [3,0,0,0,0,8,0,5,0],
                    [0,1,0,0,5,0,4,0,0,],
                    [0,0,8,0,0,3,0,0,0]])

sudoku23 = np.array([[1,0,3,0,0,0,6,0,9],
                     [0,0,0,9,0,7,0,0,0],
                     [0,0,0,0,5,0,0,0,0],
                     [2,0,0,8,0,4,0,0,6],
                     [0,0,7,0,0,0,2,0,0],
                     [5,0,0,7,0,6,0,0,1],
                     [0,0,0,0,7,0,0,0,0],
                     [0,0,0,2,0,1,0,0,0],
                     [9,0,2,0,0,0,8,0,3]])

sudoku24 = np.array([[0,4,0,2,0,0,9,0,0],
                     [0,0,9,0,0,8,0,4,0],
                     [1,0,0,0,6,0,0,0,8],
                     [0,8,0,0,0,3,0,0,0],
                     [0,0,7,0,0,0,8,0,0],
                     [0,0,0,4,0,0,0,1,0],
                     [3,0,0,0,7,0,0,0,2],
                     [0,9,0,6,0,0,4,0,0],
                     [0,0,2,0,0,1,0,6,0]])

sudoku25 = np.array([[0,8,0,2,0,0,0,9,0],
                     [0,6,0,0,0,0,0,7,3],
                     [0,0,1,0,0,8,2,0,0],
                     [0,0,0,0,0,0,9,0,0],
                     [5,0,0,0,6,0,0,0,4],
                     [1,0,7,9,0,0,0,3,0],
                     [0,0,0,0,0,0,0,0,2],
                     [8,2,4,0,7,0,0,0,0],
                     [0,0,0,1,0,0,0,0,8]])

sudoku26 = np.array([[7,0,0,0,0,0,0,5,9],
                     [2,0,6,0,0,0,0,0,0],
                     [4,0,0,8,0,0,0,0,1],
                     [0,3,0,0,0,0,9,6,0],
                     [0,0,0,0,4,0,0,3,0],
                     [0,0,0,0,0,5,7,0,0],
                     [0,0,0,0,2,0,8,0,0],
                     [0,8,0,1,0,6,0,0,0],
                     [0,0,5,0,0,3,0,2,0]])

#%%