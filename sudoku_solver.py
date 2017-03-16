
ONE_TO_NINE=set(i for i in range(1,10))

def collision_coord(i):
        line=[j for j in range((i//9)*9,(i//9+1)*9)]
        col=[j for j in range(i%9,9*9,9) ]
        box=[j for j in boxfinder(i//9,i%9) ]
        return line+col+box

def boxfinder(l,c):
    t=[0,0]
    for i in range(0,9,3):
        if i<=l<=i+2 and t[0]==0:
            t[0]=(i,i+3)
        if i<=c<=i+2 and t[1]==0:
            t[1]=(i,i+3)
    return [(i*9+j%9) for i in range(t[0][0],t[0][1]) for j in range(t[1][0],t[1][1])]

COLLISION_COORDS=[(collision_coord(i)) for i in range(81)]

def read_puzzles_from_pe_file(file):
    m=[]
    f=open(file,'r').read().splitlines()
    while f:
        m.append(''.join(i for i in f[1:10]))
        f=f[10:]
    return m

class Sudoku(object):
    
    def __init__(self,puzzle):
        self.orig_puzzle=puzzle
        self.sudoku_puzzle=[]
        self.solution_table=[]
        self.solution_order=[]
        

    def deduction_solve(self):
        change_made = True
        self.sudoku_puzzle = [int(i)for i in self.orig_puzzle]
        while change_made:
            change_made = False
            for i in range(81):
                if not self.sudoku_puzzle[i] in ONE_TO_NINE:
                    collide = set(self.sudoku_puzzle[j] for j in COLLISION_COORDS[i])
                    sols = [j for j in ONE_TO_NINE if j not in collide]
                    if len(sols) == 1:
                        self.sudoku_puzzle[i] = sols[0]
                        change_made = True
      
    
    def find_candidates(self):
        self.solution_table=[False]*81
        for i in range(81):
            if self.sudoku_puzzle[i] not in ONE_TO_NINE:
                collision_points=set(self.sudoku_puzzle[j] for j in COLLISION_COORDS[i])
                self.solution_table[i]=set((filter(lambda x:x not in collision_points,ONE_TO_NINE)))


    def backtrack_solve(self):
        if not self.solution_table :
                self.find_candidates()
        if 0 not in self.sudoku_puzzle:
            return self.sudoku_puzzle
     
        location=self.sudoku_puzzle.index(0)
        collide=set(self.sudoku_puzzle[i]for i in COLLISION_COORDS[location])
        for i in self.solution_table[location].difference(collide):
            self.sudoku_puzzle[location]=i
            if self.backtrack_solve():
                return self.sudoku_puzzle
            self.sudoku_puzzle[location]=0
        return False
    
    def solve_sudoku(self):     
        self.deduction_solve()
        if 0 not in self.sudoku_puzzle:
            return self.sudoku_puzzle
        else:
           return self.backtrack_solve()
             

def print_sudoku(s):
    if not s:
        print("No solution")
        return 
    for i in range(9):
        print(str(s[9*i:9*(i+1)]))
    print()

def write_solution_to_file(filename,sud,index):
    with open("ResultsFor"+filename,'a') as f:
        f.write("Grid {}\n".format(index))
        for i in range(9):
            f.write(str(sud[9*i:9*(i+1)]))
            f.write("\n")


def solve_puzzles(file_name,out):

        try:
            puzzle_book=read_puzzles_from_pe_file(file_name)
        except NameError:
            print("No such file found")
            return   
        solved=list()

        for sudoku_puzzles in puzzle_book:
           
            solved.append(Sudoku(sudoku_puzzles).solve_sudoku())
            if out == 'S':
                print(len(solved))
                print_sudoku(solved[-1])
            if out == "F":
                write_solution_to_file(file_name,solved[-1],len(solved))

def main():
        from time import clock
        file_name=input("File:").strip()
        cout_method=input("Write results to screen or new file(ResultsFor{})?(S/F):".format(file_name)).strip().upper()
        ht=clock()
        solve_puzzles(file_name,cout_method.upper())
        print(clock()-ht)
    
        

if __name__=='__main__':
    main()
    
