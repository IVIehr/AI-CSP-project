from copy import deepcopy
from State import State
from termcolor import colored

class VarDomains:
    def __init__(self, size):
        self.size = size
        self.domains = [[deepcopy(['w', 'b']) for i in range(size)] for _ in range(size)]


    def get_domain(self, i, j):
        return self.domains[i][j]


    def mrv(self, board):
        min_d = 100
        min_pair = (None, None)
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].is_empty():
                    d = len(self.domains[i][j])
                    if d < min_d:
                        min_d = d
                        min_pair = (i, j)
        return min_pair


    def get_domain_sorted_by_lcv(self, board, i, j):
        domain = self.domains[i][j]
        if len(domain) == 1:
            return self.domains[i][j]

        w_constraints = self.lcv_count(board, i, j, 'w')
        b_constraints = self.lcv_count(board, i, j, 'b')

        if w_constraints > b_constraints:
            return ['b', 'w']
        else:
            return ['w', 'b']


    def lcv_count(self, board, i, j, val):
        constraints = 0

        count = 0
        for y in range(self.size):
            if board[i][y].value == val:
                count += 1
        if count == self.size / 2:
            for y in range(self.size):
                if self.can_remove_from_domain(board, i, y, val):
                    constraints += 1

        count = 0
        for x in range(self.size):
            if board[x][j].value == val:
                count += 1
        if count == self.size / 2:
            for x in range(self.size):
                if self.can_remove_from_domain(board, x, j, val):
                    constraints += 1

        if i-1 >= 0 and board[i-1][j].value == val:
            if i-2 >= 0:
                if self.can_remove_from_domain(board, i-2, j, val):
                    constraints += 1
            if i+1 < self.size:
                if self.can_remove_from_domain(board, i+1, j, val):
                    constraints += 1
        if i+1 < self.size and board[i+1][j].value == val:
            if i-1 >= 0:
                if self.can_remove_from_domain(board, i-1, j, val):
                    constraints += 1
            if i+2 < self.size:
                if self.can_remove_from_domain(board, i+2, j, val):
                    constraints += 1
        if j-1 >= 0 and board[i][j-1].value == val:
            if j-2 >= 0:
                if self.can_remove_from_domain(board, i, j-2, val):
                    constraints += 1
            if j+1 < self.size:
                if self.can_remove_from_domain(board, i, j+1, val):
                    constraints += 1
        if j+1 < self.size and board[i][j+1].value == val:
            if j-1 >= 0:
                if self.can_remove_from_domain(board, i, j-1, val):
                    constraints += 1
            if j+2 < self.size:
                if self.can_remove_from_domain(board, i, j+2, val):
                    constraints += 1

        if i-2 >= 0 and board[i-2][j].value == val:
            if self.can_remove_from_domain(board, i-1, j, val):
                constraints += 1
        if i+2 < self.size and board[i+2][j].value == val:
            if self.can_remove_from_domain(board, i+1, j, val):
                constraints += 1
        if j-2 >= 0 and board[i][j-2].value == val:
            if self.can_remove_from_domain(board, i, j-1, val):
                constraints += 1
        if j+2 < self.size and board[i][j+2].value == val:
            if self.can_remove_from_domain(board, i, j+1, val):
                constraints += 1

        return constraints


    def can_remove_from_domain(self, board, i, j, val):
        return val in self.domains[i][j] and board[i][j].is_empty()


    def remove_from_domain(self, board, i, j, val):
        if self.can_remove_from_domain(board, i, j, val):
            self.domains[i][j].remove(val)


    def make_empty(self, board, i, j):
        if board[i][j].is_empty():
            self.domains[i][j] = []


    def print(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                d = 'w' if 'w' in self.domains[i][j] else '_'
                d += 'b  ' if 'b' in self.domains[i][j] else '_  '
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


    def ac3(self, board, in_place=False):
        if in_place == False:
            new_vd = self.copy()
            contradiction = new_vd.ac3(board, True)
            return new_vd, contradiction

        contradiction = False
        queue = []
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].is_empty():
                    queue.append((i, j))

        while len(queue) > 0 and not contradiction:
            i, j = queue.pop(0)
            d = self.domains[i][j]
            removed_values = False
            for val in d:
                new_vd = self.copy()
                new_vd.set_val(board, i, j, val, True)
                if new_vd.any_empty():
                    removed_values = True
                    self.domains[i][j].remove(val)
            if removed_values:
                queue.append((i, j))
                if len(self.domains[i][j]) == 0:
                    contradiction = True

        return contradiction


    def set_val(self, board, i, j, val, in_place=False):
        assert val in self.domains[i][j]

        if in_place == False:
            new_vd = self.copy()
            new_vd.set_val(board, i, j, val, True)
            return new_vd

        self.domains[i][j] = [val]

        count = 0
        for y in range(self.size):
            if board[i][y].value == val:
                count += 1
        if count == self.size / 2:
            for y in range(self.size):
                self.remove_from_domain(board, i, y, val)

        count = 0
        for x in range(self.size):
            if board[x][j].value == val:
                count += 1
        if count == self.size / 2:
            for x in range(self.size):
                self.remove_from_domain(board, x, j, val)

        if i-1 >= 0 and board[i-1][j].value == val:
            if i-2 >= 0:
                self.remove_from_domain(board, i-2, j, val)
            if i+1 < self.size:
                self.remove_from_domain(board, i+1, j, val)
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
