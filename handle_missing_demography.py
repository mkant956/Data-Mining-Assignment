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
	elif(x == "all_indiagdp" or x == "all_indiandp" or x == "india"):
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
	# data = read_csv('Education/' + file,delimiter=',')
	data = pd.read_csv('Demography/' + file, header=0)
	cdata = {}

	keys = list(data.keys())
	data = (data.values)
	for i in range(2,len(keys)):
		cdata[file[:len(file)-4] + keys[i]] = [np.nan]*37

	states = data[:,1]
	for i in range(0, len(states)):
		states[i] = alter(states[i])

	for i in range(0,len(data)):
		for j in range(2,len(data[i])):
			idx = state_list.index(convert(states[i]))
			cdata[file[:len(file)-4] + keys[j] ][idx] = data[i][j]
	
	# pp.pprint(cdata)

	edudata.update(cdata)



filelst = ['child-sex-ratio-0-6-years.csv',
 'decadal-growth-rate.csv', 
 'sex-ratio.csv']
for file in filelst:
	handleData(file)
pp.pprint(len(edudata))
