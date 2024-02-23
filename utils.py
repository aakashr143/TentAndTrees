from typing import List

# Constants
TREE = ' T '
TENT = ' A '
GRASS = ' * '
EMPTY = ' . '


def display_grid(grid: List[List[str]], row_constraints: List[int], column_constraints: List[int]):
    print(f'  |{"".join([f" {e} " for e in column_constraints])}')
    print(f'  -{" - " * len(column_constraints)}')
    for i, row in enumerate(grid):
        print(f'{row_constraints[i]} | {"".join(row)}')


def get_neighbour_indexes(grid: List[List[str]], row_idx: int, col_idx: int, n: int):
    """
        gets neighbouring indexes for a given index, n=4 for trees and n=8 for tents
    """
    rows = len(grid)
    columns = len(grid[0])

    if row_idx >= rows or col_idx >= columns:
        return []

    if n != 4 and n != 8:
        raise Exception('n can only be 4 or 8')

    idxs = []

    if n == 4:
        for i in range(row_idx - 1, row_idx + 2):
            for j in range(col_idx - 1, col_idx + 2):
                if (0 <= i < rows) and (0 <= j < columns) and not (i == row_idx and j == col_idx) and (
                        i == row_idx or j == col_idx):
                    idxs.append([i, j])
        return idxs

    if n == 8:
        for i in range(row_idx - 1, row_idx + 2):
            for j in range(col_idx - 1, col_idx + 2):
                if (0 <= i < rows) and (0 <= j < columns) and not (i == row_idx and j == col_idx):
                    idxs.append([i, j])

    return idxs


def is_valid_tent_placement(grid: List[List[str]], row_constraints: List[int], column_constraints: List[int], row_idx: int, col_idx: int):
    # Index are in range
    if row_idx >= len(grid) or row_idx < 0 or col_idx >= len(grid[0]) or col_idx < 0:
        return False

    # Cell is empty
    if grid[row_idx][col_idx] != EMPTY:
        return False

    # Doesnt violate row constraints
    if grid[row_idx].count(TENT) >= row_constraints[row_idx]:
        return False

    # Doesnt violate column constraints
    if [row[col_idx] for row in grid].count(TENT) >= column_constraints[col_idx]:
        return False

    # No neighbouring tent
    for n in get_neighbour_indexes(grid, row_idx, col_idx, 8):
        if grid[n[0]][n[1]] == TENT:
            return False

    return True


def check_grid(grid: List[List[str]], row_constraints: List[int], column_constraints: List[int]):
    # Number of tents and tress should be equal
    if sum([row.count(TREE) for row in grid]) != sum([row.count(TENT) for row in grid]):
        return False

    # Row constraints check
    if False in [row.count(TENT) == row_constraints[i] for i, row in enumerate(grid)]:
        return False

    # Column constraints check
    for i in range(len(grid[0])):
        if [row[i] for row in grid].count(TENT) != column_constraints[i]:
            return False

    # Later for checking the 1-to-1 relation of tent and trees
    tree_locations = {}

    # Each Tree should have a tent and Each tent should not be a neighbour of another tent
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == TREE:
                # Tree has a tent adjecent to it
                if [grid[n[0]][n[1]] for n in get_neighbour_indexes(grid, i, j, 4)].count(TENT) == 0:
                    return False

                tree_locations[f'{i},{j}'] = []
                for x, y in get_neighbour_indexes(grid, i, j, 4):
                    if grid[x][y] == TENT:
                        tree_locations[f'{i},{j}'].append(f'{x},{y}')

            if cell == TENT:
                # Tent doesn't have another tent adjecent to it
                if [grid[n[0]][n[1]] for n in get_neighbour_indexes(grid, i, j, 8)].count(TENT) > 0:
                    return False
                # Tent has a tree adjecent to it
                if [grid[n[0]][n[1]] for n in get_neighbour_indexes(grid, i, j, 4)].count(TREE) == 0:
                    return False

    # Each tree has a should have an assigned tent
    for tree1, v1 in tree_locations.items():
        # Only one tent near a tree, no need to check futher
        # This tent is assigned to this tree
        if len(v1) == 1:
            continue

        # Is a tree has multiple tents near it,
        # One of the tent, should also be near some other tree
        # Only then this tree can have a tent assigned to it
        is_present = False
        for tree2, v2 in tree_locations.items():
            # Same tree, skip
            if tree1 == tree2:
                continue

            # Check is tent is near some other tree
            for v in v1:
                if v in v2:
                    is_present = True

        # If none of the tents near this tree are present near some other tree
        # 1-to-1 relation not satisfied
        if not is_present:
            return False

    return True
