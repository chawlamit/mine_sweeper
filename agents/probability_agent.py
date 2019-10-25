from collections import OrderedDict
import numpy as np
from environment import Environment
from .csp_agent import CSPAgent
from utils import debug,set_reduction
from time import sleep

class ProbabilityAgent(CSPAgent) :

    P = 0.2
    def query(self,row,col):
        self.cells_turned += 1
        if np.random.binomial(1, self.P, 1):
            clue = self.env.query(row, col)
        else :
            clue = None
        self.update_visualization(clue, row, col)
        return clue
