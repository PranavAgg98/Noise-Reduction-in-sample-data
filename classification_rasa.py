import requests
import pandas as pd
import json
import nltk

data = pd.read_csv("./TestSets/ConsultingTestSet.csv") 

sentence = data['template']
print sentence[:5]

words = set(nltk.corpus.words.words())
def remove_non_english(sentence):
    new=[]
    for sent in sentence:
        new.append(" ".join(w for w in nltk.wordpunct_tokenize(sent) if w.lower() in words or not w.isalpha()))
    return new

sentence=remove_non_english(sentence)       
sent_seri = pd.Series(sentence)
data.template=sent_seri
data.dropna(subset=["template"],inplace=True)   
sentence = data['template']
print sentence[:8]

def intent_classifier(sentences): 
    intent_set=[]
    conf_set=[]
    i=0
    for s in sentences:
        if(i%100==0):
            print ("%d messages classified" % (i))
        i=i+1
        raw_data={'text':s}
        d = json.dumps(raw_data)
        try:
            r = requests.post('http://localhost:5005/model/parse',data=d)
            data =r.json()
            intent = data["intent"]["name"]
            conf = data["intent"]["confidence"]
            conf_set.append(conf)
            if (conf>0.5):
                intent_set.append(intent)
            else:
                intent_set.append(None)

        except Exception as e:
            print("error")      
    return intent_set,conf_set

intents,confidences=intent_classifier(sentence)

seri = pd.Series(intents)
data.insert(5,"Intent",seri,True)   
data.dropna(subset=["Intent"],inplace=True)
conf_seri = pd.Series(confidences)
data.insert(6,"Confidence",conf_seri,True)

data.to_csv('./ClassifiedTemplates/Consulting_classified.csv',index=False,header=True)
