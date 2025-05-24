#%%
# This is a Windows Sudoku Solver application built with PySide6

# Ensure Python uses the correct path
import os
import sys
import shutil

# Initialize Qt plugins if running as executable
def init_qt_plugins():
    try:
        # Only run this code when frozen by cx_Freeze
        if getattr(sys, 'frozen', False):
            # Get executable directory
            exec_dir = os.path.dirname(sys.executable)
            
            # Create platforms directory if it doesn't exist
            platforms_dir = os.path.join(exec_dir, "platforms")
            if not os.path.exists(platforms_dir):
                os.makedirs(platforms_dir)
                
            # Look for Qt plugins in common locations
            conda_path = os.environ.get('CONDA_PREFIX')
            if conda_path:
                # Try common locations for the plugins
                qwindows_paths = [
                    os.path.join(conda_path, "Library", "plugins", "platforms", "qwindows.dll"),
                    os.path.join(conda_path, "Lib", "site-packages", "PySide6", "plugins", "platforms", "qwindows.dll"),
                ]
                
                # Copy qwindows.dll if found
                for src_path in qwindows_paths:
                    if os.path.exists(src_path):
                        dst_path = os.path.join(platforms_dir, "qwindows.dll")
                        print(f"Copying Qt plugin from {src_path} to {dst_path}")
                        shutil.copy2(src_path, dst_path)
                        break
    except Exception as e:
        print(f"Error initializing Qt plugins: {e}")

# Call the initialization function
init_qt_plugins()

# Get the directory of this script and add it to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"Added {current_dir} to sys.path")

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                              QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout,
                              QLabel, QComboBox, QStatusBar, QMessageBox, QSizePolicy,
                              QCheckBox, QTextEdit, QInputDialog)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QRectF
from PySide6.QtGui import QFont, QColor, QPainter
import sys
import random
import time
import importlib
import puzzles

class SudokuCell(QLineEdit):
    valueChanged = Signal(int, int, str)
    
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.original = False
        self._show_candidates = False  # Initialize to False
        self.possible_numbers = set(range(1, 10))
        self.setFixedSize(40, 40)
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)
        self.setFont(QFont("Arial", 14))
        self.setValidator(lambda x: x.isdigit() and 1 <= int(x) <= 9 if x else True)
        self.textChanged.connect(self._on_text_changed)
        
        # Base style
        self.updateStyle()
    
    def updateStyle(self):
        style = """
            QLineEdit {
                font-size: 16px;
                background: white;
                border: 1px solid #cccccc;
            """
        
        # Add borders based on position
        borders = []
        if self.row == 0:
            borders.append("border-top: 3px solid black")
        elif self.row % 3 == 0:
            borders.append("border-top: 2px solid black")
            
        if self.row == 8:
            borders.append("border-bottom: 3px solid black")
            
        if self.col == 0:
            borders.append("border-left: 3px solid black")
        elif self.col % 3 == 0:
            borders.append("border-left: 2px solid black")
            
        if self.col == 8:
            borders.append("border-right: 3px solid black")
            
        if borders:
            style += "; " + "; ".join(borders)
        
        style += "}"
        self.setStyleSheet(style)

    def _on_text_changed(self, text):
        self.valueChanged.emit(self.row, self.col, text)
        self.update()  # Ensure repaint when text changes

    def paintEvent(self, event):
        super().paintEvent(event)
        
        if not self.text() and self._show_candidates and self.possible_numbers:
            painter = QPainter(self)
            painter.setFont(QFont("Arial", 8))
            painter.setPen(QColor("#808080"))
            
            cell_width = self.width() / 3
            cell_height = self.height() / 3
            
            for num in range(1, 10):
                if num in self.possible_numbers:
                    row = (num - 1) // 3
                    col = (num - 1) % 3
                    x = col * cell_width + 2
                    y = row * cell_height + cell_height - 2
                    painter.drawText(QRectF(x, y - cell_height + 4, cell_width - 2, cell_height - 2), 
                                   Qt.AlignCenter, str(num))

    def update_possibilities(self, possible_nums):
        old_possible = self.possible_numbers
        self.possible_numbers = set(possible_nums)
        if old_possible != self.possible_numbers:
            self.update()

    def set_show_candidates(self, show):
        print(f"Cell {self.row},{self.col}: Setting show_candidates to {show}")  # Debug output
        if self._show_candidates != show:
            self._show_candidates = show
            self.repaint()  # Force immediate repaint

    def setValidator(self, validator_func):
        super().setValidator(None)  # Clear existing validator
        self.textChanged.connect(lambda text: self._validate(text, validator_func))

    def _validate(self, text, validator_func):
        if text and not validator_func(text):
            self.setText("")
    
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
        self.update_all_possibilities()  # Update possibilities after setting board
    
    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].setText("")
                self.cells[i][j].set_original(False)
        self.update_all_possibilities()  # Update possibilities after clearing
    
    def _on_cell_changed(self, row, col, value):
        self.cellChanged.emit(row, col, value)
        self.update_all_possibilities()  # Update possibilities when any cell changes
    
    def mark_original_cells(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].text():
                    self.cells[i][j].set_original(True)
    
    def clear_original_marks(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_original(False)
        self.update_all_possibilities()  # Update possibilities after clearing marks
    
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
    
    def get_possible_numbers(self, row, col):
        board = self.get_board()
        if board[row][col] != 0:  # Cell already has a number
            return set()
            
        possible = set(range(1, 10))
        
        # Check row
        for j in range(9):
            if board[row][j] != 0:
                possible.discard(board[row][j])
                
        # Check column
        for i in range(9):
            if board[i][col] != 0:
                possible.discard(board[i][col])
                
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] != 0:
                    possible.discard(board[i][j])
                    
        return possible
    
    def update_all_possibilities(self):
        board = self.get_board()
        for i in range(9):
            for j in range(9):
                if not board[i][j]:  # Only update empty cells
                    possible = self.get_possible_numbers(i, j)
                    self.cells[i][j].update_possibilities(possible)

    def set_show_candidates(self, show):
        print(f"Board: Setting show_candidates to {show}")  # Debug output
        for row in self.cells:
            for cell in row:
                cell.set_show_candidates(show)
        self.update()  # Update the entire board

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
        
        # Create top controls layout
        top_controls = QHBoxLayout()
        
        # Create difficulty selector
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        top_controls.addLayout(difficulty_layout)
        
        top_controls.addStretch()
        
        # Add candidate mode checkbox
        self.candidate_checkbox = QCheckBox("Show Candidates")
        self.candidate_checkbox.setChecked(False)  # Initialize unchecked
        self.candidate_checkbox.toggled.connect(self.toggle_candidates)
        top_controls.addWidget(self.candidate_checkbox)
        
        # Create timer display
        self.timer_label = QLabel("Time: 00:00")
        self.timer_label.setAlignment(Qt.AlignRight)
        top_controls.addWidget(self.timer_label)
        
        main_layout.addLayout(top_controls)

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
        
        # Create validate button
        validate_button = QPushButton("Validate")
        validate_button.clicked.connect(self.validate_board)
        button_layout.addWidget(validate_button)
        
        # Create clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_board)
        button_layout.addWidget(clear_button)

        # Create import button
        import_button = QPushButton("Import Puzzle")
        import_button.clicked.connect(self.import_puzzle)
        button_layout.addWidget(import_button)
        
        main_layout.addLayout(button_layout)
        
        # Create output text box
        self.output_text = QTextEdit()
        self.output_text.setFixedHeight(175)  # About 1.75 inches
        self.output_text.setReadOnly(True)  # Make it read-only
        main_layout.addWidget(self.output_text)
        
        # Set window size
        self.setMinimumSize(400, 700)  

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
        self.clear_board()  # Clear the board first
        difficulty = self.difficulty_combo.currentText().lower()
        board, solution = SudokuSolver.generate_puzzle(difficulty)
        self.board.set_board(board)
        self.board.mark_original_cells()
        self.solution = solution
        self.board.update_all_possibilities()  # Ensure possibilities are updated after generating
        self.statusBar.showMessage(f"Generated a new {difficulty} puzzle. Good luck!")
        
        # Reset and start timer
        self.elapsed_time = 0
        self.timer.start(1000)  # Update every second
    
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
    
    def toggle_candidates(self, checked):  
        print(f"Window: Toggle candidates to {checked}")  # Debug output
        self.board.set_show_candidates(checked)
        if checked:
            self.board.update_all_possibilities()
        self.board.repaint()  # Force immediate repaint of the entire board
    
    def update_timer(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f"Time: {minutes:02d}:{seconds:02d}")

    def import_puzzle(self):
        # Get puzzle name from user
        puzzle_name, ok = QInputDialog.getText(self, "Import Puzzle", 
            "Enter puzzle name (e.g., sudoku0, sudoku1):\nAvailable in puzzles.py")
        
        if ok and puzzle_name:
            try:
                # Reload the puzzles module to get any updates
                importlib.reload(puzzles)
                # Get the puzzle array from the module
                puzzle = getattr(puzzles, puzzle_name)
                # Set the board
                self.board.set_board(puzzle)
                self.board.mark_original_cells()
                self.output_text.setText(f"Successfully imported puzzle '{puzzle_name}'")
            except AttributeError:
                self.output_text.setText(f"Error: Puzzle '{puzzle_name}' not found in puzzles.py")
            except Exception as e:
                self.output_text.setText(f"Error importing puzzle: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuWindow()
    window.show()
    sys.exit(app.exec())
