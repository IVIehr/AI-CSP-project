from Cell import *

class State:
    def __init__(self,size,board=[]):
        self.board = board
        self.size = size


    def print_domain(self):
        for i in range(0,self.size):
            for j in range(0,self.size):
                print(self.board[i][j].domain,end=" ")
            print("\n")


    def print_board(self):
        whtieCircle = '\u26AA'
        blackCircle = '\u26AB'
        w_sqr='\u2B1C'
        b_sqr= '\u2B1B'
        line = '\u23E4'

        whtieCircle = 'w '
        blackCircle = 'b '
        w_sqr='W '
        b_sqr= 'B '
        line = '--'

        for i in range(self.size):
            for j in range(self.size):
                if (self.board[i][j].value == 'b'):
                    if self.board[i][j].preset:
                        print(b_sqr, end='  ')
                    else:
                        print(blackCircle, end='  ')

                elif (self.board[i][j].value == 'w'):
                    if self.board[i][j].preset:
                        print(w_sqr,end='  ')
                    else:
                        print(whtieCircle,end='  ')
                else:
                    print(line,end='')
                    print(end='  ')
            print()


    def next_empty_cell(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].is_empty():
                    return i, j
        return None, None
