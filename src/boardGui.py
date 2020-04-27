import sys
from functools import partial
from src.solver import Solver

from time import perf_counter


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialog


from PyQt5.QtCore import Qt


class HelpDialog(QDialog):

    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 750, 750)
        help_body = QLabel("", parent=self)
        help_text = """
                <h1>Okay so you need help</h1>
        This is literally the simplest programme ever. The steps are as follows:<br/><br/>

        <ol>
        <li>Make sure the board is clear</li>
        <li>Load a board (two ways of doing this)</li>
        <li>Make the machine do all the hard work</li>
        </ol>
        <br/><br/>

        <h2>Clearing the board</h2>
        You can go and delete all the values one-by-one. Or you can click the <code>Clear</code> button and let the computer do it for you.
        <br/><br/>

        <h2>Loading a board</h2>
        <h4>Manually</h4>
        Input each number of the sudoku puzzle by hand. As you type a number, the cursor will automaticqlly move forward to the next slot. You can press <kbd>Shit + Tab</kbd> to go back a cell.

        <h4>With a text file</h4>
        You can also load a board from a text file, by pressing the <code>Load</code> button. The file is simply a text file that represents the sudoku board. It should contain 9 lines each with 9 numbers seperated by a whitespace. There should not be a whitespace at the end of the line, only a newline character.<br/>

        Example:

        <pre>
        0 0 3 0 2 0 6 0 0
        9 0 0 3 0 5 0 0 1
        0 0 1 8 0 6 4 0 0
        0 0 8 1 0 2 9 0 0
        7 0 0 0 0 0 0 0 8
        0 0 6 7 0 8 2 0 0
        0 0 2 6 0 9 5 0 0
        8 0 0 2 0 3 0 0 9
        0 0 5 0 1 0 3 0 0
        </pre>

        <h4>Input Notes</h4>
        Please make sure you only enter numeric values in the text file. I've been too lazy to code any input sanitization. <br/>

        When inputting manually, if you leave a cell blank or input a letter, it'll just be read as a zero.

        <h2>Make the machine do the work</h2>
        Literally just press the solve button. Note the technique used is extremely rough, so it could take anywhere from a few milliseconds to whole minutes. Also, it could be that your computer is trash.
        """
        help_body.setText(help_text)
        help_body.setWordWrap(True)


class BoardGui(QMainWindow):

    def __init__(self):
        super().__init__()

        # Where the user's cursor is at: row, col
        self.currentCursPos = [0, 0]

        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(700, 650)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createHeaderBox()
        self._createInputs()
        self.helpModal = HelpDialog()
        pass

    def _createHeaderBox(self):
        self.headerPanelLayout = QGridLayout()
        titleMessage = QLabel('<h1>Sudoku Solver</h1>')
        infoMessasge = QLabel('<p>Hello, and welcome to this app which will actually be the death of me. Load in a board (txt file - see the help button below) or type one in (it\'s more fun than you think). The click solve. DON\'T CLICK SOLVE ON AN EMPTY BOARD.</p>')
        infoMessasge.setWordWrap(True)
        self.timeMessage = QLabel("")

        self.solveButton = QPushButton("Solve")
        self.solveButton.setFixedSize(70, 30)

        self.solveButton.setStyleSheet("QPushButton {background-color: #5cb85c; color: white }")

        self.loadButton = QPushButton("Load")
        self.loadButton.setFixedSize(70, 30)

        self.clearButton = QPushButton("Clear")
        self.clearButton.setFixedSize(70, 30)

        self.helpButton = QPushButton("Help")
        self.helpButton.setFixedSize(70, 30)

        self.headerPanelLayout.addWidget(titleMessage, 0, 0, 1, 2)
        self.headerPanelLayout.addWidget(infoMessasge, 1, 0, 2, 4)
        self.headerPanelLayout.addWidget(self.timeMessage, 0, 1, 1, 2)
        self.headerPanelLayout.addWidget(self.solveButton, 2, 3, 1, 1)
        self.headerPanelLayout.addWidget(self.loadButton, 2, 1, 1, 1)
        self.headerPanelLayout.addWidget(self.clearButton, 2, 0, 1, 1)
        self.headerPanelLayout.addWidget(self.helpButton, 2, 2, 1, 1)

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
        t1_start = perf_counter()

        self.solver.solve()
        t1_stop = perf_counter()
        execTime = t1_stop - t1_start
        print(self.solver.getGrid())
        print(self.solver.counter)

        self.populateUi(self.solver.getGrid())
        execTime = 'Solved in {:f} seconds'.format(execTime)
        self._view.timeMessage.setText(execTime)

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
        newx = x + 1
        newy = y

        if newx > 8:
            newx = 0
            newy += 1
            pass

        if newy > 8:
            newy = 0
            pass

        self._view.inputs[newy][newx].setFocus()
        pass

    def clear(self):
        for row in range(9):
            for col in range(9):
                self._view.inputs[row][col].clear()
                pass
            pass

    def showHelp(self):

        self._view.helpModal.show()
        pass

    def _connectSignals(self):
        self._view.solveButton.clicked.connect(partial(self.solve))
        self._view.loadButton.clicked.connect(partial(self.loadFromFile))

        self._view.clearButton.clicked.connect(partial(self.clear))
        self._view.helpButton.clicked.connect(partial(self.showHelp))

        for row in range(9):
            for col in range(9):
                self._view.inputs[row][col].textChanged.connect(partial(self.moveCursor, col, row))


def main():
    sudoku_solver = QApplication([])
    solving_machine = Solver()

    view = BoardGui()
    view.show()
    BoardController(view=view, solver=solving_machine)

    sys.exit(sudoku_solver.exec_())


if __name__ == '__main__':
    main()
