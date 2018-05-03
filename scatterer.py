import reader
#going to make a scatter plot of the data
gens, income=reader.parse_data()
green_gens=['geothermal','hydroelectric','nuclear','solar','wind']
greens=[]
for i in range(51):
    total=0
    for gre in green_gens:
        total+=gens[gre][i]
    greens.append(total)
#print greens
percents=[]
for i in range(51):
    per=(100.0*greens[i]/gens['total'][i])
    percents.append(round(per,3))
#print percents
import matplotlib.pyplot as plt
#for p-values, going to want to look at scipy.stats (pltw used it for the other stuff)
from scipy.stats import linregress#what pltw used, still need to look into it
import numpy as np
fig, ax=plt.subplots(1,1)
m,b,r,p,E=linregress(income,percents)#Yeah, not goint to be able to do this now
ax.plot(income, percents, 'ro')
xmin,xmax=ax.get_xlim()
x=np.linspace(xmin,xmax)
y=m*x+b
ax.plot(x,y,'b-')
print p
fig.show()