import csv
import operator
import pprint as pp
from handle_missing_economy import handle_economy
from handle_missing_education import handle_education
from handle_missing_demography import handle_demography, alter, convert, notvalid


data = handle_demography()
data.update(handle_education())
data.update(handle_economy())

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
	state_to_region[y] = state_to_region.pop(x)
state_to_region['allindia'] = None
state_dic['allindia'] = []


state_list = state_dic.keys()
feature_list = []
for x in data:
	for j in range(0,len(data[x])):
		state_dic[state_list[j]].append(data[x][j])

pp.pprint(state_dic)		
