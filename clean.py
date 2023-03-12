import numpy as np
import matplotlib.pyplot as plt
import statistics

def remove_invalid(seeds):
	# remove column from fitness value array if the final creature was deemed to be invalid
	fig, ax = plt.subplots()

	for seed in seeds:
		arr = np.load(f"./NH-2/{seed}/fitnessValues.npy")

		min_val = np.min(arr[-1])
		min_col = np.where(arr[-1] == min_val)[0][0]
		# remove the column containing the minimum value
		new_arr = np.delete(arr, min_col, axis=1)

		ax.plot(np.min(new_arr, axis=1)*-1, label=seed, lw=2)

		print(new_arr.shape)

		np.save(f"./NH-2-take2/{seed}/fitnessValues-valid.npy", new_arr)

	plt.legend()
	plt.show()

def gen_stats():
	# scrape the median fitness values as well
	seeds = [154, 172, 209, 241, 415, 518, 648, 827, 859, 923] 
	for nh in [0,1,2]:
		medf = open(f"NH-stats-{nh}-medians.csv", "w", encoding="utf8")
		best1 = open(f"NH-stats-{nh}-best1.csv", "w", encoding="utf8")
		best5 = open(f"NH-stats-{nh}-best5.csv", "w", encoding="utf8")
		for seed in seeds:
			arr = np.load(f"./NH-{nh}/{seed}/fitnessValues.npy")
			res5=[]

			# find the minimum value in the last row

			l = list(arr[-1])
			l.sort()

			med = str(statistics.median(l))

			ele=l.pop(0)
			res1=str(ele)
			res5.append(res1)

			res5.append(str(l.pop(0)))
			res5.append(str(l.pop(0)))
			res5.append(str(l.pop(0)))
			res5.append(str(l.pop(0)))

			medf.writelines(med + "\n")
			best1.writelines(res1 + "\n")
			for i in range(5):
				best5.writelines(res5[i] + "\n")

		medf.close()
		best1.close()
		best5.close()