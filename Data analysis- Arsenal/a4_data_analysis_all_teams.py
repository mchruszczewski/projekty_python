import pandas as pd
import numpy as np
import datetime as d
import requests
import re 
from a1_scrapping_data import *
from a2_extra_useful_columns_functions  import *

#all teams defense and offense comparison

all_teams_def= pd.DataFrame()

for i in seasons_dict:
    df= seasons_dict[i]['general_table']
    df= df.loc[:,['Rk','Squad','xGA/90','GA']]
    df["Seasons"]= i
    all_teams_def= pd.concat([all_teams_def,df], axis=0)
    all_teams_def= all_teams_def.reset_index(drop= True)

all_teams_def= all_teams_def.loc[all_teams_def['Seasons']!='2022-2023']

all_teams_off= pd.DataFrame()

for i in seasons_dict:
    df= seasons_dict[i]['general_table']
    df= df.loc[:,['Rk','Squad','xG/90','GF']]
    df["Seasons"]= i
    all_teams_off= pd.concat([all_teams_off,df], axis=0)
    all_teams_off= all_teams_off.reset_index(drop= True)

all_teams_off= all_teams_off.loc[all_teams_off['Seasons']!='2022-2023']