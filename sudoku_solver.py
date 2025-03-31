#%%
# This is a Windows Sudoku Solver application built with PySide6

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                              QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout,
                              QLabel, QComboBox, QStatusBar, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QFont, QColor
import sys
import random
import time

class SudokuCell(QLineEdit):
    valueChanged = Signal(int, int, str)
    
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.original = False
        self.setFixedSize(40, 40)
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)
        self.setFont(QFont("Arial", 14))  
        # Only allow numbers 1-9
        self.setValidator(lambda x: x.isdigit() and 1 <= int(x) <= 9 if x else True)
        
        # Base style
        style = """
            QLineEdit {
                font-size: 16px;
                background: white;
                border: 1px solid #cccccc;
            """
        
        # Add borders based on position
        borders = []
        
        # Top border
        if row == 0:
            borders.append("border-top: 3px solid black")
        elif row % 3 == 0:
            borders.append("border-top: 2px solid black")
            
        # Bottom border
        if row == 8:
            borders.append("border-bottom: 3px solid black")
            
        # Left border
        if col == 0:
            borders.append("border-left: 3px solid black")
        elif col % 3 == 0:
            borders.append("border-left: 2px solid black")
            
        # Right border
        if col == 8:
            borders.append("border-right: 3px solid black")
            
        # Add borders to style
        if borders:
            style += "; " + "; ".join(borders)
        
        style += "}"
        self.setStyleSheet(style)
        
        # Connect signals
        self.textChanged.connect(self._on_text_changed)

    def setValidator(self, validator_func):
        super().setValidator(None)  # Clear existing validator
        self.textChanged.connect(lambda text: self._validate(text, validator_func))

    def _validate(self, text, validator_func):
        if text and not validator_func(text):
            self.setText("")
    
    def _on_text_changed(self, text):
        self.valueChanged.emit(self.row, self.col, text)
    
    def set_original(self, is_original):
        self.original = is_original
        if is_original:
            self.setStyleSheet(self.styleSheet() + """
                QLineEdit {
                    font-weight: bold;
                    color: #000080;
                    background-color: #F0F0F0;
                }
            """)
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)
            # Reset to default style
            self.setStyleSheet(self.styleSheet().split("QLineEdit {")[0] + "QLineEdit {" + 
                              self.styleSheet().split("QLineEdit {")[1].split("}")[0] + "}")
    
    def highlight_error(self, is_error):
        if is_error:
            self.setStyleSheet(self.styleSheet() + """
                QLineEdit {
                    background-color: #FFDDDD;
                }
            """)
        else:
            # Reset to default or original style
            if self.original:
                self.set_original(True)
            else:
                self.setStyleSheet(self.styleSheet().split("QLineEdit {")[0] + "QLineEdit {" + 
                                  self.styleSheet().split("QLineEdit {")[1].split("}")[0] + "}")
    
    def highlight_hint(self):
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit {
                background-color: #DDFFDD;
            }
        """)
        # Reset after 2 seconds
        QTimer.singleShot(2000, lambda: self.highlight_error(False))

class SudokuBoard(QWidget):
    cellChanged = Signal(int, int, str)
    
    def __init__(self):
        super().__init__()
        self.cells = []
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setSizeConstraint(QGridLayout.SetFixedSize)

        # Create 9x9 grid of cells
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = SudokuCell(row, col)
                cell.valueChanged.connect(self._on_cell_changed)
                layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def get_board(self):
        return [[int(cell.text()) if cell.text() else 0 
                for cell in row] for row in self.cells]

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                self.cells[i][j].setText(str(value) if value != 0 else "")
    
    def _on_cell_changed(self, row, col, value):
        self.cellChanged.emit(row, col, value)
    
    def mark_original_cells(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].text():
                    self.cells[i][j].set_original(True)
    
    def clear_original_marks(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_original(False)
    
    def highlight_conflicts(self):
        # Reset all highlights
        for i in range(9):
            for j in range(9):
                self.cells[i][j].highlight_error(False)
        
        board = self.get_board()
        
        # Check for conflicts
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    continue
                
                # Temporarily set cell to 0 to check if its value conflicts with others
                val = board[i][j]
                board[i][j] = 0
                
                # Check if placing the value back would be valid
                if not SudokuSolver.is_valid(board, i, j, val):
                    self.cells[i][j].highlight_error(True)
                
                # Restore the value
                board[i][j] = val
        
        return self._has_conflicts()
    
    def _has_conflicts(self):
        board = self.get_board()
        
        # Check rows
        for row in range(9):
            seen = set()
            for col in range(9):
                val = board[row][col]
                if val != 0:
                    if val in seen:
                        return True
                    seen.add(val)
        
        # Check columns
        for col in range(9):
            seen = set()
            for row in range(9):
                val = board[row][col]
                if val != 0:
                    if val in seen:
                        return True
                    seen.add(val)
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                seen = set()
                for i in range(3):
                    for j in range(3):
                        row, col = box_row * 3 + i, box_col * 3 + j
                        val = board[row][col]
                        if val != 0:
                            if val in seen:
                                return True
                            seen.add(val)
        
        return False
    
    def get_hint(self, solution_board):
        current_board = self.get_board()
        
        for i in range(9):
            for j in range(9):
                if current_board[i][j] == 0:
                    self.cells[i][j].setText(str(solution_board[i][j]))
                    self.cells[i][j].highlight_hint()
                    return True
        
        return False

class SudokuSolver:
    @staticmethod
    def is_valid(board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0
        return False
    
    def solve_with_copy(self, board):
        # Create a copy to avoid modifying the original
        board_copy = [row[:] for row in board]
        if self.solve(board_copy):
            return board_copy
        return None

    @staticmethod
    def find_empty(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    @staticmethod
    def generate_puzzle(difficulty):
        # Start with a solved board
        solver = SudokuSolver()
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal boxes first (these don't affect each other)
        for i in range(0, 9, 3):
            box = list(range(1, 10))
            random.shuffle(box)
            for r in range(3):
                for c in range(3):
                    board[i + r][i + c] = box.pop(0)
        
        # Solve the rest of the board
        solver.solve(board)
        
        # Create a copy of the solved board
        solution = [row[:] for row in board]
        
        # Remove numbers based on difficulty
        cells_to_remove = {
            'easy': 40,
            'medium': 50,
            'hard': 60
        }.get(difficulty, 45)
        
        # Get all positions
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions[:cells_to_remove]:
            board[i][j] = 0
        
        return board, solution
    
    @staticmethod
    def is_board_valid(board):
        # Check if the current board state is valid (may or may not be solvable)
        
        # Check rows
        for row in range(9):
            seen = set()
            for col in range(9):
                val = board[row][col]
                if val != 0:
                    if val in seen:
                        return False
                    seen.add(val)
        
        # Check columns
        for col in range(9):
            seen = set()
            for row in range(9):
                val = board[row][col]
                if val != 0:
                    if val in seen:
                        return False
                    seen.add(val)
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                seen = set()
                for i in range(3):
                    for j in range(3):
                        row, col = box_row * 3 + i, box_col * 3 + j
                        val = board[row][col]
                        if val != 0:
                            if val in seen:
                                return False
                            seen.add(val)
        
        return True

class SudokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.solver = SudokuSolver()
        self.solution = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Welcome to Sudoku Solver!")
        
        # Create difficulty selector
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        difficulty_layout.addStretch()
        
        # Create timer display
        self.timer_label = QLabel("Time: 00:00")
        self.timer_label.setAlignment(Qt.AlignRight)
        difficulty_layout.addWidget(self.timer_label)
        
        main_layout.addLayout(difficulty_layout)

        # Create Sudoku board
        self.board = SudokuBoard()
        self.board.cellChanged.connect(self.on_cell_changed)
        
        # Create board container with alignment
        board_container = QHBoxLayout()
        board_container.addStretch()
        board_container.addWidget(self.board)
        board_container.addStretch()
        main_layout.addLayout(board_container)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Create generate button
        generate_button = QPushButton("Generate Puzzle")
        generate_button.clicked.connect(self.generate_puzzle)
        button_layout.addWidget(generate_button)
        
        # Create solve button
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solve_sudoku)
        button_layout.addWidget(solve_button)
        
        # Create hint button
        hint_button = QPushButton("Hint")
        hint_button.clicked.connect(self.give_hint)
        button_layout.addWidget(hint_button)
        
        # Create validate button
        validate_button = QPushButton("Validate")
        validate_button.clicked.connect(self.validate_board)
        button_layout.addWidget(validate_button)
        
        # Create clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_board)
        button_layout.addWidget(clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Add spacer at the bottom to push everything to the top
        main_layout.addStretch(1)
        
        # Set window size
        self.setMinimumSize(400, 500)  

    def solve_sudoku(self):
        board = self.board.get_board()
        
        # Check if the board is valid before solving
        if not SudokuSolver.is_board_valid(board):
            self.statusBar.showMessage("Current board has conflicts! Please fix them first.")
            self.board.highlight_conflicts()
            return
        
        solution = self.solver.solve_with_copy(board)
        if solution:
            self.board.set_board(solution)
            self.statusBar.showMessage("Puzzle solved successfully!")
            self.timer.stop()
        else:
            self.statusBar.showMessage("No solution exists for this puzzle!")
            QMessageBox.warning(self, "No Solution", "This puzzle has no valid solution!")

    def clear_board(self):
        empty_board = [[0] * 9 for _ in range(9)]
        self.board.set_board(empty_board)
        self.board.clear_original_marks()
        self.solution = None
        self.statusBar.showMessage("Board cleared.")
        self.timer.stop()
        self.elapsed_time = 0
        self.update_timer()
    
    def generate_puzzle(self):
        difficulty = self.difficulty_combo.currentText().lower()
        board, solution = SudokuSolver.generate_puzzle(difficulty)
        self.board.set_board(board)
        self.board.mark_original_cells()
        self.solution = solution
        self.statusBar.showMessage(f"Generated a new {difficulty} puzzle. Good luck!")
        
        # Reset and start timer
        self.elapsed_time = 0
        self.timer.start(1000)  # Update every second
    
    def give_hint(self):
        if not self.solution:
            # Try to solve the current board to get a solution
            board = self.board.get_board()
            if not SudokuSolver.is_board_valid(board):
                self.statusBar.showMessage("Current board has conflicts! Please fix them first.")
                self.board.highlight_conflicts()
                return
            
            solution = self.solver.solve_with_copy(board)
            if not solution:
                self.statusBar.showMessage("No solution exists for this puzzle!")
                return
            
            self.solution = solution
        
        if self.board.get_hint(self.solution):
            self.statusBar.showMessage("Here's a hint to help you!")
        else:
            self.statusBar.showMessage("The puzzle is already complete!")
    
    def validate_board(self):
        has_conflicts = self.board.highlight_conflicts()
        if has_conflicts:
            self.statusBar.showMessage("There are conflicts in the board. Highlighted in red.")
        else:
            board = self.board.get_board()
            if SudokuSolver.find_empty(board) is None:
                self.statusBar.showMessage("Congratulations! The puzzle is solved correctly.")
                self.timer.stop()
            else:
                self.statusBar.showMessage("No conflicts found. Keep going!")
    
    def on_cell_changed(self, row, col, value):
        # Start timer if it's not running and a value was entered
        if value and not self.timer.isActive():
            self.timer.start(1000)
    
    def update_timer(self):
        if self.timer.isActive():
            self.elapsed_time += 1
        
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f"Time: {minutes:02d}:{seconds:02d}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuWindow()
    window.show()
    sys.exit(app.exec())
