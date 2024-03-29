import time

from Grid import Grid
from Minizinc import Minizinc
from Solver import Solver1, Solver2, Solver3, Solver4


grid = Grid('games/8x8/game5.txt')

m = Minizinc(grid)
m.convert()
s1 = time.time()
m.solve()
print(time.time() - s1)

s1 = time.time()
Solver1(grid.grid, grid.row_constraints, grid.column_constraints)
print(time.time() - s1)

s1 = time.time()
Solver2(grid.grid, grid.row_constraints, grid.column_constraints)
print(time.time() - s1)

s1 = time.time()
Solver3(grid.grid, grid.row_constraints, grid.column_constraints)
print(time.time() - s1)

s1 = time.time()
Solver4(grid.grid, grid.row_constraints, grid.column_constraints)
print(time.time() - s1)