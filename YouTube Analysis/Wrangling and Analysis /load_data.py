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

# https://stackoverflow.com/questions/38616077/live-stdout-output-from-python-subprocess-in-jupyter-notebook
# https://stackoverflow.com/questions/51310767/activating-conda-environment-within-python
# https://stackoverflow.com/questions/64771560/how-to-activate-a-conda-environment-within-a-python-script

# import subprocess
# subprocess.run(['/Users/mnagy99/opt/anaconda3/envs/nlp/bin/python3.8',
#                 '/Users/mnagy99/jupyter/AH/YouTube_Bot_Analysis/SNA-AH-Case-YouTube/YouTube Analysis/load_data.py'])

# https://stackoverflow.com/questions/24719368/syntaxerror-non-default-argument-follows-default-argument/39942121

def count_keywords(keylist, df):
    my_dict = {}
    for key in keylist:
        df_key = df[df.text.str.contains(key)]
        my_dict[key] = df_key.shape[0]       
    return my_dict

os.chdir('../../Filtered Data/comments_cleaned')


# LOAD DATA
df_comments = pd.read_csv("comments_cleaned_zipped.csv", compression='zip',
                          low_memory=False, lineterminator='\n')

df_comments["p_dtime"] = pd.to_datetime(df_comments["p_dtime"])
df_comments["date"] = pd.to_datetime(df_comments["date"])
df_comments["u_dtime"] = pd.to_datetime(df_comments["u_dtime"])
df_comments = df_comments.sort_values('p_dtime')

df_comments.text.fillna('isnan', inplace=True)

pos_text = {'love amber', 'stand with amber', 'standwithamber', 'support amber', 'supportamber', 'justiceforamber', 
            'johnnydeppisawifebeater', 'boycottwomenbeaters', 'wearewithamber', 'justice for amber', 
            'istandwithamber','wearewithyouamber', 'amber heard is innocent', 'amber is innocent','support her'}
# ValueError: Cannot mask with non-boolean array containing NA / NaN values
df_pos = df_comments[df_comments.text.str.contains('|'.join(pos_text))]

# Those users were checked and did not find negative comments
checked_set = {'eHacker', 'Stevie J Raw', 'DarthN3ws', "Nerdette's NewsStand", 'Sunshine', 'Binge Central',
               'Abbey Sharp', 'ko 3', 'Mary Shephard', 'Madison Beer', 'Baby Bunny', 'LadyDominion',
               'Tom Harlock', 'Gus Johnson', 'Mr. Bruhhh', 'Crypto Info 2', 'demi demi', '8-Bit Tex', 'Ty Y', 
               'Incredibly Average', 'DELCARAJO TV', 'Flashback FM','Funeral bug', 'Stranger In the Alps', 
               "Nerdette's NewsStand"}

remove_users = checked_set | set(df_pos.username)


# THREAT
# KYS is an internet acronym standing for “kill yourself
all_threat = {'burn', 'crime', 'criminal', 'amberfbi', 'dead', 'death', 'deserve', 'die', 'hell', 'inferno', 'infierno', 'jail',
              'karma', 'kill', 'kys', 'matar', 'morir', 'morire', 'muere', 'muerete', 'muerta', 'muerte', 'murder',
              'pagar', 'pay', 'prigione', 'prisión', 'prison', 'punish', 'ад', '死ね'}

# all_threat = {'deathto', "death to fascists", "death to mera", "death to all narcissistic", "social death to", 
#               "professional death", "death to femnazis", "death to those people", ' go die', 'die cunt', 
#               'kill heard', 'kill amber', 'kill her', 'kys fuck you amber', 'deserve', 'jail', 'prison', 
#               'pay for her crimes', 'if she wants assault she well get it', 'death to a turd', 'amberfbi',
#               'death to anybody not supporting johnny', 'kiss of death', 'death amber', 'go kill yourselves',
#               'kill all the people who disliked', 'to hell', 'tohell', 'in hell', 'inhell', "who the hell is",
#               'burn her', 'burn turd', 'her burn', 'isacriminal', 'amberfbi', 'pay for her crime'}

df_threat = df_comments[df_comments.text.str.contains('|'.join(all_threat))]

# exclude all the users with positive comments
df_threat = df_threat[~df_threat.username.isin(remove_users)]


# # KILL & DEATH
death_kill = {'death', 'muerte', 'die', '死ね', 'morire', 'morir', 'muere', 'muerete', 'kill', 'matar', 
              'murder', 'dead', 'muerta', 'kys'}

# death_kill = {'deathto', "death to fascists", "death to mera", "death to all narcissistic", "social death to", 
#               "professional death", "death to femnazis", "death to those people", ' go die', 'die cunt', 
#               'kill heard', 'kill amber', 'kill her', 'kys fuck you amber', 'death amber', 'go kill yourselves',
#               'kill all the people who disliked', 'deserve', 'jail', 'prison', 'death to a turd',
#               'death to anybody not supporting johnny', 'kiss of death',}

df_death = df_threat[df_threat.text.str.contains('|'.join(death_kill))]


# BURN & HELL
burn_hell = {'hell', 'inferno', 'infierno', 'ад', 'burn'}

df_burn = df_threat[df_threat.text.str.contains('|'.join(burn_hell))]


# CRIME & JAIL
crime_jail = {'pay', 'pagar', 'punish', 'crime', 'criminal', 'jail', 'prison', 'prigione', 'prisión',
              'deserve', 'karma', 'amberfbi'}

df_crime = df_threat[df_threat.text.str.contains('|'.join(crime_jail))]


# NEGATIVE TEXT
# To Load the dictionary of negative text    
with open('negative_text.pkl', 'rb') as f:
    neg_dict = pickle.load(f) 
    neg_text = set(neg_dict.keys())
    
neg_text = neg_text | {'narcissist', 'cancelamber', 'cancel amber', 'amber sucks', 'hate amber heard', 'scamber', 
                       'boycott amber', 'amber heard sucks', "i remind that amber heard craped on jonny depp's bed",
                       'amber heard is trash', 'deleteamber', 'delete amber', 'amber heard is a monster'}
      
hate_speech = {'victim', 'fuck', 'ambich', 'abuser', 'liar', 'jail', 'prison', 'deserve', 'digger',
               'bullies', 'bitch', 'crazy', 'psycho', 'not a victim', 'lies', 'turd', 'whitch'}
    
    
neg_text = neg_text | all_threat | hate_speech       
   
df_hate = df_comments[df_comments.text.str.contains('|'.join(neg_text))]

# exclude all the users with positive comments
df_hate = df_hate[~df_hate.username.isin(remove_users)]



# COUNTS
n_all = df_comments.shape[0]
n_threat = df_threat.shape[0]
# notthreat = n_all - n_threat
n_hate = df_hate.shape[0] - n_threat
nothate = n_all - n_hate - n_threat
n_death = df_death.shape[0]
n_burn = df_burn.shape[0]
n_crime = df_crime.shape[0]
    

threat_keys = {'burn', 'crime', 'criminal', 'amberfbi', 'dead', 'death', 'deserve', 'die', 'hell', 'jail', 'karma', 'kill',
               'kys', 'murder', 'pay', 'prison', 'punish'}
threat_dict = count_keywords(threat_keys, df_comments)
threat_counts = pd.DataFrame(threat_dict, index=['count'])
threat_counts = threat_counts.T.reset_index().rename(columns={'index':'keyword'})
threat_counts.sort_values('count', ascending=False, inplace=True)

mycolors1=[]
for key in threat_counts['keyword'].head(17):
    if key in death_kill:
        mycolors1.append('#E45756')
    elif key in burn_hell:
        mycolors1.append('#F58518')
    else:
        mycolors1.append('#BAB0AC')

# mycolors2=[]        
# for key in threat_counts['keyword'][15:].head(15):  
#     if key in death_kill:
#         mycolors2.append('#E45756')
#     elif key in burn_hell:
#         mycolors2.append('#F58518')
#     else:
#         mycolors2.append('#BAB0AC')
        


        
# # Threat Comments In Other Languages
# threat_others = {'pagar', 'matar', 'muerte', 'morir', 'infierno', 'muere', 'muerta', 'inferno', 'morire', 'prigione'}
# df_threat_others = df_threat[df_threat.text.str.contains('|'.join(threat_others))]

# # Add A Language-Detection Column
# import icu
# from polyglot.detect.base import logger as polyglot_logger
# polyglot_logger.setLevel("ERROR")

# def det(x):
#     try:
#         poly_obj = Detector(x, quiet=True)
#         lang = icu.Locale.getDisplayName(poly_obj.language.locale)
#     except:
#         lang = 'Other'
#     return lang

# df_threat_others['language'] = df_threat_others.text.apply(lambda x: det(x)) 

# # Add A Translation Column
# import mtranslate

# def translate(x):
#     try:
#         translated = mtranslate.translate(x,"en","auto")
#     except:
#         translated = 'not_translated'
#     return translated

# df_threat_others['translated'] = df_threat_others.text.apply(lambda x: translate(x))   
    
    
df_threat_others = pd.read_csv("other_languages.csv", low_memory=False, lineterminator='\n')

df_threat_others["p_dtime"] = pd.to_datetime(df_threat_others["p_dtime"])
df_threat_others["date"] = pd.to_datetime(df_threat_others["date"])
df_threat_others["u_dtime"] = pd.to_datetime(df_threat_others["u_dtime"])
df_threat_others = df_threat_others.sort_values('p_dtime') 
    
    
    
    

