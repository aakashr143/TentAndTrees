# Tent And Trees

## Installation

The solvers uses Python and MiniZinc to work properly, and of course this repository. Steps 2 and 3 are only required if you wish to use the MiniZinc Solver
1. Install [Python](https://www.python.org/downloads/), the solver was written in V3.11.1, so any version higher than that should work.
2. Install [MiniZinc](https://www.minizinc.org/software.html)
3. Setup the Minizinc CLI `PATH` enviroment variable, follow the steps here from this [link](https://www.minizinc.org/doc-2.5.5/en/installation.html#ch-installation)
4. Download this repository in your favourate editor and run main.py

## Structure
- Games: containts some sample puzzles
- Grid.py: responsible for reading and validating the puzzles for the solvers
- Minizinc.py: generates a `.mzn` file and uses the MiniZinc CLI to solve the puzzle
- Solver.py: python solver
- utils.py: helper functions and constants

## Puzzle Format
The puzzles are provided to the solvers in a `.txt` file and must follow the following format.
```
<num row> <num columns>
// use 'T' to represent a tree cell on the board
// use '.' to represent an empty cell on the board
...T.. <row constraint>
TT.... <row constraint>
...T.. <row constraint>
<column constraint> <column constraint> <column constraint>
```
