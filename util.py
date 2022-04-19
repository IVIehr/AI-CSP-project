from termcolor import colored, cprint


def print_colored(s1, s2):
    l = len(s1)
    colors = list([0 for i in range(l)])
    for i in range(l):
        if s1[i] != s2[i]:
            colors[i] = 1
    for i in range(l):
        if colors[i] == 0:
            print(s2[i], end='')
        else:
            cprint(s2[i], 'red', end='')
