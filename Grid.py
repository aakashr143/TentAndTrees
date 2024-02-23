from utils import *
from typing import List


class Grid:
    def __init__(self, file):
        self.rows: int = 0
        self.columns: int = 0
        self.row_constraints: List[int] = []
        self.column_constraints: List[int] = []
        self.grid: List[List[str]] = []

        self.__load_game(file)
        self.__add_grass()

    @staticmethod
    def parse_line_char(char: str) -> str:
        if char not in [".", "T"]:
            raise Exception("Invalid cell element, can only be '.' or 'T'")

        return f" {char} "

    def __load_game(self, file):
        with open(file, 'r') as file:
            lines = file.readlines()

            # Dimensions
            dimensions = lines.pop(0).split(' ')
            self.rows = int(dimensions[0])
            self.columns = int(dimensions[1])

            # Board and constraints
            for line in lines[0:-1]:
                contents = line.split(' ')

                if len(contents[0]) != self.columns:
                    raise Exception('Line length does match the specified lenght ')

                self.grid.append([self.parse_line_char(e) for e in contents[0]])
                self.row_constraints.append(int(contents[1]))

            self.column_constraints = list(map(lambda x: int(x), lines[-1].split(' ')))

        if self.rows == 0 or self.columns == 0:
            raise Exception('Unable to board dimensions')

        if len(self.grid) == 0:
            raise Exception('Unable to read grid')

        if len(self.grid) != self.rows:
            raise Exception('Number of rows in grid does not match with the number of specified')

        if len(self.grid[0]) != self.columns:
            raise Exception('Number of column in grid does not match with the number of specified')

        if self.rows != len(self.row_constraints):
            raise Exception('Number of rows is not equal to the row constaints')

        if self.columns != len(self.column_constraints):
            raise Exception('Number of columns is not equal to the columns constaints')

    def __add_grass(self):
        """
        Adds grass to empty cells with row or column constraints equal to 0 or a placement of tent is impossible at the
        location
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == EMPTY and (
                        self.row_constraints[i] == 0 or self.column_constraints[j] == 0 or [self.grid[n[0]][n[1]] for n
                                                                                            in get_neighbour_indexes(
                        self.grid, i, j, 4)].count(TREE) == 0):
                    self.grid[i][j] = GRASS
