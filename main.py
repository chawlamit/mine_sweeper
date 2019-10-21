from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent
from minesweepermatplot import MineSweeper
import matplotlib.pyplot as plt


env = Environment(10, 40)
# env._board = [[0, 0, 0, -1, 0],
# [-1, 0, 0, 0, 0],
# [-1, 0, 0, 0, 0],
# [0, 0, -1, 0, 0],
# [0, 0, -1, 0, 0]]
env.show()

# agent = BaselineAgent(env)
# agent.run()
# print(agent.calc_score())

agent = Agent(env)
# MineSweeper.intermediate()
# plt.show()
agent.run()
print(agent.calc_score())

