import pandas as pd
import numpy as np
import datetime as d
from bs4 import BeautifulSoup
import requests
import re 
from a1_scrapping_data import *
from a2_extra_useful_columns_functions  import *


#Part 1: champions comparison

#create dictionary with seasons and champions names
champions_dict= {}
for i in seasons_dict:
    champions_dict[i]=seasons_dict[i]['general_table']['Squad'].iloc[0]

#general_table_champions table with all champions from 2017- 2022
general_table_champions= pd.DataFrame(columns=list(seasons_dict[list_of_seasons[-1]]['general_table'].columns))
for i in champions_dict:
    season_champ= seasons_dict[i]['general_table'].iloc[0]
    general_table_champions.loc[len(general_table_champions)] =  season_champ
general_table_champions=general_table_champions.reset_index(drop= True)

        
#defensive_stats_champions_table
table= 'def_actions'
def_columns= pd.MultiIndex.from_tuples(list((seasons_dict[list_of_seasons[1]]['def_actions'].columns)))
champions_table_def= pd.DataFrame(columns= def_columns)
for i in champions_dict:
    team= champions_dict[i]
    season= i
    df= team_tables(team, table, season)
    champions_table_def= pd.concat([champions_table_def, df]).reset_index(drop= True)

# find the best dfensive teams in each season based on xGA and best offensive team based on xG and GF
columns= list(seasons_dict[list_of_seasons[-1]]['general_table'].columns)
columns.append('season')
best_def_table= pd.DataFrame(columns=columns)
for i in seasons_dict:
    best_def_team= seasons_dict[i]['general_table']
    best_def_team= best_def_team.sort_values(by=['xGA/90','GA']).reset_index(drop=True)
    best_def_team= best_def_team.iloc[0]
    best_def_team['season']=i
    best_def_table.loc[len(best_def_table)]= best_def_team
best_def_table= best_def_table.loc[:,['Rk','Squad','xGA/90','GA','season']]

best_off_table= pd.DataFrame(columns=columns)
for i in seasons_dict:
    best_off_team= seasons_dict[i]['general_table']
    best_off_team= best_off_team.sort_values(by=['xG/90','GF'],ascending= False).reset_index(drop=True)
    best_off_team= best_off_team.iloc[0]
    best_off_team['season']=i
    best_off_table.loc[len(best_off_table)]= best_off_team
best_off_table= best_off_table.loc[:,['Rk','Squad','xG/90','GF', 'season']]
 


