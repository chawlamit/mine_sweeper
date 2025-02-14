from environment import Environment
import random
from abc import ABC, abstractmethod
from minesweepermatplot import MineSweeper
import matplotlib.pyplot as plt
from utils import SETTINGS


class BaseAgent(ABC):
    FLAG = -2

    def __init__(self, env: Environment, debug=False, visualize=False):
        self.env = env
        self.kb = {}
        self.visualize = visualize
        SETTINGS['debug'] = debug

        # stats
        self.cells_turned = 0
        self.mines_flagged = 0
        self.mines_burst = 0
        self.fringe = []

        if visualize:
            self.visual_ms = ms = MineSweeper(self.env.dim, self.env.dim, self.env.n_mines)
            ms._show_board()

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
        row, col = random_point[0] // self.env.dim, random_point[0] % self.env.dim

        # keep picking cells until you find an unturned cell / unflagged cell
        while (row, col) in self.kb:
            random_point = random.sample(range(self.env.dim * self.env.dim), 1)
            row, col = random_point[0] // self.env.dim, random_point[0] % self.env.dim
        return row, col

    def query(self, row: int, col: int):
        """
        Wrapper function around environments query method
        :param row:
        :param col:
        :return: env.MINE or Mine count in 8 neighbors
        """
        clue = self.env.query(row, col)
        self.cells_turned += 1
        self.update_visualization(clue, row, col)
        return clue

    def flag(self, row, col):
        """
        Mark a cell as flagged in knowledge base
        :param row:
        :param col:
        :return:
        """
        self.kb[(row, col)] = self.FLAG
        self.mines_flagged += 1
        self.update_visualization(-1, row, col, 3)

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
        print(f'{self.__class__.__name__}: correctly_flagged: {correctly_flagged_mines}, incorrectly_flagged:{incorrectly_flagged_mines}')
        return score

    def update_visualization(self, clue, row, col, button = 1):
        """
        Update the visualization after a cell is turned or flagged
        """
        if self.visualize:
            event = Event(row, col, button)
            self.visual_ms._button_press(event, clue)


class Event:
    def __init__(self, xdata, ydata, button):
        self.xdata = xdata
        self.ydata = ydata
        self.button = button
