
import pandas as pd


data = pd.read_csv('consulting_processed.csv',names=['template','industry'])

data_sort = data.sort_values('industry')

print data_sort[:5]

intent = data['industry']

unique_intent = list(set(intent))
#data.to_csv('finance_processed.csv',index=False,header=True)


temp=[]
f = open("nlu_consulting.md", "a")
for u in unique_intent:
	for d in data:
		temp = data[data['industry'] == u]
		temp_list=temp['template']
	f.write("## intent:%s \n"%(u))
	for l in temp_list:
		f.write("- %s\n"%(l))
	f.write("\n")
	

