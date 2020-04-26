# Sudoku Solver
 Real straightforward sudoku solver, using a basic baxcktracking algorithm.

 ## CMD Usage
 Run the following command
 ```
 python3 main.py path/to/board.txt
 ```
### Board.txt
The `board.txt` file is simply a text file that represents the sudoku board. It should contain 9 lines each with 9 numbers seperated by a whitespace. There should not be a whitespace at the end of the line, only a newline character.

Example from `boards/board0.txt`

```txt
0 0 3 0 2 0 6 0 0
9 0 0 3 0 5 0 0 1
0 0 1 8 0 6 4 0 0
0 0 8 1 0 2 9 0 0
7 0 0 0 0 0 0 0 8
0 0 6 7 0 8 2 0 0
0 0 2 6 0 9 5 0 0
8 0 0 2 0 3 0 0 9
0 0 5 0 1 0 3 0 0
```
# License
This project is licensed under the **GNU General Public License v3.0** which you can find in `COPYING.txt`
