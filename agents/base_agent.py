from environment import Environment
import random
from abc import ABC, abstractmethod
from time import sleep
# from visualization import MainWindow
# from PyQt5.QtWidgets import QApplication
from multiprocessing import Process, Manager
from minesweepermatplot import MineSweeper
import matplotlib.pyplot as plt


class Event:
    pass


class BaseAgent(ABC):
    FLAG = -2

    def __init__(self, env: Environment):
        self.env = env
        self.kb = {}

        # stats
        self.cells_turned = 0
        self.mines_flagged = 0
        self.mines_burst = 0
        self.fringe = []

        # self.manager = dict()
        # self.manager['ms'] = ms = MineSweeper(self.env.dim, self.env.dim, self.env.n_mines)
        # ms._show_board()

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
        event = Event()
        event.xdata = row
        event.ydata = col
        event.button = 1
        # plt.draw()
        # plt.pause(0.1)
        # self.manager['ms']._button_press(event, clue)
        return clue

    def flag(self, row, col):
        self.kb[(row, col)] = self.FLAG
        self.mines_flagged += 1
        clue = -1
        event = Event()
        event.xdata = row
        event.ydata = col
        event.button = 3
        # self.manager['ms']._button_press(event, clue)

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

    def wait(self):
        plt.pause(5)

    # def simulate_steps(self, ):
