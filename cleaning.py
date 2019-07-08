import re, string
import nltk
import contractions
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer	
import pandas as pd


data = pd.read_csv('data/templates - templates.csv')

data = data.astype({'template' : str, 'accountId' : str})
len1=len(data)
#	data = data.dropna(subset=['industry'])
sentence = data['template']

#sentence = filter(None,basedata)
# print sentence[10:30]
intent = data['industry']

location = data['country']
unique_intent = list(set(intent))
unique_loc = list((set(location)))
#print unique_loc
data.reset_index(drop =True,inplace=True)
#print data[:10]

def cleaning(sentence):
	new = []
	for s in sentence:
		s = s.replace(r"\n","")
		s = s.replace(r"%s","")
		s = s.replace(r"%d","")
		#s = s.replace(r"%c","")	
  		sf = contractions.fix(s)
  		clean = re.sub(r'[^ a-z A-Z 0-9]', " ", sf)
  		clean = clean.lower()
  		new.append(clean)
	return new
	
clean_sentence = cleaning(sentence)
#print clean_sentence[:10]
print "Data Cleaned.."
def remove_stopwords(sent):
	stopwords_en = set(stopwords.words('english'))
	rm_stopwords = []
	for s in sent:
		rm_stopwords.append(' '.join(w for w in nltk.word_tokenize(s) if w not in stopwords_en))
	return rm_stopwords

clean_sentence = remove_stopwords(clean_sentence)

print "Stop Words removed"
def lemmat(sent):	
	lemmatizer = WordNetLemmatizer()
	lemma = []
	for s in sent:
		words = nltk.word_tokenize(s)
		res_words = []
		for w in words:
			lem_word = lemmatizer.lemmatize(w,'v')
			res_words.append(lem_word)
			# if lem_word != w:
			# 	print '{} -> {}'.format(w,lem_word)	
		lemma.append(' '.join(res_words))
	return lemma
	

clean_sentence = lemmat(clean_sentence)
print "Lemmatization done"
series_sen = pd.Series(clean_sentence)
data.template=series_sen

data.to_csv('stopwords.csv',index=False,header=False)
data.drop_duplicates(subset ="template", keep = 'first', inplace = True) 
#print len(data)
data.dropna(subset=["template"], inplace = True)
#print len(data)
len2=len(data)
rem=len1-len2
print "{} messages removed".format(rem)	
# print "Unique Intents:"
# for u in unique_intent:
# 	print u
# df = data.groupby('industry')
# print df.describe().head()
data.to_csv('template_processed.csv',index=False,header=True)

#print data[:10]