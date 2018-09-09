import csv
import operator
import pprint as pp
import numpy as np
import pandas as pd
import pdb
import random
from matplotlib import pyplot

import pylab 
import scipy.stats as stats

from handle_missing_economy import handle_economy
from handle_missing_education import handle_education
from handle_missing_demography import handle_demography, alter, convert, notvalid

data = {}
demo = handle_demography()
edu = handle_education()
eco = handle_economy()
data.update(demo)
data.update(edu)
data.update(eco)


with open('regions.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	sortedlist = sorted(csv_reader, key= operator.itemgetter(1))


state_dic = {}
state_to_region = {}

for [x,y] in sortedlist[1:]:
	state_to_region[x] = y
	state_dic[x] = []

for x in state_dic:
	y = alter(x)
	state_dic[y] = state_dic.pop(x)
	state_to_region[y] = state_to_region.pop(x)
state_to_region['allindia'] = None
state_dic['allindia'] = []

# for x in data:
# 	base = min(data[x])
# 	rage = max(max(data[x]) - base , 1)
# 	data[x] = [(y-base)/rage for y in data[x]]

state_list = state_to_region.keys()
feature_list = []
for x in data:
	for j in range(0,len(data[x])):
		state_dic[state_list[j]].append(data[x][j])

def nearest_miss(state, feature_idx):
	mindist = np.inf
	score = 0
	for x in state_dic:
		if(x == state or x == 'allindia' or state_to_region[x] == state_to_region[state]):
			continue
		else:
			# mindist = min(mindist , np.linalg.norm(np.subtract(state_dic[state], state_dic[x])))
			if(mindist> np.linalg.norm(np.subtract(state_dic[state], state_dic[x]))):
				mindist= np.linalg.norm(np.subtract(state_dic[state], state_dic[x]))
				score = (state_dic[state][feature_idx]-state_dic[x][feature_idx])**2
	return score


def nearest_hit(state, feature_idx):
	mindist = np.inf
	score = 0
	for x in state_dic:
		if(x == state or x == 'allindia' or state_to_region[x] <> state_to_region[state]):
			continue
		else:
			# mindist = min(mindist , np.linalg.norm(np.subtract(state_dic[state], state_dic[x])))
			if(mindist> np.linalg.norm(np.subtract(state_dic[state], state_dic[x]))):
				mindist= np.linalg.norm(np.subtract(state_dic[state], state_dic[x]))
				score = (state_dic[state][feature_idx]-state_dic[x][feature_idx])**2
	return score




# pp.pprint(state_dic)
indiaidx = list(state_dic.keys())
indiaidx = indiaidx.index('allindia')


for x in data:
	data[x].pop(indiaidx)

# for x in data:
# 	base = min(data[x])
# 	rage = max(max(data[x]) - base , 1)
# 	data[x] = [(y-base)/rage for y in data[x]]
#--------------------que 2 -------------------------------------------------
# pp.pprint(data)

for x in data:
	base = min(data[x])
	rage = max(max(data[x]) - base , 1)
	data[x] = [(y-base)/rage for y in data[x]]

distance = {}

india_vector = state_dic['allindia']


for x in state_dic:
	if(x <> "allindia"):
		distance[x] = np.linalg.norm(np.subtract(state_dic[x], india_vector))

# pp.pprint(distance)
distance = sorted(distance,key=distance.get)
min5 = distance[0:5]		
print("before normalising")
print(min5)

# normalising the vectors ---------------

norm_distance = {}
# pp.pprint(state_dic)
for x in state_dic:
	base = min(state_dic[x])
	rage = max(max(state_dic[x]) - base , 1)
	state_dic[x] = [(y-base)/rage for y in state_dic[x]]


india_vector = state_dic['allindia']

for x in state_dic:
	norm_distance[x] = np.linalg.norm(np.subtract(state_dic[x], india_vector))
# pp.pprint(norm_distance)
norm_distance = sorted(norm_distance,key=norm_distance.get)
min5 = norm_distance[1:6]		
print("after normalising")
print(min5)



# ---------------que 3 -------------

dfdata = pd.DataFrame.from_dict(data)
overall_corr = dfdata.corr()
c = 0
# for x in overall_corr:
# 	for y in range(len(overall_corr[x])):
# 		if(abs(overall_corr[x][y]) >= 0.9):
# 			c+=1

# print(c)


#-----------------que 4------------
for x in data:
	base = min(data[x])
	rage = max(max(data[x]) - base , 1)
	data[x] = [(y-base)/rage for y in data[x]]

states = list(state_to_region.keys())
s = {}

for x in range(0,len(data)):
	feature = data.keys()[x]
	s[feature] = 0
	m = 40
	while(m>0):
		m-=1
		idx = random.randint(0,36)
		if(states[idx] == 'allindia'):
			idx = random.randint(0,36)
		s[feature] = s[feature] - nearest_hit(states[idx],x) + nearest_miss(states[idx],x)

s = sorted(s.items(), key=lambda x:x[1])
best_two_overall = [x[0] for x in s[len(s)-2:]]
best_two_edu = []
best_two_eco = []
best_two_demo = []

print(best_two_eco)
print(best_two_overall)

for x in s:
	if(x[0] in eco and len(best_two_eco) < 2):
		best_two_eco.append(x[0])

for x in s:
	if(x[0] in edu and len(best_two_edu) < 2):
		best_two_edu.append(x[0])

for x in s:
	if(x[0] in demo and len(best_two_demo) < 2):
		best_two_demo.append(x[0])

plt = pyplot
fig, ax = plt.subplots(nrows=2, ncols=2)

feature1 = sorted(data[best_two_demo[0]])
feature2 = sorted(data[best_two_demo[1]])

ax[0][0].scatter(feature1, feature2, c = 'red', marker = '.')
ax[0][0].set_title('demography')

feature1 = sorted(data[best_two_edu[0]])
feature2 = sorted(data[best_two_edu[1]])

ax[0][1].scatter(feature1, feature2, c = 'red', marker = '.')
ax[0][1].set_title('Education')

feature1 = sorted(data[best_two_eco[0]])
feature2 = sorted(data[best_two_eco[1]])

ax[1][0].scatter(feature1, feature2, c = 'red', marker = '.')
ax[1][0].set_title('Economy')

feature1 = sorted(data[best_two_overall[0]])
feature2 = sorted(data[best_two_overall[1]])

ax[1][1].scatter(feature1, feature2, c = 'red', marker = '.')
ax[1][1].title.set_text('Total Data')


plt.show()
# plt1 = pyplot


# plt1.show()

# plt2 = pyplot
# plt2.scatter(feature1, feature2, c = 'red', marker = '.')
# plt2.xlabel('feature 1')
# plt2.ylabel('feature 2')
# plt2.title('demography')

# plt2.show()


# stats.probplot(feature1, dist="norm", plot=pylab)
# stats.probplot(feature2, dist="norm", plot=pylab)
# pylab.show()

