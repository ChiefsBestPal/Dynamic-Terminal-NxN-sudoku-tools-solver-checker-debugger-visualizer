import time, random
import Optimal_Sudoku_Solve as S
#// Computation %completed: (required_instructions/cyclesOractionif1:1 * CPU_clock_speed * cores * processors * time_allowed) / actions)
from UtilitiesSudoku import *
def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.process_time()
        values = S.solve(grid)
        t = time.process_time()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            S.display(S.grid_values(grid))
            if values: 
                S.display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids]) #if you have a list t = [1,2], you can either say add(t[0], t[1]) which is needlessly verbose or you can "unpack" t into separate arguments using the * operator like so add(*t).

    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)



grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
# if __name__ == '__main__':
#     test()
#     solve_all(from_file("easy50.txt", '========'), "easy", None)
#     solve_all(from_file("top95.txt"), "hard", None)
#     solve_all(from_file("hardest.txt"), "hardest", None)
#     solve_all([random_puzzle() for _ in range(99)], "random", 100.0)