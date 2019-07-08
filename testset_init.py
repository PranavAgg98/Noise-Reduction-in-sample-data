import pandas as pd

data = pd.read_csv('./template_processed.csv')
data = data.dropna(subset=['industry'])
df = data.groupby('industry')
nulldata = data[data['industry'].isnull()]
nulltemp = data[data['template'].isnull()]

industry_list= df.describe()



intent = data['industry']
unique_intent = list(set(intent))

# for ui in unique_intent:
# 	temp = df.get_group(ui)
# 	name=str(ui)
# 	temp.to_csv('./TestSets/'+name+'TestSet.csv',index=False,header=True)

print len(unique_intent)
