import numpy as np
import matplotlib.pyplot as plt

def plotify(tags, solved, unsolved, handle):
	n_groups = len(tags)
	fig, ax = plt.subplots()

	index = np.arange(n_groups) * 11.5
	bar_width = 2.5
	opacity = 0.4
	offset = 1.5

	plt.bar(index + offset, solved, bar_width, alpha=opacity, color='b', label='Solved')
	plt.bar(index + offset + bar_width, unsolved, bar_width, alpha=opacity, color='r', label='Unsolved')

	fig.set_size_inches([10, 5])
	
	plt.title('User ' + handle + ' submissions')
	#plt.ylabel('Problems')
	plt.xticks(index + offset + bar_width, tags)
	plt.axis([0, 100, 0, 50])
	plt.yticks(np.arange(0, 51, 5))
	plt.legend()
	#plt.tight_layout()
	plt.savefig('cf_stats.png')
