import copy
from itertools import combinations
from utils import *
from typing import List


class Solver1:
    """
       Loops through all possible tent placements in a row
       Not used in the report, slower compared to Solver2 and Solver3
    """

    def __init__(self, grid: List[List[str]], row_constraints: List[int], column_constraints: List[int]):
        self.grid = copy.deepcopy(grid)
        self.row_constraints = row_constraints
        self.column_constraints = column_constraints

        self.is_solved = False
        self.__solve(self.grid)

    def get_tent_placement_options(self, grid, row_idx):
        if self.row_constraints[row_idx] == 0:
            return []

        options = list(
            combinations([i for i, cell in enumerate(grid[row_idx]) if cell == EMPTY], self.row_constraints[row_idx]))

        if self.row_constraints[row_idx] == 1:
            return options

        x = []
        for t in options:
            # Check if any two elements in the tuple have a difference of 1
            if not any(abs(t[i] - t[j]) == 1 for i in range(len(t)) for j in range(i + 1, len(t))):
                x.append(t)

        return x

    def __solve(self, grid: List[List[str]], row_idx: int = 0):
        if self.is_solved:
            return

        if row_idx == len(self.grid):
            if check_grid(grid, self.row_constraints, self.column_constraints):
                display_grid(grid, self.row_constraints, self.column_constraints)
                self.is_solved = True
            return

        # Skip row if no tents are allowed
        if self.row_constraints[row_idx] == 0:
            self.__solve(grid, row_idx + 1)
            return

        # All possible placement of tress in the row
        for i, placement in enumerate(self.get_tent_placement_options(grid, row_idx)):
            g = copy.deepcopy(grid)
            for x, col_idx in enumerate(placement):
                if is_valid_tent_placement(grid, self.row_constraints, self.column_constraints, row_idx, col_idx):
                    g[row_idx][col_idx] = TENT
                else:
                    break

                # Go to next row, if all the placement of the tent are done in the row
                if x == self.row_constraints[row_idx] - 1:
                    self.__solve(g, row_idx + 1)


class Solver2:
    """
        Loops through all possible tent placements for a tree
    """

    def __init__(self, grid: List[List[str]], row_constraints: List[int], column_constraints: List[int]):
        self.grid = copy.deepcopy(grid)
        self.row_constraints = row_constraints
        self.column_constraints = column_constraints

        self.is_solved = False
        self.tree_locations = []

        for i, row in enumerate(self.grid):
            self.tree_locations += [[i, j] for j, cell in enumerate(row) if cell == TREE]

        self.__solve(self.grid)

    def __solve(self, grid: List[List[str]], tree_idx=0):
        if self.is_solved:
            return

        if tree_idx == len(self.tree_locations):
            if check_grid(grid, self.row_constraints, self.column_constraints):
                self.is_solved = True
                display_grid(grid, self.row_constraints, self.column_constraints)
            return

        [x, y] = self.tree_locations[tree_idx]

        for i, j in [n for n in get_neighbour_indexes(grid, x, y, 4) if
                     is_valid_tent_placement(grid, self.row_constraints, self.column_constraints, n[0], n[1])]:
            g = copy.deepcopy(grid)
            g[i][j] = TENT
            self.__solve(g, tree_idx + 1)


class Solver3:
    """
        Loops through all possible tent placements for a tree
        Reduces domain for the remaining trees
        Not used in the report, slower compared to Solver2
    """

    def __init__(self, grid: List[List[str]], row_constraints: List[int], column_constraints: List[int]):
        self.grid = copy.deepcopy(grid)
        self.row_constraints = row_constraints
        self.column_constraints = column_constraints

        self.is_solved = False
        self.tree_domain: List[List[List[int]]] = []

        # Get all the possible location of tents
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == TREE:
                    self.tree_domain += [[n for n in get_neighbour_indexes(grid, i, j, 4) if
                                          is_valid_tent_placement(grid, self.row_constraints, self.column_constraints,
                                                                  n[0], n[1])]]

        self.__solve(self.grid, self.tree_domain)

    def __reduce_tree_domain(self, grid, tree_domain: List[List[List[int]]]):
        reduced_domain = []
        for domain in tree_domain:
            reduced_domain += [[n for n in domain if
                                is_valid_tent_placement(grid, self.row_constraints, self.column_constraints, n[0],
                                                        n[1])]]

        return reduced_domain

    def __solve(self, grid: List[List[str]], tree_domain: List[List[List[int]]]):
        if self.is_solved:
            return

        if len(tree_domain) == 0:
            if check_grid(grid, self.row_constraints, self.column_constraints):
                self.is_solved = True
                display_grid(grid, self.row_constraints, self.column_constraints)
            return

        for n in tree_domain[0]:
            g = copy.deepcopy(grid)
            g[n[0]][n[1]] = TENT
            reduced_domain = self.__reduce_tree_domain(g, tree_domain[1:])
            if any(len(d) == 0 for d in reduced_domain):
                continue

            self.__solve(g, reduced_domain)
