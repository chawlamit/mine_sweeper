from environment import Environment
import random
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    FLAG = -2

    def __init__(self, env: Environment):
        self.env = env
        self.kb = {}

    @abstractmethod
    def run(self):
        """Start running the agent on the given mine sweeper environment"""
        pass

    @abstractmethod
    def infer(self):
        """based on the clue from the environment upton turning a cell, infer basic knowledge from it"""
        pass

    def pick_random(self):
        """
        Find a random starting point within the environment to start its search from
        :return: (row, col) : returns the row, col value of chosen cell
        """
        random_point = random.sample(range(self.env.dim * self.env.dim), 1)
        return random_point[0] // self.env.dim, random_point[0] % self.env.dim

    def query(self, row: int, col: int):
        """
        Wrapper function around environments query method
        :param row:
        :param col:
        :return: env.MINE or Mine count in 8 neighbors
        """
        return self.env.query(row, col)
    
    def calc_score(self):
        """
        Calculates the score for your agent based on
        Correctly_flagged_mines - Incorrectly_flagged_Mines / Total_no_of_mines :return:
        """
        correctly_flagged_mines = 0
        incorrectly_flagged_mines = 0
        undiscovered_mines = 0
        for i, j in self.kb:
            if self.kb[(i, j)] == self.FLAG:
                if self.env.has_mine(i, j):
                    correctly_flagged_mines += 1
                else:
                    incorrectly_flagged_mines += 1
            elif self.kb[(i, j)] == self.env.MINE:
                undiscovered_mines += 1
        score = (correctly_flagged_mines - incorrectly_flagged_mines) / self.env.n_mines
        print(f'correctly_flagged: {correctly_flagged_mines}, incorrectly_flagged:{incorrectly_flagged_mines}')
        return score








            
