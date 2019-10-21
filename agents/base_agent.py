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
        self.manager = dict()
        self.manager['ms'] = ms = MineSweeper(self.env.dim, self.env.dim, self.env.n_mines)
        ms._show_board()
        # p = Process(target=ms._show_board)
        # p.start()

    @abstractmethod
    def run(self):
        """Start running the agent on the given mine sweeper environment"""
        pass

    @abstractmethod
    def infer(self):
        """based on the clue from the environment upton turning a cell, infer basic knowledge from it"""
        pass
    
    # def initialize_visualization_pyqt(self,dim:int, manager) :
    #     # self.app = QApplication([])
    #     # self.window = MainWindow(self.env.dim)
    #     # self.window.show()

    #     if QApplication.instance() is None:
    #         app = QApplication([])
    #         window = MainWindow(dim)
    #         manager['grid'] = window.grid
    #         # self.window.show()
    #         # sleep(1)
    #         app.exec_()
    #         # self.window.callback_pb_load()

    # def update_visualization_pyqt(self, row,col,val):
    #     sleep(1)
    #     w = self.manager['grid'].itemAtPosition(col, row).widget()
    #     if val == Environment.MINE :
    #         w.is_mine = True
    #         w.is_revealed = True
    #     else :
    #         w.is_revealed = True
    #         w.adjacent_n = val
    #     w.update()


    def probabilistic_pick(self, cells_turned: int, mines_flagged: int) :
        ''' Use the Remaining mines information while opening a random point to search '''
        remaining_cells = self.env.dim**2 - cells_turned - mines_flagged
        rand_prob = ( self.env.n_mines - mines_flagged )/ remaining_cells
        dict_hidden_prob = {}
        # plt.pause(0.

        for (row, col) in self.kb:
            clue = self.kb[(row, col)]
            if clue == self.env.MINE or clue == self.FLAG :
                continue
            n, h, m, s = self.infer(row, col)
            if len(h) == 0:
                continue
            prob_hidden = (clue - len(m)) / len(h)
            for (row_, col_) in h:
                if (row_, col_) in dict_hidden_prob :
                    dict_hidden_prob[(row_, col_)] += prob_hidden
                else:
                    dict_hidden_prob[(row_, col_)] = prob_hidden
        list_sorted_probabilities = sorted(dict_hidden_prob.items(), key=lambda l: l[1])
        # print(list_sorted_probabilities)
        # print("rand_prob", rand_prob)
        if list_sorted_probabilities:
            if list_sorted_probabilities[0][1] < rand_prob:
                print("Probabilistic pick ", list_sorted_probabilities[0][0])
                return list_sorted_probabilities[0][0]

        row, col = self.pick_random()

<<<<<<< HEAD
        while(row, col) not in dict_hidden_prob:
            row, col  = self.pick_random()
=======
        while (row, col) in dict_hidden_prob and len(dict_hidden_prob) < remaining_cells:
            row, col = self.pick_random()
>>>>>>> 23fdc827e64386d7a4a578d90b1ad856ea7139e9

        # print("random pick", row, col)
        return row, col

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
        event = Event()
        event.xdata = row
        event.ydata = col
        event.button = 1
        # plt.draw()
        # plt.pause(0.1)
        self.manager['ms']._button_press(event, clue)
        return clue
    
    def flag(self, row, col):
        self.kb[(row, col)] = self.FLAG
        clue = -1
        event = Event()
        event.xdata = row
        event.ydata = col
        event.button = 3
        self.manager['ms']._button_press(event, clue)

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
        plt.pause(50)





            
