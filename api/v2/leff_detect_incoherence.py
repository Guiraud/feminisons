
# coding: utf-8

# In[26]:


import spacy
from spacy import displacy
import pandas as pd
import datetime
import time
import psycopg2
import io
from spacy_lefff import LefffLemmatizer, POSTagger
from sqlalchemy import create_engine
from konnect_polen import *
host='localhost:5433'
engine = create_engine('postgresql://'+configuration_db_user_localhost+':'+configuration_db_pass_localhost+'@'+host+'/mehdi.guiraud',encoding='utf-8')
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def noun_gender(tag):
    if 'Fem' in tag:
        return 'Fem'
    elif 'Masc' in tag:
        return 'Masc'
    else:
        return None		
print("nlp")
nlp = spacy.load('fr')
pos = POSTagger()
print("nlp_2")
french_lemmatizer = LefffLemmatizer(after_melt=True)
nlp.add_pipe(pos, name='pos', after='parser')
nlp.add_pipe(french_lemmatizer, name='lefff', after='pos')
doc = nlp(u"Les policiers qui portaient le suspect sont tombés.")
doc = nlp(u"La Femme naît libre et demeure égale à l'homme en droits.")
doc = nlp(u"Elle est jeune, c'est une femme, rapporteur auprès du Conseil d'État.")
doc = nlp(u"Elle est femme et policier.")
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.label_, chunk.root.text)
for token in doc:
    #print("{0}/{1}({2}) <--{3}-- {4}/{5}".format(token.text, token.tag_,token._.lefff_lemma, token.dep_, token.head.text, token.head.tag_))
    #print("\n"+token.head.tag_,token.tag_)
    a = [token.head.tag_,token.tag_]
    #print(a)
    if any("Fem" in s for s in a) and any("Masc" in s for s in a):
        print("{0}({1}) <--{2}({3})".format(token.tag_,noun_gender(token.tag_), token.head.tag_,noun_gender(token.head.tag_)))
        print("Détection : {0}/{1}({2}) <--{3}-- {4}/{5}".format(token.text, token.tag_,token._.lefff_lemma, token.dep_, token.head.text, token.head.tag_))
#    print(d.text, d.pos_, d._.melt_tagger, d._.lefff_lemma, d.tag_, d.lemma_,d.dep_)
#    texte={'text':d.text,'pos_':d.pos_,'melt_tagger':d._.melt_tagger,'lefff_lemma':d._.lefff_lemma,'tag_':d.tag_,'lemma_':d.lemma,'dep_':d.dep_}
    #print(texte)
    df_texte=pd.DataFrame({'timestamp':pd.Timestamp(st),'text':token.text,'pos_':token.pos_,'melt_tagger':token._.melt_tagger,'lefff_lemma':token._.lefff_lemma,'tag_':token.tag_,'lemma_':token.lemma,'dep_':token.dep_}, index=[0])
    #df_texte=pd.read_csv(io.StringIO('\n'.join(texte)), delim_whitespace=True)
    #print(df_texte)
    df_texte.to_sql('phrase',engine, if_exists='append', index=False)
#displacy.render(doc, style='dep', jupyter=True)
#displacy.render(doc, style='ent', manual=True)

    
