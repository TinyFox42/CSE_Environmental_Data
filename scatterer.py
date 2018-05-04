import reader
#going to make a scatter plot of the data
gens, income=reader.parse_data()
#This is the list of all the graphs to be made, [Name, [types]]
groups=[['Green',['geothermal','hydroelectric','nuclear','solar','wind']],
        ['Other',['other']]]
#green_gens=['geothermal','hydroelectric','nuclear','solar','wind']
#greens=[]
data=[]
for j,g in enumerate(groups):
    data.append([])
    for i in range(51):
        total=0
        for gre in g[1]:
            total+=gens[gre][i]
        data[j].append(total)
#print greens
#print data
percents=[]
for j,g in enumerate(groups):
    percents.append([])
    for i in range(51):
        per=(100.0*data[j][i]/gens['total'][i])
        percents[j].append(round(per,3))
#print percents

import matplotlib.pyplot as plt
#for p-values, going to want to look at scipy.stats (pltw used it for the other stuff)
from scipy.stats import linregress#what pltw used, still need to look into it
import numpy as np


#print s,l,w



for i,g in enumerate(groups):
    fig, ax=plt.subplots(1,1)
    m,b,r,p,E=linregress(income,percents[i])#Yeah, not goint to be able to do this now
    ax.plot(income, percents[i], 'ro')
    xmin,xmax=ax.get_xlim()
    x=np.linspace(xmin,xmax)
    y=m*x+b
    ax.plot(x,y,'b-')
    ax.set_title("Percent of %s Energy vs. Average Income in State\n2016"%g[0])
    ax.set_xlabel("Average income in State($)")
    ax.set_ylabel("Average %s Power Generation\n per Month (MWH)"%g[0])
    r2='$r^2$='+str(int(r**2*100))+'%'
    text=ax.text(0.5, 0.1, r2+"\np=%.2f"%p, transform=ax.transAxes)
    if p<0.05:
        text.set_bbox(dict(boxstyle='round',facecolor='lime',alpha=0.6))
    else:
        text.set_bbox(dict(boxstyle='round',facecolor='white',alpha=0.6))
    fig.show()
#print p
#fig.show()#'''