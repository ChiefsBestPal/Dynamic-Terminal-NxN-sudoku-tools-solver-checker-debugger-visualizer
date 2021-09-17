# import pyautogui, sys
# print('Press Ctrl-C to quit.')
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')
from ConsoleSudokuVisualizerFirstVersion import CELL_WIDTH
from UtilitiesSudoku import *
import time
import sys
import os
arr = ['* * * |* * * |* * * ', '* * * |* * * |* * * ', '* * * |* * * |* * * ', '------+------+------', '* * * |* * * |* * * ', '* * * |* * * |* * * ', '* * * |* * * |* * * ', '------+------+------', '* * * |* * * |* * * ', '* * * |* * * |* * * ', '* * * |* * * |* * * ']


#!UTILITIES------------------
def display(values,speed=0.005):
	"Display these values as a 2-D grid."
	def flush_print_grid(arr,SpeedParam):
		l = '* * * |* * * |* * * '
		L = '------+------+------'
		to = max(len(l),len(L))
		digits = len(str(to - 1))
		delete = "\b" * (digits)
		os.system( 'cls' )
		print("\n{0}{1}\n{0}{2}\n{0}{3}\n{0}{4}\n{0}{5}\n{0}{6}\n{0}{7}\n{0}{8}\n{0}{9}\n{0}{10}\n{0}{11}\n".format(delete, 
			arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9],arr[10]), end="")

		time.sleep(SpeedParam)
		sys.stdout.flush()


	width = 1+max(len(values[s]) for s in squares)
	line = '+'.join(['-'*(width*3)]*3)
	store = []
	for r in rows:
		store.append(''.join(values[r+c].center(width)+('|' if c in '36' else '')
					  for c in cols))

		if r in 'CF':
			store.append(line)

	flush_print_grid(store,speed)
	#print("")
	return
CELL_WIDTH = 5
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


def displayPRETTY(values,speed=0.005):
	pass

def from_file(filename, sep='\n'):
	"Parse a file into a list of strings, separated by sep."
	return file(filename).read().strip().split(sep)

#TODO USER INPUT FOR FUTURE APP AND EVEN OCR
# from tkinter import *
# root = Tk()

# e = Entry(root,width=50)
# e.pack()
# e.insert(0,'WIP: DEBUG; Paste sudoku here')

# def myClick():
# 	hello = 'Test ' + e.get()
# 	myLabel = Label(root, text=hello)
# 	myLabel.pack()

# myButton = Button(root, text='Entry',command=myClick)
# myButton.pack()

# root.mainloop()



