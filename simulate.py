from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.csp_agent import CSPAgent
from agents.mine_aware_agent import MineAwareAgent
from agents.probability_agent import ProbabilityAgent
from multiprocessing import Process, Pool, Lock
import time

import numpy as np


def performance(p):
    dim = 40
    n_sims = 10

    agent_holder = ProbabilityAgent
    agent_name = agent_holder.__name__
    p2 = {p: {}}
    for mine_density in np.arange(0.10, 0.52, 0.01):
        print(f'Simulation for {agent_name}, {mine_density}')

        f_1 = []
        for i in range(n_sims):
            n_mines = mine_density * dim*dim
            n_mines = int(np.ceil(n_mines))
            env = Environment(dim, n_mines)
            agent = agent_holder(env, debug=False, visualize=False)
            st = time.time()
            agent.P = p
            agent.run()
            print('time: ', agent_name, time.time() - st)
            p1 = agent.calc_score()
            f_1.append(p1)

        mean_score = np.mean(f_1)
        p2[p][mine_density] = mean_score
        print(agent_name, agent.P, mine_density, mean_score)
    print(agent_name, p2)


if __name__ == '__main__':

    probaility_range = np.arange(0.1, 1.1, 0.1)
    # start 4 worker processes
    pool = Pool(processes=3)
    pool.map(performance, probaility_range)