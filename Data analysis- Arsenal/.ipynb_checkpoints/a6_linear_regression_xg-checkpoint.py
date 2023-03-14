import pandas as pd
import numpy as np
import datetime as d
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from a1_scrapping_data import *

df_regression= pd.DataFrame()

for i in seasons_dict:
    df_regression=pd.concat([df, seasons_dict[i]['general_table']])
    
df_regression.reset_index(inplace= True, drop= True)

y= df_regression.Rk
x= df_regression['xGD/90'].values.reshape(-1,1)

model= LinearRegression().fit(x,y)
r_sq= model.score(x,y)
intercept= model.intercept_
slope= model.coef_
y_pred= intercept + slope*x
