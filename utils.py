import numpy as np

SETTINGS = {'debug': False}


def debug(*args):
    if SETTINGS['debug']:
        print(*args)


def partial_equations(a, b):
    """
    A helper function to reduce the equations of the form ax = b for each unknown cell
    to identify them as mine or not mine
    :param a:
    :param b:
    :return:
    """
    change_count = -1
    while change_count != 0:
        change_count = 0
        for i in range(len(a)):
            for j in range(len(a)):
                if i == j:
                    continue
                if sum(a[i]) == 0 or sum(a[j] == 0):
                    continue
                if len(set(np.where(a[i] == 1)[0]).intersection(set(np.where(a[j] == 1)[0]))) == sum(a[i]):
                    change_count += 1
                    a[j, np.where(a[i] == 1)[0]] = 0
                    b[j] -= b[i]
