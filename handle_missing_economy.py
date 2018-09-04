from pandas import read_csv
import operator
import csv
import numpy as np
import pprint as pp
import pandas as pd
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
	elif(x == "all_indiagdp" or x == "all_indiandp"):
		return "allindia"
	else:
		return x
def notvalid(x):
	try:
		x = float(x)
		if(np.isnan(x)):
			return 1
		else:
			return 0
	except Exception as e:
		return 1


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
state_dic['allindia'] = None
state_list = state_dic.keys()
# intialising complete data
headers = []
edudata = {}

# cdata = {}
# for x in state_dic:
# 	cdata[x] = []

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

def handleData2(file):
	# data = read_csv('Education/' + file,delimiter=',')
	data = pd.read_csv('Economy/' + file, header=0)
	cdata = {}

	keys = data.keys()
	data = (data.values)
	for i in range(0,len(data)):
		try:
			float(data[i,0])
		except Exception as e:
			cdata[file[:len(file)-4] + data[i,0] + data[i,1]] = [np.nan]*37

	states = list(keys)
	for i in range(0, len(states)):
		states[i] = alter(states[i])


	for i in range(0,len(data)-1):
		for j in range(2,len(data[i])):
			idx = state_list.index(convert(states[j]))
			cdata[file[:len(file)-4] +data[i,0] + data[i,1]][idx] = data[i][j]

	for x in cdata:
		for y in range(0,len(cdata[x])):
			if(notvalid(cdata[x][y])):
				avg = 0
				region = state_dic[convert(state_list[y])]
				c = 0
				if(region == None):
					for z in range(0,len(cdata[x])):
						if(not notvalid(cdata[x][z])):
							avg += float(cdata[x][z])
							c+=1	
				else:				
					for z in range(0,len(cdata[x])):
						if(state_dic[convert(state_list[z])] == region and not notvalid(cdata[x][z]) ):
							avg += float(cdata[x][z])
							c+=1
				cdata[x][y] = float(avg)/(1 if c == 0 else c)
	
	# pp.pprint(cdata)
	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(np.isnan(y)):
	# 			print(x)

	edudata.update(cdata)



filelst = ['gross-domestic-product-gdp-constant-price.csv',
 'gross-domestic-product-gdp-current-price.csv', 
 'state-wise-net-domestic-product-ndp-constant-price.csv', 
 'state-wise-net-domestic-product-ndp-current-price.csv']
for file in filelst:
	handleData2(file)
pp.pprint(len(edudata))
