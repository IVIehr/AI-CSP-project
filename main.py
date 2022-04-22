from time import time
from Binairo import check_termination, is_consistent
from Cell import *
from State import *
from VarDomains import VarDomains

FAIL = 0xABCD

def main():
    input_numbers = []  ## first row = size of puzzle(n)  ## second row = number of cells that have color in the statrt  (m)  ## row 3 to row 3+m :
    input = open("testcase/input2.txt").readlines()
    for line in input:
        line = line.rstrip()
        numbers = line.split(' ')
        n = [int(number) for number in numbers]
        input_numbers.append(n)

    board = []
    size_puzzle = input_numbers[0][0]
    for i in range(0,size_puzzle):

        row = []
        for j in range(0,size_puzzle):
            cell = Cell(i,j)
            row.append(cell)
        board.append(row)

    vd = VarDomains(size_puzzle)

    for i in range(2,len(input_numbers)) :
        if input_numbers[i][2]==0 : # w
            board[input_numbers[i][0]][input_numbers[i][1]].set_val('w')
            board[input_numbers[i][0]][input_numbers[i][1]].preset = True
            vd.set_val(board, input_numbers[i][0], input_numbers[i][1], 'w', True)
            # board[input_numbers[i][0]][input_numbers[i][1]].value='W'
            # board[input_numbers[i][0]][input_numbers[i][1]].domain=['n']

        if input_numbers[i][2]==1 :  # b
            board[input_numbers[i][0]][input_numbers[i][1]].set_val('b')
            board[input_numbers[i][0]][input_numbers[i][1]].preset = True
            vd.set_val(board, input_numbers[i][0], input_numbers[i][1], 'b', True)
            # board[input_numbers[i][0]][input_numbers[i][1]].value='B'
            # board[input_numbers[i][0]][input_numbers[i][1]].domain=['n']

    state = State(size_puzzle,board)
    print('================= Initial Board ===================')
    state.print_board()
    print()
    start_time = time()

    print('================ Solution Board ===================')
    result = backTrack(state, vd)
    # result = backTrackNormal(state)
    if result == FAIL:
        print('No solution found.')
    else:
        result.print_board()

    end_time = time()
    print(f'\nTime: {end_time-start_time} seconds')



def backTrack(state, vd):
    if check_termination(state):
        return state

    # Apply AC3
    new_vd, contradiction = vd.ac3(state.board)
    if contradiction:
        return FAIL
    vd = new_vd

    # Select next variable
    # i, j = state.next_empty_cell()
    i, j = vd.mrv(state.board)
    if i == None:
        return FAIL

    # for val in vd.get_domain(i ,j):
    for val in vd.get_domain_sorted_by_lcv(state.board, i ,j):
        state.board[i][j].set_val(val)
        new_vd = vd.set_val(state.board, i, j, val)
        if not new_vd.any_empty():
            result = backTrack(state, new_vd)
            if result != FAIL:
                return result
        state.board[i][j].remove_val()

    return FAIL



def backTrackNormal(state):
    if check_termination(state):
        return state

    # Select next variable
    i, j = state.next_empty_cell()

    for val in state.board[i][j].domain:
        state.board[i][j].set_val(val)
        if is_consistent(state):
            result = backTrackNormal(state)
            if result != FAIL:
                return result
        state.board[i][j].remove_val()

    return FAIL



if __name__=="__main__":
    main()
