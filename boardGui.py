import sys
from functools import partial
import solver

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt


class BoardGui(QMainWindow):

    def __init__(self):
        super().__init__()

        # Where the user's cursor is at: row, col
        self.currentCursPos = [0, 0]

        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(650, 300, 650, 600)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createHeaderBox()
        self._createInputs()
        pass

    def _createHeaderBox(self):
        self.headerPanelLayout = QGridLayout()
        titleMessage = QLabel('<h1>Sudoku Solver</h1>')
        infoMessasge = QLabel('<p>Hello, and welcome to this app which will actually be the death of me</p>')

        timeMessage = QLabel("")

        self.solveButton = QPushButton("Solve")
        self.solveButton.setFixedSize(70, 30)
        self.loadButton = QPushButton("Load")
        self.loadButton.setFixedSize(70, 30)

        self.headerPanelLayout.addWidget(titleMessage, 0, 0)
        self.headerPanelLayout.addWidget(infoMessasge, 1, 0)
        self.headerPanelLayout.addWidget(timeMessage, 0, 2)
        self.headerPanelLayout.addWidget(self.solveButton, 1, 1)
        self.headerPanelLayout.addWidget(self.loadButton, 1, 2)

        self.generalLayout.addLayout(self.headerPanelLayout)

    def _createInputs(self):
        self.inputs = []
        self.inputLayout = QGridLayout()

        for y in range(9):
            tempRow = []
            for x in range(9):

                # Create the edit box
                currentEdit = QLineEdit()

                # Do some parameter stuff
                currentEdit.setMaximumWidth(45)
                currentEdit.setMinimumWidth(45)
                currentEdit.setMaximumHeight(45)
                currentEdit.setMinimumHeight(45)
                currentEdit.setMaxLength(1)
                currentEdit.setAlignment(Qt.AlignCenter)

                font = currentEdit.font()
                font.setPointSize(38)
                currentEdit.setFont(font)

                self.inputLayout.addWidget(currentEdit, y, x)
                tempRow.append(currentEdit)
                pass

            self.inputs.append(tempRow)
            pass

        self.generalLayout.addLayout(self.inputLayout)

        pass


class BoardController():

    def __init__(self, view, solver):
        self._view = view
        self.solver = solver

        self._connectSignals()

    def cleanData(self):
        grid = []
        for row in range(9):
            grid_row = []
            for col in range(9):
                cell = self._view.inputs[row][col]
                sanitized_value = 0
                try:
                    sanitized_value = int(cell.text())
                    pass
                except ValueError:
                    print("Found a character or an empty space. Substituting with 0")

                grid_row.append(sanitized_value)
                pass
            grid.append(grid_row)
            pass
        return grid

    def solve(self):
        cleanedGrid = self.cleanData()
        self.solver.setGrid(cleanedGrid)
        self.solver.solve()
        print(self.solver.getGrid())
        print(self.solver.solvedGrid)
        self.populateUi(self.solver.getGrid())

    def populateUi(self, grid):
        for row in range(9):
            for col in range(9):
                self._view.inputs[row][col].setText(str(grid[row][col]))
                pass
            pass
        pass

    def loadFromFile(self):
        filename = QFileDialog.getOpenFileName(self._view, "Select File", "./", "Text Files (*.txt)")
        grid = []
        with open(filename[0], mode='r') as board_file:
            for col in board_file:
                # Remove whitespace from end of line and seperate numbers
                col_rows = col.strip().split(" ")

                # Transform strings to int
                col_rows = [int(x) for x in col_rows]

                # Add the current row to the board
                grid.append(col_rows)
                pass
            pass
        self.populateUi(grid)
        pass

    def moveCursor(self, x, y):

        pass

    def _connectSignals(self):
        self._view.solveButton.clicked.connect(partial(self.solve))
        self._view.loadButton.clicked.connect(partial(self.loadFromFile))

        for row in range(9):
            for col in range(9):
                self._view.inputs[row][col].textChanged.connect(partial(self.moveCursor, col, row))


def main():
    sudoku_solver = QApplication([])
    solving_machine = solver.Solver()

    view = BoardGui()
    view.show()
    BoardController(view=view, solver=solving_machine)

    sys.exit(sudoku_solver.exec_())


if __name__ != '__main__':
    main()
