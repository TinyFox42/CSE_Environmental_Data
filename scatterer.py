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
ax.set_title("Percent of green Energy vs. Average Income in State\n2016")
ax.set_xlabel("Average income in State($)")
ax.set_ylabel("Average Green Power Generation per Month (MW)")
r2='$r^2$='+str(int(r**2*100))+'%'
text=ax.text(0.5, 0.1, r2+"\np=%.2f"%p, transform=ax.transAxes)
if p<0.05:
    text.set_bbox(dict(boxstyle='round',facecolor='lime',alpha=0.6))
else:
    text.set_bbox(dict(boxstyle='round',facecolor='white',alpha=0.6))
#print p
fig.show()