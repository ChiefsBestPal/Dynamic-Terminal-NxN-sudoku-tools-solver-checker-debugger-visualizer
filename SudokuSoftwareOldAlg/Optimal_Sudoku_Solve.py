import numpy as np
import itertools as it
import time
import os,sys
from UtilitiesSudoku import *
# from Backtrack_Animation_and_interface_print import * #TODO Original animation (simpler and faster)
from ConsoleSudokuVisualizerFirstFullFeatures import *
import itertools as it
#TEST_DISPLAY = display
TEST_DISPLAY = printSolveAnimationCycle
IS_GRID_VERSION = True
isOneTimeOutOfTwo = True
speed = 0.00 # !!!!!!!!!!float(input('Enter Animation Speed in seconds\t'))
puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8], 
		  [0, 8, 0, 0, 9, 0, 0, 3, 0], 
		  [2, 0, 0, 0, 0, 5, 4, 0, 0], 
		  [4, 0, 0, 0, 0, 1, 8, 0, 0], 
		  [0, 3, 0, 0, 7, 0, 0, 4, 0], 
		  [0, 0, 7, 9, 0, 0, 0, 0, 3], 
		  [0, 0, 8, 4, 0, 0, 0, 0, 6], 
		  [0, 2, 0, 0, 5, 0, 0, 8, 0], 
		  [1, 0, 0, 0, 0, 2, 5, 0, 0]]


#Each cells has 3 units (Column, Row, Box) and so 20 peers (all unique cells in from all units )
#So 9 cells per unit and cells that share a unit are peers
#! See UTILITIES FOR ALL CONSTANTS (UNITLIST,SQUARES,PEERS,LIST)

def cellsDictToGrid(temp_values_dict): #TODO NEW : D
	global N
	chunks = [temp_values_dict.items()] * N
	g = [next(iter(dict(filter(None, v)).items()))[1] for v in it.zip_longest(*chunks)]
	g2 = (g[i:i + N] for i in range(0, len(g), N))
	return list(g2)

def grid_values(grid):
	"Convert grid into a dict of {square: char} with '0' or '.' for empties."
	grid = list(map(str,np.array(grid).flatten()))
	chars = [c for c in grid if c in digits or c in '0.']
	print(len(chars))
	print(grid)
	assert len(chars) == N*N
	return dict(zip(squares, chars))

def parse_grid(grid):
	"""Convert grid to a dict of possible values, {square: digits}, or
	return False if a contradiction is detected."""
	## To start, every square can be any digit; then assign values from the grid.
	values = dict((s, digits) for s in squares) #initially, we are treating 9 poss/empty cell
	for s,d in grid_values(grid).items():
		if d in digits and not assign(values, s, d): #if single possibility and cant assign it:
			return False ## (Fail if we can't assign d to square s.)

	TEST_DISPLAY(cellsDictToGrid(values),speed,isAnimated=False)
	return values

#! Basic Strats (Constraint satisfaction;consistency, Constraint propagation,backtracking): 
#* I. If cell has 1 possible value, then remove this value from the cell's peers 
# --> If A1 is assigned value, 20 peers lose that possible value
#* II. corrolary following I.: If unit has 1 only possibility (out of9) for a value, place value there
# --> If all cells apart A2 in row (unit) lack a certain possible value, A2 is assigned that certain value 
#* III. Complimentary of I. and II. will change peers of peers, use: Notation, update possibilities and backtracking
# --> https://en.wikipedia.org/wiki/Local_consistency#Constraint_propagation_for_arc_and_path_consistency

#*Logic here will state that we ought to favor elimination over assignment
#?values = dictionnary that incorporates all possible values of each cell as such: {cell: 'possibilities'}
#?So, values[s] is possibilities for cell s and d is the single digit that is or not in values[s]
stored_final_grid = None
first_time = 0
def assign(values, s, d):
	"""Eliminate all the other values (except d) from values[s] and propagate.
	Return values, except return False if a contradiction is detected."""
	global isOneTimeOutOfTwo,stored_final_grid,first_time
	other_values = values[s].replace(d, '')


	temp = values.copy()#deepcopy()


	if first_time != 0:
		for k,v in temp.items():
			if len(v.replace(' ','')) != 1:
				temp[k] = '*'
		if IS_GRID_VERSION: #TODO new : D
			temp = cellsDictToGrid(temp)
			stored_final_grid = temp
		if isOneTimeOutOfTwo:
			TEST_DISPLAY(temp,speed,True)#,end='',flush=True
			isOneTimeOutOfTwo = False
		else:
			isOneTimeOutOfTwo = True

	first_time += 1
	del temp


	if all(eliminate(values, s, d2) for d2 in other_values): #Eliminate all d2s and propagate;
		return values
	else:#1+ empty string or eliminate as produced a false bool = Impossibility = Error;
		return False

def eliminate(values, s, d): #intially treat values[s], but it might affect values var as param
	"""Eliminate d from values[s]; propagate when values or places <= 2.
	Return values, except return False if a contradiction is detected."""

	if d not in values[s]:
		return values ## Already eliminated

	values[s] = values[s].replace(d,'')

	#? (I.) If d2 is the only possible value for reduced s, remove d2 from peers[s] (all 20 peers of s lose d2 as poss value)
	if len(values[s]) == 0:
		return False ## Contradiction: removed last value,

	elif len(values[s]) == 1:
		last_value = values[s]
		if not all(eliminate(values, peer, last_value) for peer in peers[s]):
			#*peer=s',eliminate last_value from values[peer] and do propagate effects
			
			return False #like in assign function
		del last_value#*

	#? (II.) If a unit u is reduced to only one place for a value d, then put it there.
	for u in units[s]:# iterates [9 row el],[9 col el] and [9 box el] (3 iterations)
		dplaces = [s for s in u if d in values[s]] #list of all cells that have digit as a possibility
		if len(dplaces) == 0:
			return False ## Contradiction: no place for this value
		elif len(dplaces) == 1:
		# d can only be in one place in unit; assign it there
			if not assign(values, dplaces[0], d): #!second recursion
				return False #assign() contradiction
		del dplaces#*

	return values


#* Search algorithm: depth-first search (+ backtracking due to constraint propagation) 

#? --> (recursive, consider all poss for values[s] before next s) #? s stands for current cell
#backtracking search (alternative): keep track of each change to values and undo the change when we hit a dead end
# ---> we use .copy() for previous possibilities that will possibly need correction

#* Depth-first variable ordering (which cell is tested first ?): minimum remaining values heuristic (less poss = cell goes first)
# Depth-first value ordering (which digit for cell tested first ?): Not important: '123456789' in .json


#* Steps of this optimization search algorithm:
# 1. Check for solution or contradiction, afterward choose empty cell and consider all possibilities for it (start of constraint propagation)
# 2. Test each possible values of d for cell s
# 3. Try and keep value of d if it allows for further search nearing the solution
# 4. For each failed d for cell s, recursion allows to drop to another d and test it.


def isIn(seq):
	""" Returns first non null element in sequence """
	for el in seq:
		if el:
			return el
	return False #all elements are null in sequence

def depth_first_search(values):
	"Using depth-first search and propagation, try all possible values."
	if values is False:
		return False ## Failed earlier due to contradiction or other prompts of error against proper grid placement

	if all(len(values[s]) == 1 for s in squares): #if all N**2 (9**2) cells have a single possibility
		return values ##* Solved!

	## Choose empty cell with least possibility #*(minimum remaining values)
	n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1) 
	#non empty cells = all cells with not one possibility, min applies to tup[0]
	#!print('Minimum remaining values for chosen cell:  ',n,' ###Cell: ',s,end='\n')

	return isIn(depth_first_search(assign(values.copy(), s, d)) for d in values[s])#!Important line
	#* isIn is all nul, than values is False will become true and generate failure
	#*Otherwise, line recursively checks possible d for s 
	#*shallow copy ofstring is memory efficient, and it serves as previous version of values dict: {cell: possible digits}
	# --> for possible backtrack

#!------------------------------------------
#SOLVE:
def solve(grid): return TEST_DISPLAY(depth_first_search(parse_grid(grid)),speed,True)



def solve_all(grids, name='', showif=0.0):
	"""Attempt to solve a sequence of grids. Report results.
	When showif is a number of seconds, display puzzles that take longer.
	When showif is None, don't display any puzzles."""
	def time_solve(grid):
		start = time.process_time()
		values = solve(grid)
		t = time.process_time()-start
		## Display puzzles that take long enough
		# if showif is not None and t > showif:
		# 	display(grid_values(grid))
		# 	if values: 
		# 		display(values)
		# 	print('(%.2f seconds)\n' % t)
		return (t, solved(values))

	#times, results = zip(*[time_solve(grid) for grid in grids])

	# #if you have a list t = [1,2], you can either say add(t[0], t[1]) 
	# which is needlessly verbose or you can "unpack" t into separate arguments using the * operator like so add(*t).
	results,times = time_solve(grids) #!Works only for single grid
	N = len(grids)
	if N >= 1:
		print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
			sum(results), N, name, sum(times)/N, N/sum(times), max(times)))
 
def solved(values):
	"A puzzle is solved if each unit is a permutation of the digits 1 to 9."
	def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
	return values is not False and all(unitsolved(unit) for unit in unitlist)


#TODO Rank sudoku difficulty from database !
def MAIN():
	start = time.process_time()
	#print(TEST_DISPLAY(depth_first_search(parse_grid(GRID))))
	solve(puzzle)
	t = time.process_time()-start
	os.system('cls')
	print('%.4f seconds on first animation process' % t)
	TEST_DISPLAY(stored_final_grid,speed,isAnimated=False)

if __name__ == '__main__':
	MAIN()




