from time import time
from Binairo import check_termination, is_consistent
from Cell import *
from State import *

FAIL = 0xABCD

def main():
    input_numbers = []  ## first row = size of puzzle(n)  ## second row = number of cells that have color in the statrt  (m)  ## row 3 to row 3+m :
    input = open("input2.txt").readlines()
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

    for i in range(2,len(input_numbers)) :


        if input_numbers[i][2]==0 : # w
            board[input_numbers[i][0]][input_numbers[i][1]].set_val('W')
            # board[input_numbers[i][0]][input_numbers[i][1]].value='W'
            # board[input_numbers[i][0]][input_numbers[i][1]].domain=['n']

        if input_numbers[i][2]==1 :  # b
            board[input_numbers[i][0]][input_numbers[i][1]].set_val('B')
            # board[input_numbers[i][0]][input_numbers[i][1]].value='B'
            # board[input_numbers[i][0]][input_numbers[i][1]].domain=['n']

    state = State(size_puzzle,board)
    print('================= Initial Board ================')
    state.print_board()
    print('\n')
    start_time = time()

    print('================ Solution Board ================')
    result = backTrack(state)
    if result == FAIL:
        print('No solution found :(')
    else:
        result.print_board()

    end_time = time()
    print('time: ', end_time-start_time)



def backTrack(state):
    if check_termination(state):
        return state

    # Select next empty cell
    i, j = state.next_empty_cell()

    for val in state.board[i][j].domain:
        state.board[i][j].set_val(val)
        if is_consistent(state):
            result = backTrack(state)
            if result != FAIL:
                return result
        state.board[i][j].remove_val()

    return FAIL



if __name__=="__main__":
    main()
