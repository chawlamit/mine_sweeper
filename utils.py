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


def set_reduction(eqns, b):
    change_count = -1
    eqns_list = list(eqns.items())
    n = len(eqns_list)

    while change_count != 0:
        change_count = 0
        for i, el in enumerate(eqns_list):
            set1 = el[1]

            for j in range(i+1, n):
                set2 = eqns_list[j][1]
                if set1 == set2:
                    continue

                if set2.issubset(set1):
                    # debug(set1, set2, b[i], b[j])
                    set1.difference_update(set2)
                    b[i] -= b[j]
                    change_count += 1

                elif set1.issubset(set2):
                    # debug(set1, set2, b[i], b[j])
                    set2.difference_update(set1)
                    b[j] -= b[i]
                    change_count += 1





