import numpy as np


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.currentIndex = [0, 0]

    def isPossible(self, posx, posy, num):
        # Let us check if the number is in the column
        possible = True

        for y, row in enumerate(self.grid):
            if row[posx] == num:
                possible = False
                pass

        # Let us check if the current number is alredy in the row
        for current_number in self.grid[posy]:
            if current_number == num:
                possible = False
                pass

        # We define the x y coords of the smaller square
        sub_x = posx - (posx % 3)
        sub_y = posy - (posy % 3)

        for row in range(2):
            for col in range(2):
                if self.grid[sub_y + row][sub_x + col] == num:
                    possible = False
                pass
            pass
        pass

        return possible
        pass

    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    for attempt in range(1, 10):
                        if self.isPossible(col, row, attempt):
                            self.grid[row][col] = attempt
                            self.solve()
                            self.grid[row][col] = 0
                    return

        self.printGrid()
        pass

    def printGrid(self):
        print(np.matrix(self.grid), end='\r')
        pass
