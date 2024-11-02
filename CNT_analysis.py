# -*- coding: utf-8 -*-
"""
@author: asenic
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import ttest_ind

def get_colour_opposite(colorname):
      opposite = {
        "red"     : "cyan", # R
        "yellow"  : "blue", # Y
        "green"   : "magenta", # G
        "blue"    : "yellow", # B
        "magenta" : "green", # 
        "skyblue" : "brown", # 
        "brown"   : "skyblue", # noncanonical
     "lightblue"  : "orange", # noncanonical
        "orange"  : "lightblue", # dark orange
        "cyan"    : "red", # 
        "black"   : "white", # 
        "white"   : "black",
        "Silver"  : "Silver"}
      return opposite[colorname]

#check opposite colors
def get_inverted(dat):
    inv=pd.DataFrame({'RT':[]})
    for i in range(len(dat)):
        if dat.loc[:,"presentedcolor"][i] == get_colour_opposite(dat.loc[:,"selection"][i]) : inv=np.append(inv,dat['RT'][i])
    ooa=round(len(inv)/(len(dat))*100,2)
    return inv, ooa

#read CNT results
expi='color_selection_results_inv100.csv'
exp='color_selection_results_norm100.csv'
path='d:\\my_scripts\\py\\CNT'
os.chdir(path)
data=pd.read_csv(exp, sep=",") #normal colors
idata=pd.read_csv(expi, sep=",") #inverted colors
adata=data.query('Accuracy == 1')['RT'] #for norm
ndata=idata.query('Accuracy == 0')['RT'] #for inv
adata=adata.reset_index(drop=True)
ndata=ndata.reset_index(drop=True)

#adata=data.query('Accuracy == 0 and Response != "down"')#adata=accurate responses only

#normal colors
oa=round(len(adata)/(len(data))*100,2)
oai=100-round(len(ndata)/(len(data))*100,2)
print('Overall accuracy for normal colors: ',oa, '% for n=',len(adata), '.')
print('Accuracy if accounted for inverted colors:', oai, '% for n=',len(ndata),'.')
#check opposite colors
inv, ooa = get_inverted(data)
print('Overall accuracy for inverted colors: ',ooa, '% for n=',len(adata), '.')    
iinv, ooai = get_inverted(idata)
print('Accuracy if accounted for inverted colors:',ooai, '% for n=',len(ndata),'.')


#boxplot with scatter
sns.barplot([oa,ooa, oai, ooai]) #accuracy
rt=pd.DataFrame(data={'normal': pd.Series(adata),'inverted':pd.Series(iinv)})
rt=pd.melt(rt)
rt['c'] = rt.variable=='normal'
rt.c = rt.c.replace({True: 1, False: 0})
rt.rename(columns={'value': 'RT'}, inplace=True)
sns.boxplot(data=rt, x=rt.variable, y=rt.RT, hue=rt.variable)
for i in [0,1]:
    y = rt.RT[rt.c==i]#.dropna()
    x = np.random.normal(i, 0.04, size=len(y))
    plt.plot(x, y, 'k.', alpha=0.5)

#statistics
t_statistic, p_value = ttest_ind(adata,iinv)
# Output the results
print("t-statistic",round(t_statistic,3))
print("p-value:", round(p_value,10))
# t-statistic 0.87
# p-value: 0.3855690048
#RT the same

#by colors 
#colors =  ['green','magenta','black', 'orange','white','skyblue','yellow','red','cyan', 'brown','blue']
colors =  sorted(pd.unique(pd.Series(data.presentedcolor)))
data=data.sort_values('presentedcolor')
sns.set_context("paper", font_scale=0.8)
sns.boxplot(x = data['presentedcolor'], y = data['RT'], hue = data['presentedcolor'],palette = colors).legend_.remove()
