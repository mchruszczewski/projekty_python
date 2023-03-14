import pandas as pd
import numpy as np
import datetime as d
import requests
import re 
from a1_scrapping_data import *
from a2_extra_useful_columns_functions  import *
from a2_extra_useful_columns_functions  import *
from a3_data_analysis_masters import *

#Arsenal positions progress
arsenal_table= pd.DataFrame()
for i in list_of_seasons:
    team= 'Arsenal'
    table= 'general_table'
    series= team_tables (team, table, i)
    series['season']= i
    arsenal_table= pd.concat([arsenal_table, series])
arsenal_table.reset_index(drop= True, inplace= True)

#Arsenal xG/90 vs the best team in each season

arsenal_xg_comparison= best_off_table
for i in list_of_seasons:
    team= 'Arsenal'
    table= 'general_table'
    series= team_tables (team, table, i)
    series['season']= i
    arsenal_xg_comparison= pd.concat([arsenal_xg_comparison, series])
arsenal_xg_comparison= arsenal_xg_comparison.loc[:,['Rk','Squad','xG/90','GF', 'season']]
arsenal_xg_comparison.reset_index(drop= True, inplace= True)

#Arsenal xGA/90 vs the best team in each season

arsenal_xga_comparison= best_def_table
for i in list_of_seasons:
    team= 'Arsenal'
    table= 'general_table'
    series= team_tables (team, table, i)
    series['season']= i
    arsenal_xga_comparison= pd.concat([arsenal_xga_comparison, series])
arsenal_xga_comparison= arsenal_xga_comparison.loc[:,['Rk','Squad','xGA/90','GA', 'season']]
arsenal_xga_comparison.reset_index(drop= True, inplace= True)

    
    