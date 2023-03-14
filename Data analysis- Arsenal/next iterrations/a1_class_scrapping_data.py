import pandas as pd
import numpy as np
import datetime as d
from bs4 import BeautifulSoup
import requests
import re 



class Table:
    def __init__(self, season):
        self.season= season
        
    def season_stats (self)