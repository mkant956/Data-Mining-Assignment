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
	elif(x == "chhatisgarh"):
		return "chhattisgarh"
	elif(x == "uttrakhand" or x == "uttaranchal"):
		return "uttarakhand"
	elif(x == "pondicherry"):
		return "puducherry"
	elif(x == "india"):
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
	print(states)
	# to check NR remaining or not

	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(y == 'NR'):
	# 			print(x,y)

def handleData3(file):
	# data = read_csv('Education/' + file,delimiter=',')
	data = pd.read_csv('Education/' + file, header=0)
	cdata = {}

	keys = data.keys()
	data = (data.values)
	if(file == 'gross-enrolment-ratio-higher-education.csv'):
		year = np.array(data[:,0].T)
	else:
		year = np.array(data[:,1].T)

	for x in keys[2:]:
		for y in np.unique(year):
			cdata[file+x+y] = []

	# print(keys)
	# print(year)
	if(file == 'gross-enrolment-ratio-higher-education.csv'):
		states = data[:,1]
	else:
		states = data[:,0]

	for i in range(0,len(data)):
		if(alter(states[i]) == 'tripura' and (year[i] in ['2010-11','2011-12'])):
			for j in range(2,len(data[i])):
				cdata[file+keys[j]+year[i]].append(np.nan)
		for j in range(2,len(data[i])):
			cdata[file+keys[j] + year[i]].append(data[i][j])

	for i in range(0, len(states)):
		states[i] = alter(states[i])
	states = np.unique(states)
	for x in cdata:
		for y in range(0,len(cdata[x])):
			if(notvalid(cdata[x][y])):
				avg = 0
				region = state_dic[convert(states[y])]
				c = 0
				if(region == None):
					for z in range(0,len(cdata[x])):
						if(not notvalid(cdata[x][z])):
							avg += float(cdata[x][z])
							c+=1	
				else:				
					for z in range(0,len(cdata[x])):
						if(state_dic[convert(states[z])] == region and not notvalid(cdata[x][z]) ):
							avg += float(cdata[x][z])
							c+=1
				cdata[x][y] = float(avg)/(1 if c == 0 else c)
	
	# pp.pprint(cdata)
	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(np.isnan(y)):
	# 			print(x)

	edudata.update(cdata)
	print(states)
	
	# to check NR remaining or not

	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(y == 'NR'):
	# 			print(x,y)

def handleData4(file):
	# data = read_csv('Education/' + file,delimiter=',')
	data = pd.read_csv('Education/' + file, header=0)
	cdata = {}

	keys = data.keys()
	data = (data.values)

	for x in keys[2:]:
		cdata[file+x] = []

	states = data[:,1]

	for i in range(0, len(states)):
		states[i] = alter(states[i])
	states = np.array(np.unique(states))
	for i in range(0,len(data)):
		if(alter(states[i]) == 'tripura' and 'telangana' not in states):
			states = np.insert(states, i, 'telangana')
			for j in range(2,len(data[i])):
				cdata[file+keys[j]].append(np.nan)
		for j in range(2,len(data[i])):
			cdata[file+keys[j]].append(data[i][j])


	for x in cdata:
		for y in range(0,len(cdata[x])):
			if(notvalid(cdata[x][y])):
				avg = 0
				region = state_dic[convert(states[y])]
				c = 0
				if(region == None):
					for z in range(0,len(cdata[x])):
						if(not notvalid(cdata[x][z])):
							avg += float(cdata[x][z])
							c+=1	
				else:				
					for z in range(0,len(cdata[x])):
						if(state_dic[convert(states[z])] == region and not notvalid(cdata[x][z]) ):
							avg += float(cdata[x][z])
							c+=1
				cdata[x][y] = float(avg)/(1 if c == 0 else c)
	
	# pp.pprint(cdata)
	# pp.pprint(cdata)
	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(np.isnan(y)):
	# 			print(x)

	edudata.update(cdata)
	print(states)	
	# to check NR remaining or not

	# for x in cdata:
	# 	for y in cdata[x]:
	# 		if(y == 'NR'):
	# 			print(x,y)


filelst1 = [
'drop-out-rate.csv',
'percentage-schools-boys-toilet.csv',
'percentage-schools-computers.csv',
'percentage-schools-drinking-water.csv',
'percentage-schools-electricity.csv',
'percentage-schools-girls-toilet.csv'
]
filelst2 = [
'gross-enrolment-ratio-higher-education.csv',
'gross-enrolment-ratio-schools.csv'
]

filelst3 = [
'literacy-rate-7-years.csv'
]

for file in filelst1:
	handleData2(file)

# for file in filelst2:
# 	handleData3(file)


# for file in filelst3:
# 	handleData4(file)

# pp.pprint(edudata)

print(len(edudata))
# for x in cdata:
# 	print(x)
# 	print(cdata[x])
# for x in headers:
# 	print(x)

