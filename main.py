from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent


import numpy as np

import matplotlib.pyplot as plt


# env = Environment(5, 5)
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

def performance(dim,agent_holder):
	p2={}
	for mine_density in np.arange(0.10,0.2,0.01):
		print(mine_density)
		# p1[str(mine_density)]=dict()

		f_1=[]
		m_1=[]

		for i in  range(1,10):
			n_mines=mine_density*dim*dim
			print(np.ceil(n_mines))
			env=Environment(dim,int(np.ceil(n_mines)))
			env.show()
			agent = agent_holder(env)
			agent.run()
			p1=agent.calc_score()
			f_1.append(p1)
			m_1.append(n_mines)

		f_1=np.mean(f_1)
		m_1=np.mean(m_1)
		p2[mine_density] = {
			'f_1' : f_1,
			'm_1' : m_1
		}
		# p1[str(mine_density)]['f_1']=f_1
		# p1[str(mine_density)]['m_1']=m_1

	mine_density_keys=p2.keys()
	f_1_1=[p2[density]['f_1'] for density in p2]
	m_1_1=[p2[density]['m_1'] for density in p2]


	plt.plot(m_1_1, f_1_1, marker = 'o', label = "Base CSP Agent")
	# plt.plot(m_2_2, f_2_2, marker = 'o', label = "Final CSP Agent")
	plt.xlabel("Mine Density")
	plt.ylabel("Average Final Score")
	# plt.savefig('avg_final_score_bonus.png')
	plt.legend()
	plt.show()

performance(20,Agent)
# agent = BaselineAgent(env)
# agent.run()
# print(agent.calc_score())

# agent = Agent(env)
# agent.run()
# print(agent.calc_score())

	

