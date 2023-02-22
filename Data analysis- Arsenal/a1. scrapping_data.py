import pandas as pd
import numpy as np
import datetime as d
from bs4 import BeautifulSoup
import requests
import re 



#Step 1- define functions to save team season data
# table_names= ['general_table', 'home_away_table', 'squad_stats', 'shooting', 'passing','pass_types',
#              'goal_shot_crea', 'def_action', 'possesion', 'play_time', 'misc']
table_names= ['general_table', 'home_away_table', 'shooting', 'goal_shot_crea', 'play_time', 'misc', 'squad_stats','pass_types',
              'possesion', 'play_time','passing','def_actions' ]
def season_stats (season_data):
    df = pd.read_html(season_data)
    season_data_dict= {
        table_names[0]:df[0],
        table_names[1]:df[1],
        table_names[6]:df[2],
        table_names[2]:df[8],
        table_names[-2]:df[10],
        table_names[7]:df[12],
        table_names[3]: df[14],
        table_names[-1]:df[16],
        table_names[-4]: df[18],
        table_names[-3]: df[20],
        table_names[5]: df[22]  
        }
        
    return  season_data_dict


#Step 2 download data for each season
seasons_dict={}

list_of_seasons= [f"{i}-{i+1}" for i in range (2017,int(d.datetime.now().year))]

for i in list_of_seasons:
    if i == list_of_seasons[-1]:
        season_data= 'https://fbref.com/en/comps/9/Premier-League-Stats'
    else:
        season_data= f'https://fbref.com/en/comps/9/{i}/{i}-Premier-League-Stats'
    season_tables= season_stats(season_data)
    seasons_dict[i]=season_tables
    
#Step 2.1 Clearing data amd renaming unndamed multindex- 
#Step 2.1.1 looping through the dictionary - renaming columns

for i in seasons_dict:
    for j in table_names[1:2]:
        list_columns= list(seasons_dict[i][j].columns.levels[0])
        columns_dict = {k: "General Info" for k in list_columns[-2:]}
        seasons_dict[i][j] = seasons_dict[i][j].rename(columns=columns_dict, level=0)
for i in seasons_dict:
    for j in table_names[2:6]:
        list_columns= list(seasons_dict[i][j].columns.levels[0])
        columns_dict = {k: "General Info" for k in list_columns[-3:]}
        seasons_dict[i][j] = seasons_dict[i][j].rename(columns=columns_dict, level=0)
for i in seasons_dict:
    for j in table_names[6:10]:
        list_columns= list(seasons_dict[i][j].columns.levels[0])
        columns_dict = {k: "General Info" for k in list_columns[-4:]}
        seasons_dict[i][j] = seasons_dict[i][j].rename(columns=columns_dict, level=0)
        
#Step 2.1.2 Renaming columns that cannot be renamed with loop
#passing:

columns_dict= {
 'Unnamed: 0_level_0': 'General Info',
 'Unnamed: 17_level_0': 'Assists' ,
 'Unnamed: 18_level_0': 'Assists' ,
 'Unnamed: 19_level_0': 'Assists' ,
 'Unnamed: 1_level_0': 'General Info',
 'Unnamed: 20_level_0': 'Assists' ,
 'Unnamed: 21_level_0':'Progressive passes',
 'Unnamed: 22_level_0':'Progressive passes',
 'Unnamed: 23_level_0':'Progressive passes',
 'Unnamed: 24_level_0':'Progressive passes',
 'Unnamed: 25_level_0':'Progressive passes',
 'Unnamed: 2_level_0': 'General Info'
    }


for i in seasons_dict:
    seasons_dict[i]['passing']= seasons_dict[i]['passing'].rename(columns=columns_dict, level=0)

#def_actions 

columns_dict={
 'Unnamed: 0_level_0':'General Info',
 'Unnamed: 15_level_0':'Intercept',
 'Unnamed: 16_level_0':'Intercept',
 'Unnamed: 17_level_0':'Clearances',
 'Unnamed: 18_level_0':'Errors',
 'Unnamed: 1_level_0':'General Info',
 'Unnamed: 2_level_0':'General Info'
    }
 
for i in seasons_dict:
    seasons_dict[i]['def_actions']= seasons_dict[i]['def_actions'].rename(columns=columns_dict, level=0)
    
#Step 3 create team ids table

#step 3.1 downloading list of 'a href' from fbref.com
list_all_a_href=[]
for i in list_of_seasons:
    if i == list_of_seasons[-1]:
        r=requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")
        soup=BeautifulSoup(r.content,"html.parser")
        list_all_a_href+=soup.find_all('a')
    else:
        r=requests.get(f'https://fbref.com/en/comps/9/{i}/{i}-Premier-League-Stats')
        soup=BeautifulSoup(r.content,"html.parser")
        list_all_a_href+=soup.find_all('a')
        

# step 3.2 getting list of clubs for all seasons

# step 3.2.1 creating empty df
club_id_df=pd.DataFrame()              
#step 3.2.2 looping through seasons and adding teams to dataset
for i in seasons_dict:
    club_df= seasons_dict[i]
    club_df= club_df['general_table'].Squad
    club_id_df= pd.concat([club_id_df,club_df])
#step 3.3.3 dropping duplicates and renaming column to 'squd'
club_id_df= club_id_df.drop_duplicates().reset_index(drop=True)
club_id_df.columns= ['Squad']

#step 3.3 searching for ids
list_df= list(club_id_df['Squad'])
club_id_df['ID']=np.nan
for i, squad_name in enumerate(list_df):
    # Compile a regular expression pattern to match the team name
    pattern = re.compile(r'\b{}\b'.format(re.escape(squad_name)), re.IGNORECASE)
    for j in list_all_a_href:
        # Check if the href matches the pattern
        if pattern.search(str(j)):
            club_id_df.at[i, 'ID'] = str(j)[20:28] 
club_id_df['Squad']= club_id_df['Squad'].str.replace(" ", "-")
#Chelsea ID needs to be exchanged as Women team is sourced from default

club_id_df.loc[club_id_df['Squad']=='Chelsea','ID']= 'cff3d9bb'
    
    
#step 4 creating function to search for players stats in a given season in a given team

def stats_search(team, season):
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
#step 5 creating function to search for a stats of a palayer from given team 
                         #!!!stats_search needs to be executed first!!!
                         
def player_stats_search (player_name, df):
    df= df[df['General Info']['Player'].str.contains(player_name)]
    return df
                         


