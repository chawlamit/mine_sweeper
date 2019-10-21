from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent
from agents.probabilistic_agent import ProbabilisticAgent 
from multiprocessing import Process, Pool, Lock

import numpy as np

import matplotlib.pyplot as plt


env = Environment(50, 5)
# env._board = [[0, 0, 0, -1, 0],
# [-1, 0, 0, 0, 0],
# [-1, 0, 0, 0, 0],
# [0, 0, -1, 0, 0],
# [0, 0, -1, 0, 0]]
# env.show()
# app=QApplication([])

# agent = Agent(env)

# window=MainWindow(env,agent)
# app.exec_()

def performance(agent_holder):
	dim = 10
	with open(f'{dim}_{agent_holder.__name__}.txt', 'w') as fo:
		p2={}
		for mine_density in np.arange(0.10,0.2,0.01):
			print(mine_density)
			# p1[str(mine_density)]=dict()

			f_1=[]

			for i in  range(1,10):
				n_mines=mine_density*dim*dim
				print(np.ceil(n_mines))
				env=Environment(dim,int(np.ceil(n_mines)))
				env.show()
				agent = Agent(env)
				agent.run()
				p1=agent.calc_score()
				f_1.append(p1)

			f_1=np.mean(f_1)
			p2[mine_density] = f_1
			# p1[str(mine_density)]['f_1']=f_1
			# p1[str(mine_density)]['m_1']=m_1

		# mine_density_keys=p2.keys()
		# f_1_1=[p2[density]['f_1'] for density in p2]
		# m_1_1=[p2[density]['m_1'] for density in p2]
		print("p2", p2)
		for el in p2:
			fo.write(f'{el}, {p2[el]}\n')
			
	# plt.plot(m_1_1, f_1_1, marker = 'o', label = "Base CSP Agent")
	# # plt.plot(m_2_2, f_2_2, marker = 'o', label = "Final CSP Agent")
	# plt.xlabel("Mine Density")
	# plt.ylabel("Average Final Score")
	# # plt.savefig('avg_final_score_bonus.png')
	# plt.legend()
	# plt.show()

# performance(10,ProbabilisticAgent)
# agent = BaselineAgent(env)
# agent.run()
# print(agent.calc_score())

# agent = Agent(env)
# agent.run()
# print(agent.calc_score())

	

if __name__ == '__main__':

	pool = Pool(processes=4)              #start 4 worker processes
	pool.map(performance, [BaselineAgent, Agent, ProbabilisticAgent])	
