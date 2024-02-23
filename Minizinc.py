import os

from Grid import Grid
from utils import TREE, GRASS

constraints = f'''

% row sum
constraint forall(i in 1..r) (
  sum([
      if grid[i,j] = tent then 1 else 0 endif | j in 1..c
  ]) = rowConstraints[i]
);

% colum sum 
constraint forall(i in 1..c) (
  sum([
      if grid[j,i] = tent then 1 else 0 endif | j in 1..r
  ]) = columnConstraints[i]
);


% There is no tent next to a tent
constraint forall(i in 1..r, j in 1..c) (
    if grid[i,j] = tent then
      sum([
        if grid[i+dx, j+dy] = tent /\ not(dx = 0 /\ dy = 0) /\ i+dx >= 1 /\ i+dx <= r /\ j+dy >= 1 /\ j+dy <= c then 1 else 0 endif | dx in -1..1, dy in -1..1
      ]) = 0
    endif
);

% There is a tree next to a tent
constraint forall(i in 1..r, j in 1..c) (
    if grid[i,j] = tent then
          sum([
              grid[i+dx, j+dy] = tree /\ abs(dx) + abs(dy) = 1 /\ not(dx = 0 /\ dy = 0) /\ i+dx >= 1 /\ i+dx <= r /\ j+dy >= 1 /\ j+dy <= c | dx in -1..1, dy in -1..1
          ]) >= 1
  endif
);

% There is a tent next to a tree
constraint forall(i in 1..r, j in 1..c) (
    if grid[i,j] = tree then
          sum([
              grid[i+dx, j+dy] = tent /\ abs(dx) + abs(dy) = 1 /\ not(dx = 0 /\ dy = 0) /\ i+dx >= 1 /\ i+dx <= r /\ j+dy >= 1 /\ j+dy <= c | dx in -1..1, dy in -1..1
          ]) >= 1
  endif
);

function var int: findCost() = 
  sum([ 
    sum([
      if grid[i,j] = tree then
        sum([
          if i+dx >= 1 /\ i+dx <= r /\ j+dy >= 1 /\ j+dy <= c /\ 
             grid[i+dx, j+dy] = tent /\ abs(dx) + abs(dy) = 1 /\ not(dx = 0 /\ dy = 0) 
          then 1 else 0 endif
        | dx in -1..1, dy in -1..1])
      else 0 endif
    | j in 1..c])
  | i in 1..r])
;

var int: cost = findCost();

%solve satisfy;
solve minimize cost;
    
output 
[
 if j = 1 then "\\n" else " " endif ++
   if fix(grid[i,j]) = tree then " T " elseif fix(grid[i,j]) = tent then " A " else " . " endif
| i in 1..r, j in 1..r
];
%output["\\ncost=\(cost)"];

'''


class Minizinc:
    def __init__(self, grid: Grid):
        self.grid = grid

    def solve(self):
        os.system("minizinc --solver Gecode minizinc.mzn")

    def convert(self, file_name='minizinc.mzn'):
        if ".mzn" not in file_name:
            raise Exception("Filename must contain the ext .mzn")

        with open(file_name, 'w') as f:
            f.write(f'include "globals.mzn";\n')
            f.write(f'int: r = {self.grid.rows};\n')
            f.write(f'int: c = {self.grid.columns};\n\n')
            f.write(f'int: empty = 0;\n')
            f.write(f'int: tree = 1;\n')
            f.write(f'int: tent = 2;\n')
            f.write(f'int: grass = 3;\n\n')
            f.write(f'array[1..r,1..c] of var 0..3: grid;\n\n')
            f.write(
                f'array[1..r] of int: rowConstraints = [{", ".join([f"{c}" for c in self.grid.row_constraints])}];\n')
            f.write(
                f'array[1..c] of int: columnConstraints = [{", ".join([f"{c}" for c in self.grid.column_constraints])}];\n\n')

            tree_count = 0
            grass_count = 0
            for i in range(len(self.grid.grid)):
                for j in range(len(self.grid.grid[i])):
                    if self.grid.grid[i][j] == TREE:
                        tree_count += 1
                        f.write(f'constraint grid[{i + 1},{j + 1}] = tree;\n')
                    if self.grid.grid[i][j] == GRASS:
                        grass_count += 1
                        f.write(f'constraint grid[{i + 1},{j + 1}] = grass;\n')

            f.write(f'\n')
            f.write(f'constraint sum([\n')
            f.write(f'  if grid[i,j] = grass then 1 else 0 endif | i in 1..r, j in 1..c\n')
            f.write(f']) = {grass_count};\n\n')

            f.write(f'\n')
            f.write(f'constraint sum([\n')
            f.write(f'  if grid[i,j] = tent then 1 else 0 endif | i in 1..r, j in 1..c\n')
            f.write(f']) = {tree_count};\n\n')

            f.write(f'constraint sum([\n')
            f.write(f'  if grid[i,j] = tree then 1 else 0 endif | i in 1..r, j in 1..c\n')
            f.write(f']) = {tree_count};\n\n')

            f.write(f'{constraints}')
