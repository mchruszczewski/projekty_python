import pandas as pd
import numpy as np
import math
from datetime import date

path= '/Users/michalchruszczewski/Documents/kalkulator_wydatków/input_spendings'


#Step 1: Defining inputs

input_pko= pd.read_excel(path+'/history_20230223_111504.xls', sheet_name= 'Lista transakcji')
input_ing= pd.read_excel(path+'/Lista_transakcji_nr_0154205485_230223.xlsx', skiprows= 19,  sheet_name='Lista_transakcji_nr_0154205485_' )
category_dict= {"sport":["fpinka", 'bez kontuzji','fitness','manpowergroup'], 
                "zakupy spozywcze":['netto','kaufland','carrefour','biedronka','lidl','ntfy',"auchan","El Gato","concept","stu"], 
                "di bakery":["di bakery"], 
                "zabka":["zabka"], 
                "samochód":['santander'], 
                "kredyty i rachunki":['pzm','pgnig','tauron','netia','opłata','splata',"spłat","rachunki"], 
                'rozrywka':['netflix','hbo','cinema',"storytel","spotify"],
                'allegro':['allegro'],
                'podatki firma': ['urzad','zus','skarbowy','ifirma'],
                "revolut":["revolut"], 
                "jedzenie- dostawa":["uber","wolt","pyszne","bunga"],
                "bilety mpk":["urbancard"],
                "zakupy ciuchów/kosmetyków/fryzjer":     
                ["fashion","zara","intim","calzedonia","adidas",
                "reserved","triumph","rossmann","babett"],
                "podróże":["ryanair","booking","wizz","hotel"],
                "pies":["zoo","maxi","psi bufet","weteryn"]
                }
#step 2: Data clearance

#ING

input_ing= input_ing.iloc[:,[0,2,3,8]].dropna()

#PKO

input_pko= input_pko.iloc[:,[0,3,12,13]].dropna()

#step 3: Data joining

#changing order to match and renaming columns

input_pko= input_pko.iloc[:,[0,3,2,1]]
input_ing= input_ing.iloc[:,[0,1,2,3]]
new_columns_name= ["Data", "Kontrahent", "Tytuł", "Kwota"]
input_pko.columns= new_columns_name
input_ing.columns= new_columns_name
#join
data_v1= pd.concat([input_ing,input_pko], axis= 'rows')


#step 4 grouping into new categories

#adding new column
data_v1['Kategoria']= "Other"

#overwriting values in 'Kategoria'

data_v2= data_v1.copy()

data_v2 = data_v2[~(data_v2['Tytuł']).str.lower().str.contains('wyp'.lower())]
data_v2 = data_v2[~(data_v2['Tytuł']).str.lower().str.contains('oszcz'.lower())]

for x in category_dict: 
    for y in category_dict[x]:
        data_v2['Kategoria']= np.where(data_v2['Kontrahent'].str.contains(y, case= False), x, data_v2['Kategoria'])
        data_v2['Kategoria']= np.where(data_v2['Tytuł'].str.contains(y, case= False), x, data_v2['Kategoria'])
        
data_v2= data_v2.reset_index(drop=True)

        
#step 5 calculating sum for each category + provisions


category_split= data_v2.groupby(['Kategoria'], as_index= False).sum(['Kwota'])
category_split.loc[category_split['Kategoria'].str.contains('kredyty'), "Kwota"] += 1000
category_split['%']= 0
category_split['%']= category_split['Kwota']/category_split['Kwota'].sum()

#step 6 write t oexcel

with pd.ExcelWriter(f"/Users/michalchruszczewski/Documents/kalkulator_wydatków/output_spendings/Output{date.today()}.xlsx") as writer:
                      
                      data_v2.to_excel(writer, sheet_name="General")
                      category_split.to_excel(writer, sheet_name="Kategorie")


        
                               





