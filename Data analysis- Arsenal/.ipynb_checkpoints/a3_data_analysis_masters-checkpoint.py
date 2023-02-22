import pandas as pd
import numpy as np
import datetime as d
from bs4 import BeautifulSoup
import requests
import re 
from a1_scrapping_data import *
from a2_extra_useful_columns import *

#general_table_masters table with all masters from 2017- 2022
general_table_masters= pd.DataFrame()
for i in seasons_dict:
    general_table_masters= pd.concat([general_table_masters, seasons_dict[i]['general_table'].iloc[0]], axis=1, sort= False)
general_table_masters= general_table_masters.transpose()    
general_table_masters['Season']= list_of_seasons
general_table_masters= general_table_masters.reset_index(drop=True)
        
#tables 





