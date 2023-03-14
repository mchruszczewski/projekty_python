import pandas as pd
import numpy as np
import datetime as d
from bs4 import BeautifulSoup
import requests
import re 
from a1_scrapping_data import *

#Search functions

def stats_search(team, season):
    """ Returns DataFrame with all players stats of given team for given season"""
    team = team.replace(" ", "-")
    try:
        team_id = club_id_df[club_id_df['Squad'].str.contains(team)]['ID'].iloc[0]
    except IndexError:
        print(f"Error: team '{team}' not found in club_id_df.")
        return None
    if season == list_of_seasons[-1]:
        df = pd.read_html(f'https://fbref.com/en/squads/{team_id}/{team}-Stats')
    else:
        df = pd.read_html(f'https://fbref.com/en/squads/{team_id}/{season}/{team}-Stats')
    df = df[0]
    df = df.drop(columns=['Unnamed: 33_level_0'])
    list_columns = list(df.columns.levels[0])
    columns_dict = {i: "General Info" for i in list_columns[-6:]}
    df = df.rename(columns=columns_dict, level=0)
    return df

                         
def player_stats_search (player_name, df):
    """ !!!EXECUTE stats_search function first!!!
    Returns DataFrame with  player stats"""
    df= df[df['General Info']['Player'].str.contains(player_name)]
    return df
                        
    
def team_tables (team, table, season):
    """ Returns set of detailed statistics for given team and given season"""
    if table == 'general_table':
        df= seasons_dict[season][table]
        df= df.loc[df['Squad']== team]
    else:
        df= seasons_dict[season][table]
        df= df[df.loc[:,('General Info','Squad')]== team]
    return df


#Adding useful columns

#Adding xG/90mins column that shows average xG for a match 

for i in seasons_dict:
    seasons_dict[i]['general_table']['xG/90']= round(seasons_dict[i]['general_table']['xG']
                                                /seasons_dict[i]['general_table']['MP'],2)
    seasons_dict[i]['general_table']['xGA/90']= round(seasons_dict[i]['general_table']['xGA']
                                                /seasons_dict[i]['general_table']['MP'],2)
    
for i in seasons_dict:
    seasons_dict[i]['general_table']['season']= f'{i}'