import plotly.io as pio
from datetime import datetime
import pandas as pd
import os
import pickle
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import helpers


def count_keywords(keylist, df):
    my_dict = {}
    for key in keylist:
        df_key1 = df[df.comment.str.contains(key)]
        df_key2 = df[df.translated.str.contains(key)]
        df_key = df_key1.append(df_key2)
        df_key.drop_duplicates(inplace=True)
        my_dict[key] = df_key.shape[0]
        
    return my_dict

os.chdir('../data')

# LOAD DATA
df_comments = pd.read_csv("./cleaned_data/facebook_cleaned.csv")

# THREAT
all_threat = {'burn', 'crime', 'criminal', 'dead', 'death', 'deserve', 'die', 'hell', 'inferno', 'infierno', 'jail',
              'karma', 'kill', 'kys', 'matar', 'morir', 'morire', 'muere', 'muerete', 'muerta', 'muerte', 'murder',
              'pagar', 'pay', 'prigione', 'prisión', 'prison', 'punish', 'ад', '死ね'}

df_threat1 = df_comments[df_comments.comment.str.contains('|'.join(all_threat))]
df_threat2 = df_comments[df_comments.translated.str.contains('|'.join(all_threat))]
df_threat = df_threat1.append(df_threat2)
df_threat.drop_duplicates(inplace=True)

# KILL & DEATH
death_kill = {'death', 'muerte', 'die', '死ね', 'morire', 'morir', 'muere', 'muerete', 'kill', 'matar', 
              'murder', 'dead', 'muerta', 'kys'}

df_death1 = df_comments[df_comments.comment.str.contains('|'.join(death_kill))]
df_death2 = df_comments[df_comments.translated.str.contains('|'.join(death_kill))]
df_death = df_death1.append(df_death2)
df_death.drop_duplicates(inplace=True)

# BURN & HELL
burn_hell = {'hell', 'inferno', 'infierno', 'ад', 'burn'}

df_burn1 = df_comments[df_comments.comment.str.contains('|'.join(burn_hell))]
df_burn2 = df_comments[df_comments.translated.str.contains('|'.join(burn_hell))]
df_burn = df_burn1.append(df_burn2)
df_burn.drop_duplicates(inplace=True)

# CRIME & JAIL
crime_jail = {'pay', 'pagar', 'punish', 'crime', 'criminal', 'jail', 'prison', 'prigione', 'prisión',
              'deserve', 'karma'}

df_crime1 = df_comments[df_comments.comment.str.contains('|'.join(crime_jail))]
df_crime2 = df_comments[df_comments.translated.str.contains('|'.join(crime_jail))]
df_crime = df_crime1.append(df_crime2)
df_crime.drop_duplicates(inplace=True)

# NEGATIVE TEXT
# To Load the dictionary of negative text    
with open('./cleaned_data/negative_text.pkl', 'rb') as f:
    neg_dict = pickle.load(f) 
    neg_text = set(neg_dict.keys())
    
neg_text = neg_text | {'narcissist', 'cancelamber', 'cancel amber', 'amber sucks', 'hate amber heard', 'scamber', 
                       'boycott amber', 'amber heard sucks', "i remind that amber heard craped on jonny depp's bed",
                       'amber heard is trash', 'deleteamber', 'delete amber', 'amber heard is a monster'}
      
hate_speech = {'victim', 'fuck', 'ambich', 'abuser', 'liar', 'jail', 'prison', 'deserve', 'digger',
               'bullies', 'bitch', 'crazy', 'psycho', 'not a victim', 'lies', 'turd', 'whitch'}
    
    
neg_text = neg_text | all_threat | hate_speech       
   
df_hate1 = df_comments[df_comments.comment.str.contains('|'.join(neg_text))]
df_hate2 = df_comments[df_comments.translated.str.contains('|'.join(neg_text))]
df_hate = df_hate1.append(df_hate2)
df_hate.drop_duplicates(inplace=True)


# COUNTS
n_all = df_comments.shape[0]
n_threat = df_threat.shape[0]
# notthreat = n_all - n_threat
n_hate = df_hate.shape[0] - n_threat
nothate = n_all - n_hate - n_threat
n_death = df_death.shape[0]
n_burn = df_burn.shape[0]
n_crime = df_crime.shape[0]
    

threat_dict = helpers.count_keywords(all_threat|{'jail','prison','deserve','burn'}, df_comments)
threat_counts = pd.DataFrame(threat_dict, index=['count'])
threat_counts = threat_counts.T.reset_index().rename(columns={'index':'keyword'})
threat_counts.sort_values('count', ascending=False, inplace=True)

mycolors1=[]
for key in threat_counts['keyword'].head(15):
    if key in death_kill:
        mycolors1.append('#E45756')
    elif key in burn_hell:
        mycolors1.append('#F58518')
    else:
        mycolors1.append('#BAB0AC')

mycolors2=[]        
for key in threat_counts['keyword'][15:].head(15):  
    if key in death_kill:
        mycolors2.append('#E45756')
    elif key in burn_hell:
        mycolors2.append('#F58518')
    else:
        mycolors2.append('#BAB0AC')
    
    
    
    
    
    
    
    

