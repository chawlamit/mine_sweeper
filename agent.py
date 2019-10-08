from environment import Environment
import random
class Agent:

    def __init__(self, env: Environment):
        self.env = env

    def query(self, row, col):
        pass


env = Environment(5, 7)
env.show()
kb = {}

def infer(row, col):
    safe = set()
    mines = set()
    neighbors = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            #print(row+i,col+j)
            if i == 0 and j == 0:
                continue
            if env.is_valid(row+i, col+j):
                neighbors.add( (row+i,col+j) )
            if (row+i, col+j) in kb:
                clue = kb[(row + i, col + j)]
                if clue == -1:
                    mines.add( (row+i,col+j) )
                else:
                    safe.add( (row+i,col+j) )
    hidden = neighbors - mines - safe

    return (neighbors, hidden, mines, safe)

def pick_random(env):
    random_point = random.sample(range(env.dim * env.dim), 1)
    return ( random_point[0] // env.dim, random_point[0] % env.dim)


row, col = pick_random(env)
fringe = [(row, col)]

while(len(kb) < env.dim * env.dim):
    # print('Fringe: ', fringe)
    if fringe:
        row, col = fringe.pop(0)
    else:
        row, col = pick_random(env)

    kb[(row, col)] = env.query(row, col)
    clue = kb[(row, col)]

    neighbors, hidden, mines, safe = infer(row, col)
    if clue - len(mines) == len(hidden):
        for el in hidden:
            kb[el] = -2

    if len(neighbors) - clue - len(safe) == len(hidden):
        for el in hidden:
            kb[el] = env.query(el[0], el[1])
            fringe.append(el)
    # print(kb)
print(kb)
