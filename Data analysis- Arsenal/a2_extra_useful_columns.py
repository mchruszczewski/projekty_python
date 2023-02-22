import pandas as pd
import numpy as np
import datetime as d
from bs4 import BeautifulSoup
import requests
import re 
from a1_scrapping_data import *

for i in seasons_dict:
    seasons_dict[i]['general_table']['xG/90']= round(seasons_dict[i]['general_table']['xG']
                                                /seasons_dict[i]['general_table']['MP'],2)
    seasons_dict[i]['general_table']['xGA/90']= round(seasons_dict[i]['general_table']['xGA']
                                                /seasons_dict[i]['general_table']['MP'],2)
