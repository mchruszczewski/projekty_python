import pandas as pd
import numpy as np
import datetime as d



#Step 1- define functions to save team season data

def season_stats (season_data):
    df = pd.read_html(season_data)
    season_data_dict= {
        'general_table':df[0],
        'home_away_table':df[1],
        'squad_stats':df[2],
        'squad_shooting':df[8],
        'squad_passing':df[10],
        'squad_pass_types':df[12],
        'squad_goal_shot_crea': df[14],
        'squad_def_action':df[16],
        'squad_possesion': df[18],
        'squad_play_time': df[20],
        'squad_misc': df[22]  
        }
    return  season_data_dict


#Step 2 download data for each season
seasons_dict={}
list_of_seasons= [f"{i}-{i+1}" for i in range (2018,int(d.datetime.now().year))]
print(list_of_seasons)
for i in list_of_seasons:
    if i == list_of_seasons[-1]:
        season_data= 'https://fbref.com/en/comps/9/Premier-League-Stats'
    else:
        season_data= f'https://fbref.com/en/comps/9/{i}/{i}-Premier-League-Stats'
    # season_raw= scrap_fbref_table(season_data)
    season_tables= season_stats(season_data)
    seasons_dict[i]=season_tables

