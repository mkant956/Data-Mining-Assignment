from pandas import read_csv
import pandas as pd
import operator
import csv
import numpy as np
import pprint as pp
import re
import json

import pdb

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
	elif(x == "dadra&nagarhaveli"):
		return "d&nhaveli"
	elif(x == "jammuandkashmir"):
		return "jammu&kashmir"
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
# print(state_dic)
state_dic['allindia'] = None

# intialising complete data
headers = []
edudata = {}
# for x in state_dic:
# 	edudata[x] = []

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

def handleData2(file):
	# data = read_csv('Education/' + file,delimiter=',')
	data = pd.read_csv('Education/' + file, index_col=0, header=None).T
	states = data.keys()[1:]
	data = data.values
	# print(data)
	# print(len(data))
	# print(len(data[0]))
	# print(states.values)
	tdata = []
	j = 1
	states = list(states)
	for i in range(0,len(states)):
		states[i] = alter(states[i])
	cdata = {}
	# # print(data[0][4], states[4])
	# print(len(states))
	# quit()
	for i in range(1,len(data)):
		cdata[file + data[i][0] + data[0][j]]  =[]
		# print(file +data[i][0] + data[0][j])
		j+=1
		cdata[file+data[i][0] + data[0][j]]  =[]
		# print(file +data[i][0] + data[0][j])
		j+=1
		cdata[file+data[i][0] + data[0][j]]  =[]
		# print(file +data[i][0] + data[0][j])
		j+=1
	# pp.pprint(cdata)
	# print(len(data[0]))

	# for i in range(1,len(data)):
	# 	if

	for i in range(1,len(data)):
		# print(states[i])
		for j in range(1, len(data[i])):
			if(states[j-1] == 'telangana'):
				if(data[0][j] == '2013-14' and file == 'drop-out-rate.csv'):
					cdata[file+data[i][0]+data[0][j-3]].append('NR')
				elif(data[0][j] == '2014-15' and file != 'drop-out-rate.csv'):
					cdata[file+data[i][0]+data[0][j-3]].append('NR')
				

			cdata[file + data[i][0]+data[0][j]].append(data[i][j])

	# pp.pprint(cdata)
	states = list(set(states))
	for x in cdata:
		# print(len(cdata[x]))
		for y in range(0,len(cdata[x])):
			if(cdata[x][y] == 'NR'):
				# print(states[y], state_dic[convert(states[y])])
				avg = 0
				region = state_dic[convert(states[y])]
				c = 0
				if(region == None):
					for z in range(0,len(cdata[x])):
						if(cdata[x][z] <> 'NR' ):
							avg += float(cdata[x][z])
							c+=1	
				else:				
					for z in range(0,len(cdata[x])):
						if(state_dic[convert(states[z])] == region and cdata[x][z] <> 'NR' ):
							avg += float(cdata[x][z])
							c+=1
				cdata[x][y] = float(avg)/(1 if c == 0 else c)
	
	edudata.update(cdata)
	# for x in edudata:
	# 	print(len(cdata[x]))
	
	# to check NR remaining or not

	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(y == 'NR'):
	# 			print(x,y)

# filelst = ['drop-out-rate.csv']
# filelst = [
# 'drop-out-rate.csv',
# 'gross-enrolment-ratio-higher-education.csv',
# 'gross-enrolment-ratio-schools.csv',
# 'literacy-rate-7-years.csv',
# 'percentage-schools-boys-toilet.csv',
# 'percentage-schools-computers.csv',
# 'percentage-schools-drinking-water.csv',
# 'percentage-schools-electricity.csv',
# 'percentage-schools-girls-toilet.csv'
# ]
filelst = [
'drop-out-rate.csv',
'percentage-schools-boys-toilet.csv',
'percentage-schools-computers.csv',
'percentage-schools-drinking-water.csv',
'percentage-schools-electricity.csv',
'percentage-schools-girls-toilet.csv'
]


for file in filelst:
	handleData2(file)



pp.pprint(edudata)
print(len(edudata))
# for x in cdata:
# 	print(x)
# 	print(cdata[x])
# for x in headers:
# 	print(x)

