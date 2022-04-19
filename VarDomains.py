from copy import deepcopy
from State import State
from termcolor import colored
from util import print_colored

class VarDomains:
    def __init__(self, size):
        self.size = size
        self.domains = [[deepcopy(['w', 'b']) for i in range(size)] for _ in range(size)]


    def get_domain(self, i, j):
        return self.domains[i][j]


    def remove_from_domain(self, board, i, j, val, pr=False):
        if val in self.domains[i][j] and board[i][j].is_empty():
            # if pr:
            #     print('*' * 100)
            #     State(self.size, board).print_board()
            #     # print('Domain: ' + str(self.domains[i][j]))
            #     # print('i,j,val: ' + str((i, j, val)))
            #     # print()
            #     print('*' * 100)
            self.domains[i][j].remove(val)


    def make_empty(self, board, i, j):
        if board[i][j].is_empty():
            self.domains[i][j] = []


    def print(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                d = 'w' if 'w' in self.domains[i][j] else '_'
                # d = ''.join(self.domains[i][j])
                d += 'b' if 'b' in self.domains[i][j] else '_'
                # d = d.ljust(2).replace(' ', '_') + '  '
                s += d + '  '
                # print(d, end='')
            # print()
            s += '\n'
        return s


    def copy(self):
        new_vd = VarDomains(self.size)
        new_vd.domains = deepcopy(self.domains)
        return new_vd


    def any_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if len(self.domains[i][j]) == 0:
                    return True
        return False


    def set_val(self, board, i, j, val, in_place=False):
        assert val in self.domains[i][j]

        if in_place == False:
            new_vd = self.copy()
            new_vd.set_val(board, i, j, val, True)
            return new_vd


        # print('###############################################################################################################')
        # print(f'=========================== i:{i} - j:{j} - val:{val} ==========================')
        # s1 = self.print()
        # print(s1)
        # print(f'================================================================================')
        # State(self.size, board).print_board()


        self.domains[i][j] = [val]

        # Number of same circles in the row i
        count = 0
        for y in range(self.size):
            if board[i][y].value == val:
                count += 1
        # if count > self.size / 2:
        #     for y in range(self.size):
        #         if board[i][y].is_empty():
        #             self.make_empty(i, y)
        if count == self.size / 2:
            for y in range(self.size):
                # print('HHHHHHHH' + str((i, y, val)) +  'HHHHHHHH')
                self.remove_from_domain(board, i, y, val)

        # Number of same circles in the col j
        count = 0
        for x in range(self.size):
            if board[x][j].value == val:
                count += 1
        # if count > self.size / 2:
        #     for x in range(self.size):
        #         if board[x][j].is_empty():
        #             self.make_empty(x, j)
        # return True
        if count == self.size / 2:
            for x in range(self.size):
                # print(f'=========================== i: {i}, j: {j} ||| x: {x}, val: {val} ===========================')
                self.remove_from_domain(board, x, j, val, True)

        # return True
        # Check for 3 consecutive cirlces

        if i-1 >= 0 and board[i-1][j].value == val:
            if i-2 >= 0:
                # print('XXXXX' + str((i-2, j, val)) +  'XXXXX')
                self.remove_from_domain(board, i-2, j, val)
            if i+1 < self.size:
                # print('XXXXX' + str((i+1, j, val)) +  'XXXXX')
                self.remove_from_domain(board, i+1, j, val)
        # if True: return

        if i+1 < self.size and board[i+1][j].value == val:
            if i-1 >= 0:
                self.remove_from_domain(board, i-1, j, val)
            if i+2 < self.size:
                self.remove_from_domain(board, i+2, j, val)
        if j-1 >= 0 and board[i][j-1].value == val:
            if j-2 >= 0:
                self.remove_from_domain(board, i, j-2, val)
            if j+1 < self.size:
                self.remove_from_domain(board, i, j+1, val)
        if j+1 < self.size and board[i][j+1].value == val:
            if j-1 >= 0:
                self.remove_from_domain(board, i, j-1, val)
            if j+2 < self.size:
                self.remove_from_domain(board, i, j+2, val)

        if i-2 >= 0 and board[i-2][j].value == val:
            self.remove_from_domain(board, i-1, j, val)
        if i+2 < self.size and board[i+2][j].value == val:
            self.remove_from_domain(board, i+1, j, val)
        if j-2 >= 0 and board[i][j-2].value == val:
            self.remove_from_domain(board, i, j-1, val)
        if j+2 < self.size and board[i][j+2].value == val:
            self.remove_from_domain(board, i, j+1, val)


        # print(f'================================================================================')
        # s2 = self.print()
        # print_colored(s1, s2)
        # print('###############################################################################################################')
