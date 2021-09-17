# env [?;]

#TODO from SudokuSoftwareOldAlg.Optimal_Sudoku_Solve import *
# def getCrossIxFromCell(state,cellIx) -> helper():
#     """Cool to returns all cells in the row and column of the given cell
#     >>> getCrossIxFromCell(...state, 2) and state.N=4
#             [0,1,3,6,10,14]"""
#     rowIx,colIx = divmod(cellIx,state.N) #row jump by Nix(truediv), col by 1ix (mod)=> shown in other helper functions!

#     peers = set(getCellIxFromRowIx(rowIx,state.N))\
#         ^ (set(getCellIxFromColIx(colIx,state.N))) #Binary op as .symetric_difference()
#     return list(peers)
import os
import sys,time
import string,functools,collections
from typing import Callable, Container, List, Tuple
from pyparsing import *
first16x16 = [[0,15,0,1,0,2,10,14,12,0,0,0,0,0,0,0],
              [0,6,3,16,12,0,15,4,14,15,1,0,2,0,0,0],
              [14,0,9,7,11,3,15,0,0,0,0,0,0,0,0,0],
              [4,13,2,12,0,0,0,0,6,0,0,0,0,15,0,0],
              [0,0,0,0,14,1,15,7,3,5,10,0,0,8,0,12],
              [3,16,0,0,2,4,0,0,0,14,7,13,0,0,5,15],
              [11,0,5,0,0,0,0,0,0,9,4,0,0,6,0,0],
              [0,0,0,0,13,0,16,5,15,0,0,12,0,0,0,0],
              [0,0,0,0,9,0,1,12,0,8,3,10,11,0,15,0],
              [2,12,0,11,0,0,14,3,5,4,0,0,0,0,9,0],
              [6,3,0,4,0,0,13,0,0,11,9,1,0,12,16,2],
              [0,0,10,9,0,0,0,0,0,0,12,0,8,0,6,7],
              [12,8,0,0,16,0,0,10,0,13,0,0,0,5,0,0],
              [5,0,0,0,3,0,4,6,0,1,15,0,0,0,0,0],
              [0,9,1,6,0,14,0,11,0,0,2,0,0,0,10,8],
              [0,14,0,0,0,13,9,0,4,12,11,8,0,0,2,0]]
def encodeCellString(cellContent:str)->unicodeString: return bytes(cellContent,'ascii').decode('unicode_escape')

def ignoreAnsiRawBytes(stringCellSequence,basicEncode=True)->string:
    if basicEncode:
        _unicodeString = encodeCellString(stringCellSequence)
    else:
        _unicodeString = str(stringCellSequence)
    ESC = Literal('\x1b')
    integer = Word(nums)
    escapeSeq = Combine(ESC + '[' + \
        Optional(delimitedList(integer,';')) + oneOf(list(alphas)))

    ignoreAnsiString = lambda string : Suppress(escapeSeq).transformString(string)

    RES = ignoreAnsiString(_unicodeString)
    assert len(str(RES)) == (len(repr(RES)) - 2)
    return RES
    
def color_cellIx(grid,color_code,*cellIxes):
    # Neutral: white \u001b[47m
    # Bad: red \u001b[41m
    # Good: green \u001b[42m
    N = len(grid[0])
    for cellIx in cellIxes:
        rowIx,colIx = divmod(cellIx,N)
        grid[rowIx][colIx] = color_code + str(grid[rowIx][colIx]) + "\u001b[0m"
        ignoreAnsiRawBytes(grid[rowIx][colIx]) #!Test
        
    return grid
# Neutral: white \u001b[47m
# Bad: red \u001b[41m
# Good: green \u001b[42m
def color_cell(cell,*,color_code): return str(color_code) + str(cell) + u"\u001b[0m"
#!----------------
N = int(input("Enter a NxN size:\t"))
CUBE_N = N**0.5
assert (N // CUBE_N) == CUBE_N
assert CUBE_N in {3,4,5}
#!----------------
CELL_WIDTH = int(input("Enter a cell width (better 5 or 6 overall):\t"))#!


BOARD = [   [ '5', '3', '.', '.', '7', '.', '.', '.', '.' ],
            [ '6', '.', '.', '1', '9', '5', '.', '.', '.' ],
            [ '.', '9', '8', '.', '.', '.', '.', '6', '.' ],
            [ '8', '.', '.', '.', '6', '.', '.', '.', '3' ],
            [ '4', '.', '.', '8', '.', '3', '.', '.', '1' ],
            [ '7', '.', '.', '.', '2', '.', '.', '.', '6' ],
            [ '.', '6', '.', '.', '.', '.', '2', '8', '.' ],
            [ '.', '.', '.', '4', '1', '9', '.', '.', '5' ],
            [ '.', '.', '.', '.', '8', '.', '.', '7', '9' ]]
puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8], 
		  [0, 8, 0, 0, 9, 0, 0, 3, 0], 
		  [2, 0, 0, 0, 0, 5, 4, 0, 0], 
		  [4, 0, 0, 0, 0, 1, 8, 0, 0], 
		  [0, 3, 0, 0, 7, 0, 0, 4, 0], 
		  [0, 0, 7, 9, 0, 0, 0, 0, 3], 
		  [0, 0, 8, 4, 0, 0, 0, 0, 6], 
		  [0, 2, 0, 0, 5, 0, 0, 8, 0], 
		  [1, 0, 0, 0, 0, 2, 5, 0, 0]]
class Cell:#TODO make methods part of project class + Utils
    pass
class BoardType:
    pass
def rowColIxToCellIx(rowIx,colIx,N=N) -> int: return N*rowIx + colIx
def cellIxtoRowColIx(cellIx,N=N) -> Tuple[int,int]: return divmod(cellIx,N)

def mapGrid(grid,Function:Callable=lambda cell: "." if cell in ["0",0] else str(cell)): return [list(map(Function,row)) for row in grid]
    
def INIT_apply_cell_width(grid): #?this is like a  init() 
    grid = mapGrid(grid)
    for row_ix,row in enumerate(grid):
        for col_ix,cell in enumerate(row):
            RawANSIcellLength = len(ignoreAnsiRawBytes(cell))
            if RawANSIcellLength > CELL_WIDTH:
                raise Exception("ERROR CHECK INIT() FUNC WITH .CENTER() METHODS")
            elif len(cell) > CELL_WIDTH:
                real_len = len(cell) + (CELL_WIDTH-1)
                if RawANSIcellLength > 1:#more than a byte/ a digit character
                    real_len -= (RawANSIcellLength - 1)
                grid[row_ix][col_ix] = str(cell).center(real_len," ")
            else:
                grid[row_ix][col_ix] = str(cell).center(CELL_WIDTH," ")

    return grid

global ErrorCollector#verbose
ErrorCollector = set()
global ErrorCollection #verbose param for all "check" functions,#TODO use wrapper instead... 
ErrorCollection = True #!
global ErrorBasicColor
ErrorBasicColor = "\u001b[40m\u001b[31;1m"


def simpleDuplicatesFetch(array) -> None:
    global ErrorCollector
    seen_map = dict()
    dupes = list()
    for cell in array:
        #?POSSIBLE DEBUG:  key error if hash(cell) == None
        if cell not in seen_map:
            seen_map[cell] = 1
        else:
            if seen_map[cell] == 1:
                dupes.append(cell)
            seen_map[cell] += 1

    ErrorCollector = ErrorCollector.union(dupes)

def markDuplicatesForFinalPrint(grid) -> None:#* Epic too
    global ErrorCollector,ErrorBasicColor
    ErrorCollector = set(map(str,ErrorCollector))
    
    N = len(grid[0])

    for rowIx in range(N):
        for colIx in range(N):

            cell = ignoreAnsiRawBytes(grid[rowIx][colIx]) #* Epic: even if previously altered by setter, this will only take the nonANSI raw bytes
            cellIx = rowColIxToCellIx(rowIx,colIx)
            if {str(cell)}.issubset(ErrorCollector):#!-----------------------------

                temp_nonANSIgrid = mapGrid(grid,ignoreAnsiRawBytes)
                if not checkCubeOfCell(grid=temp_nonANSIgrid,cellIx=cellIx,isErrorCollectionDone=ErrorCollection):
                    grid = SETCubeOfCell(grid,cellIx,Function=lambda _cell: color_cell(cell=_cell,color_code=f"{ErrorBasicColor}"))
                if not checkRowOfCell(grid=temp_nonANSIgrid,cellIx=cellIx,isErrorCollectionDone=ErrorCollection):
                    grid = SETRowOfCell(grid,cellIx,Function=lambda _cell: color_cell(cell=_cell,color_code=f"{ErrorBasicColor}"))
                if not checkColOfCell(grid=temp_nonANSIgrid,cellIx=cellIx,isErrorCollectionDone=ErrorCollection):
                    grid = SETColOfCell(grid,cellIx,Function=lambda _cell: color_cell(cell=_cell,color_code=f"{ErrorBasicColor}"))           
    return grid

hasNoDuplicates = lambda array: bool(len(set(array)) == len(array))

def isOccupied(num,N=9):
    if type(num) == str:#!change
        return num.isdigit()
    else:
        return bool(int(num) in range(1,N+1))

def removeEmptyCells(array): return list(filter(isOccupied,array))


#board = highlight_cell(board,"\u001b[47m",10,20)
def closestMultipleOfK (num,K): return K * (num//K)
def getCubeOfCell(grid,cellIx)->list:
    res = list()
    N = len(grid[0])
    CUBE_N = int(N**0.5)
    cellRowIx,cellColIx = divmod(cellIx,N)
    minRowIx = closestMultipleOfK(num=cellRowIx,K=CUBE_N)
    minColIx = closestMultipleOfK(num=cellColIx,K=CUBE_N)
    for cubeRow in grid[minRowIx:minRowIx+CUBE_N]:
        for cell in cubeRow[minColIx:minColIx+CUBE_N]:
            res.append(cell)
    return res
def SETCubeOfCell(grid,cellIx,Function:Callable=None)->list:#!------------------------------
    if Function and not callable(Function):
        raise Exception("Enter a proper function in the CubeCellsSetter")
    NEW_GRID = grid
    N = len(grid[0])
    CUBE_N = int(N**0.5)
    cellRowIx,cellColIx = divmod(cellIx,N)
    minRowIx = closestMultipleOfK(num=cellRowIx,K=CUBE_N)
    minColIx = closestMultipleOfK(num=cellColIx,K=CUBE_N)
    for cubeRowIx,cubeRow in enumerate(grid[minRowIx:minRowIx+CUBE_N]):
        for cubeColIx,cell in enumerate(cubeRow[minColIx:minColIx+CUBE_N]):
            NEW_GRID[cubeRowIx][cubeColIx] = Function(cell)
    return NEW_GRID

def checkCubeOfCell(grid,cellIx,isErrorCollectionDone = ErrorCollection )->bool: 
    array_checked = removeEmptyCells(getCubeOfCell(grid,cellIx))
    if hasNoDuplicates(array_checked):
        return True
    elif isErrorCollectionDone:
        simpleDuplicatesFetch(array_checked)#!~

        return False
    else:
        return False

def getRowOfCell(grid,cellIx)-> list: N = len(grid[0]); cellRowIx = cellIx // N; return grid[cellRowIx]
def getColOfCell(grid,cellIx)-> list: N = len(grid[0]); cellColIx = cellIx % N ; return [row[cellColIx] for row in grid]

def SETRowOfCell(grid,cellIx,Function:Callable=None)->list:#!------------------------------
    N = len(grid[0]); cellRowIx = cellIx // N
    NEW_GRID = grid
    for cellColIx,cell in enumerate(grid[cellRowIx]):
        NEW_GRID[cellRowIx][cellColIx] = Function(cell)
    
    return NEW_GRID


def SETColOfCell(grid,cellIx,Function:Callable=None)->list:#!------------------------------
    N = len(grid[0]); cellColIx = cellIx % N 
    NEW_GRID = grid
    for cellRowIx,row in enumerate(grid):
        cell = row[cellColIx]
        NEW_GRID[cellRowIx][cellColIx] = Function(cell)
    
    return NEW_GRID
def checkRowOfCell(grid,cellIx,isErrorCollectionDone = ErrorCollection )->bool: 
    array_checked = removeEmptyCells(getRowOfCell(grid,cellIx))
    if hasNoDuplicates(array_checked):
        return True
    elif isErrorCollectionDone:
        simpleDuplicatesFetch(array_checked)#!~

        return False
    else:
        return False
def checkColOfCell(grid,cellIx,isErrorCollectionDone = ErrorCollection )->bool: 
    array_checked = removeEmptyCells(getColOfCell(grid,cellIx))
    if hasNoDuplicates(array_checked):
        return True
    elif isErrorCollectionDone:
        simpleDuplicatesFetch(array_checked)#!~

        return False
    else:
        return False


def getCrossOfCell(grid,cellIx)-> list: return getRowOfCell(grid,cellIx) + getColOfCell(grid,cellIx)
def checkCrossOfCell(grid,cellIx)-> bool:
    uniqueRowElements = checkRowOfCell(grid,cellIx,isErrorCollectionDone=ErrorCollection)
    uniqueColElements = checkColOfCell(grid,cellIx,isErrorCollectionDone=ErrorCollection)
    return all([uniqueRowElements,uniqueColElements])




def smart_cells(N)->List[Tuple[int,int]]: #? My cool function for fast check_sudoku traversal
    CUBE_N = int(N**0.5)
    #* With N crosses with their middle cell in the N different cubes
    #* I can check with one loop 1/N cross AND 1/N cube... 
    #* see picture in project folder
    smart_cells = [(x,y) for x,y in enumerate(range(0,(N - CUBE_N) + 1,CUBE_N))]
    smart_cells = [(coord[1] + inc, coord[0] + inc*CUBE_N) for coord in smart_cells for inc in range(0,CUBE_N+1-1)]
    return smart_cells


def check_sudoku(grid):
    isSuccess = [True]
    N = len(grid[0])

    smartCells = smart_cells(N)#*

    for smartCell in smartCells:#check each diagonal cell's cross peers from left to right
        smartCellRowIx,smartCellColIx = smartCell[0],smartCell[1]
        smartCellIx = rowColIxToCellIx(smartCellRowIx,smartCellColIx)

        if checkCrossOfCell(grid, smartCellIx) and checkCubeOfCell(grid, smartCellIx):
            pass
        else:
            isSuccess.append(False)
    return all(isSuccess)




def cubes_delimiter(row,*,sep1,sep2,margin=""):#*My cool delim function, good for printing in universal terminals
    """ Allows to have a different pattern in
    printed lines, so cubes appear delimited
    row : input list
    sep1 : normal lines
    sep2 : special lines to delim cubes
    margin : characters at each side of el in row

    N : grid dimensions (must be 4x4,9x9,16x16,etc in order to have inner cubes) 
    """
    N = len(row)
    CUBE_N = int(N**0.5)
    
    
    cubes = [f"{margin}{sep1}{margin}".join([str(char).center(CELL_WIDTH," ") for char in row[ix :ix + CUBE_N]])\
                                        for ix in range(0,N+1,CUBE_N)] 
    return f"{margin}{sep2}{margin}".join(cubes)


TOP = cubes_delimiter(["━"*CELL_WIDTH for _ in range(N)],sep1 = "┯",sep2="┳")
TOP = "┏" + TOP[:-1] + "┓" #replace last "-" by corner

MID = cubes_delimiter(["─"*CELL_WIDTH for _ in range(N)],sep1 = "┼",sep2="╂")
MID = "┠" + MID[:-1]  + "┨"

MID_CUBES_DELIM = cubes_delimiter(["━"*CELL_WIDTH for _ in range(N)],sep1 = "┿",sep2="╋")
MID_CUBES_DELIM = "┣" + MID_CUBES_DELIM[:-1] + "┫"

BOT = cubes_delimiter(["━"*CELL_WIDTH for _ in range(N)],sep1 = "┷",sep2="┻")
BOT = "┗" + BOT[:-1] + "┛" #replace last "-" by corner

def pretty_sudoku(grid,SpeedParam=0.005,isAnimated=False):
    #! assert isinstance(grid[0],list)   
    # TODO implement again the assertions
    N = len(grid)
    CUBE_N = N**0.5
    #!  assert N == len(grid[0])
    
    store_linesToPrint = []
    store_linesToPrint.append(f"\u001b[37;1m{TOP}\u001b[0m")
    #print(f"\u001b[37;1m{TOP}\u001b[0m")
    for row_ix,row in enumerate(grid):

        _row = cubes_delimiter(row,sep1 = "│",sep2="┃")
        _row = "┃" + _row[:-1] + "┃"

        store_linesToPrint.append(f"\u001b[30;1m{_row}\u001b[0m")
        #print(f"\u001b[30;1m{_row}\u001b[0m")

        if row_ix != N-1:        
            if (row_ix+1) % CUBE_N == 0: #ex: 3,6,9,...
                store_linesToPrint.append(f"\u001b[30;1m{MID_CUBES_DELIM}\u001b[0m")
                #print(f"\u001b[30;1m{MID_CUBES_DELIM}\u001b[0m")
            else:
                store_linesToPrint.append(f"\u001b[30;1m{MID}\u001b[0m")
                #print(f"\u001b[30;1m{MID}\u001b[0m")
        
    #//sys.stdout.write("\u001b[1F\u001b[2K")
    #print(f"\u001b[37;1m{BOT}\u001b[0m")
    #store_linesToPrint.append("\u001b[1F\u001b[2K\u001b[1F")
    store_linesToPrint.append(f"\u001b[37;1m{BOT}\u001b[0m")
    
    delete = "\b" * 2#TODO changes if N changes???
    arr = store_linesToPrint
    #sys.stdout.write("\u001b[2J\u001b[5m")
    #os.system( 'cls')
    if isAnimated == True: sys.stdout.write("\u001b[2J\u001b[5m\u001b[80D\u001b[20A")
    pretty_sudoku_string = f"\n{delete}" + f"\n{delete}".join(store_linesToPrint) + "\n"
    print(pretty_sudoku_string,end="")
    # sys.stdout.write("\u001b[1F\u001b[2K")
    # print(f"\u001b[37;1m{BOT}\u001b[0m")
    

    time.sleep(SpeedParam)
    sys.stdout.flush()
    

def printSolveAnimationCycle(grid,speed=0.005,isAnimated=False):
    grid = mapGrid(grid)
    # sys.stdout.flush()
    # sys.stdout.write("\u001b[2J")
    FINAL_BOARD = INIT_apply_cell_width(grid)
    pretty_sudoku(FINAL_BOARD,speed,isAnimated)
    # sys.stdout.flush()
    #print(...,flush=True,end="")

def printCheckedPrettySudoku(FINAL_BOARD):
    sys.stdout.flush()
    sys.stdout.write("\u001b[2J")
    _INPUT_SUDOKU = str(input("Enter the name of the grid you want to print:\t \r\n"))
    #_INPUT_SUDOKU = INIT_apply_cell_width(puzzle)
    FINAL_BOARD = mapGrid(globals()[_INPUT_SUDOKU])

    if check_sudoku(FINAL_BOARD):

        print(u"\u001b[42;1m-> This grid is valid.\u001b[0m")
    else:
        print(u"\u001b[41;1m-> This grid is invalid.\u001b[0m\n\tErrors:",end="\n\t")
        print(ErrorCollector)

    if ErrorCollection == True: #!THIS OPERATION IS A BIT LONGER
        FINAL_BOARD = markDuplicatesForFinalPrint(FINAL_BOARD)#marks any errors found in ErrorCollector

    FINAL_BOARD = INIT_apply_cell_width(FINAL_BOARD)#*Init() before first print

    pretty_sudoku(FINAL_BOARD) #Draw board

def main():
    grid = INIT_apply_cell_width(first16x16)
    printCheckedPrettySudoku(grid)



if __name__ == "__main__":
    # sys.stdout.flush()
    # sys.stdout.write("\u001b[2J")
    # FINAL_BOARD = INIT_apply_cell_width(puzzle)
    # pretty_sudoku(FINAL_BOARD)
    # time.sleep(1)
    # sys.stdout.flush()
    # sys.stdout.write("\u001b[2J")
    # FINAL_BOARD = INIT_apply_cell_width(BOARD)
    # pretty_sudoku(FINAL_BOARD)
    main()
    pass

