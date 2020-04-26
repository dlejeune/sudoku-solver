import solver
import sys
import boardGui

if __name__ == '__main__':
    filename = None
    sudoku_board = []

    if sys.argv[1] != "-g":
        filename = sys.argv[1]

        with open(filename, mode='r') as board_file:
            for col in board_file:
                # Remove whitespace from end of line and seperate numbers
                col_rows = col.strip().split(" ")

                # Transform strings to int
                col_rows = [int(x) for x in col_rows]

                # Add the current row to the board
                sudoku_board.append(col_rows)
                pass
            pass

        solve = solver.Solver(sudoku_board)

        solve.solve()
    else:
        gui = boardGui.BoardGui()
