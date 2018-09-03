from pandas import read_csv
import operator
import csv
import numpy as np
import pprint as pp
import re

def alter(x):
	x = re.sub(r'\d+', '', x)
	x = x.replace(' ','')
	x = x.lower()

	return x

def convert(x):
	if(x == "andaman&nicobarislands"):
		return "a&nislands"
	elif(x == "delhi"):
		return "nctofdelhi"
	else:
		return x

# region = read_csv('regions.csv',delimiter = ',')
with open('regions.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	sortedlist = sorted(csv_reader, key= operator.itemgetter(1))
file = 'gross-domestic-product-gdp-constant-price.csv'
file = 'gross-domestic-product-gdp-current-price.csv'
file = 'state-wise-net-domestic-product-ndp-constant-price.csv'
file = 'state-wise-net-domestic-product-ndp-current-price.csv'
data = read_csv('Economy/' + file,delimiter=',')
# data = read_csv('datagov/Economy/gross-domestic-product-gdp-current-price.csv',delimiter=',')
# data = read_csv('datagov/Economy/state-wise-net-domestic-product-ndp-constant-price.csv',delimiter=',')
# data = read_csv('datagov/Economy/state-wise-net-domestic-product-ndp-current-price.csv',delimiter=',')

size_item = len(data[data.keys()[0]])

# compute avg. for each region

mean_dic = {}
sum_dic = {}
state_dic = {}
count = {}


for [x,y] in sortedlist[1:]:
	state_dic[x] = y
	if y in mean_dic:
		mean_dic[y].append(x)
	else:
		mean_dic[y] = [x]


for [x,y] in sortedlist[1:]:
	y = alter(y)
	sum_dic[y] = [0]*size_item
	count[y] = [0]*size_item

for x in state_dic:
	y = alter(x)
	state_dic[y] = state_dic.pop(x)
	# count[y] = count.pop(x)

for x in data:
	y = alter(x)
	data[y] = data.pop(x)


# pp.pprint(state_dic)
# pp.pprint(data.keys())

for x in data:
	y = convert(x)
	# print(x,y)
	if(y in state_dic):
		sum_dic[state_dic[y]] = sum_dic[state_dic[y]] + np.where(np.isnan(data[x]),0,data[x])
		count[state_dic[y]] = count[state_dic[y]] + (np.isnan(data[x]) == False)


# print(sum_dic)
# print(count)
for x in sum_dic:
	count[x] = np.where(count[x] == 0,1,count[x])
	# print(count[x])
	sum_dic[x] = sum_dic[x] / count[x]

# print(sum_dic)

for x in data:
	y = convert(x)
	if(y in state_dic):
		data[x] = np.where(np.isnan(data[x]),sum_dic[state_dic[y]], data[x])

# print(data)
with open('newEconomy/' + file, 'w') as f:
    data.to_csv(f, header=True)

