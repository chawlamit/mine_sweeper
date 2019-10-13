import numpy as np

def partial_equations(a, b):
    # new_mat = a.copy()
    prev_change_count = -1
    change_count = 0
    while change_count != prev_change_count:
        prev_change_count = change_count
        for i in range(len(a)):
            for j in range(len(a)):
                if i == j:
                    continue
                if sum(a[i]) == 0:
                    return
                if len(set(np.where(a[i] == 1)[0]).intersection(set(np.where(a[j] == 1)[0]))) == sum(a[i]):
                    change_count += 1
                    print(i, j)
                    a[j, np.where(a[i] == 1)[0]] = 0
                    b[j] -= b[i]
                    # print("error")
        print(a)
        print("cc"+str(change_count) )
        print("pcc"+str(prev_change_count) )
