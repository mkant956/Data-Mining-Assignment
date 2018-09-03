from pandas import read_csv
import operator
import csv
import numpy as np
import pprint as pp
import re
import json

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


# data = read_csv('datagov/Economy/gross-domestic-product-gdp-current-price.csv',delimiter=',')


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

for x in state_dic:
	y = alter(x)
	state_dic[y] = state_dic.pop(x)


# intialising complete data
headers = []
cdata = {}
for x in state_dic:
	cdata[x] = []

#made cdata as completee daa append all in this

def handleData(file):
	data = read_csv('Economy/' + file,delimiter=',')

	check = {}
	size_item = len(data[data.keys()[0]])
	for [x,y] in sortedlist[1:]:
		y = alter(y)
		sum_dic[y] = [0]*size_item
		count[y] = [0]*size_item
		
	for x in cdata:
		check[x] = 0

	for x in data:
		y = alter(x)
		data[y] = data.pop(x)



	for x in data:
		y = convert(x)
		if(y in state_dic):
			sum_dic[state_dic[y]] = sum_dic[state_dic[y]] + np.where(np.isnan(data[x]),0,data[x])
			count[state_dic[y]] = count[state_dic[y]] + (np.isnan(data[x]) == False)

	for x in sum_dic:
		count[x] = np.where(count[x] == 0,1,count[x])
		sum_dic[x] = sum_dic[x] / count[x]


	for x in data:
		y = convert(x)
		if(y in state_dic):
			data[x] = np.where(np.isnan(data[x]),sum_dic[state_dic[y]], data[x])

	for x in data:
		if convert(x) in cdata:
			check[convert(x)] = 1
			cdata[convert(x)].extend(list(data[x]))

	for y in check:
		if(check[y] == 0):
			cdata[y].extend(sum_dic[state_dic[y]])

	headers.extend(data[data.keys()[0]])
	# for x in cdata:
	# 	if x not in data:
	# 		print(x)
	# 		cdata[x].extend(sum_dic[state_dic[x]]/count[state_dic[x]])


filelst = ['gross-domestic-product-gdp-constant-price.csv', 'gross-domestic-product-gdp-current-price.csv', 'state-wise-net-domestic-product-ndp-constant-price.csv', 'state-wise-net-domestic-product-ndp-current-price.csv']
# filelst = ['gross-domestic-product-gdp-constant-price.csv']#, 'gross-domestic-product-gdp-current-price.csv', 'state-wise-net-domestic-product-ndp-constant-price.csv', 'state-wise-net-domestic-product-ndp-current-price.csv']
for file in filelst:
	handleData(file)
# pp.pprint(cdata)
for x in cdata:
	print(x)
	print(cdata[x])
for x in headers:
	print(x)

