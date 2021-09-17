#Each cells has 3 units (Column, Row, Box) and so 20 peers (all unique cells in from all units )
#So 9 cells per unit and cells that share a unit are peers

cross = lambda A,B: [a+b for a in A for b in B]
digits   = '123456789TUVWXYZ'
rows     = 'ABCDEFGHIJKLMNOP'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
			[cross(r, cols) for r in rows] +
			[cross(rs, cs) for rs in ('ABCD','EFGH','IJKL','MNOP') for cs in ('1234','5678','9TUV','WXYZ')])
#unitlist: [[the 9 rows][the 9 cols][the 9 boxes]]
#*print(np.array(list(chunk(9,unitlist))))
units = dict((s, [u for u in unitlist if s in u]) 
			 for s in squares)
# print(squares)
# print('\n\n\n\n\n') #! UNECESSARY PRINTS THAT RUN IN THE MAIN PROGRAM! 
# print(units)
# print('\n\n\n\n\n')
#units synthax: {k:v} => {rowcol: [[9 cells in Row][9 cells in Col][9 cells in Box]]}
peers = dict((s, set(sum(units[s],[]))-set([s]))
			 for s in squares)
# print(peers)
#peers synthax: {k,v} => {rowcol: {the 20 peers of key/square}}

def chunk(N,arr):
	for i in range(0, len(arr), N):  
		yield arr[i:i + N]
def ifin(el,*iters): 
	for i in iters:
		if el in i:
			yield True
