import reader
'''
Name:       Elijah Thorpe
Course:     CSE
Assignment: Data Modeling
Purpose:    Creates a whole bunch of scatter plots when run.
            This is the first one that I can't just give a function summary to explain...
            Going to make easily visible comments like this for important notes
            Why parts of this look weird:
                1. This was code origninally just for 1 group, expanded to multiple, so some loops could be combined better
                2. I was originally going to put them all in 1 figure with a lot of subplots, but there were problems, and
                    it wasn't worth all the work to fix it
'''
#going to make a scatter plot of the data
gens, income=reader.parse_data() 
'''Gets the data'''
#This is the list of all the graphs to be made, [Name, [types]]
'''These make the titles and types for the scatter plots, and then just makes ones for individual types'''
groups=[['Green',['geothermal','hydroelectric','nuclear','solar','wind']],
        ['Other',['other']],
        ['Fossil Fuel',['coal','gas','petroleum']]]
for t in reader.pwrs[1:-1]:#All but 'total' and 'other'
    name=t[0].upper()+t[1:]
    groups.append([name,[t]])
#green_gens=['geothermal','hydroelectric','nuclear','solar','wind']
#greens=[]
data=[]
'''Goes through and adds up all the power generations per group per state'''
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
'''Goes through and finds the percent of the total power generation for that type of power, per state'''
for j,g in enumerate(groups):
    percents.append([])
    for i in range(51):
        per=(100.0*data[j][i]/gens['total'][i])
        percents[j].append(round(per,3))
#print percents
'''Everything after this is making the scatter plots'''
import matplotlib.pyplot as plt
#for p-values, going to want to look at scipy.stats (pltw used it for the other stuff)
from scipy.stats import linregress#what pltw used, still need to look into it
import numpy as np
'''Goes through each grouping'''
for i,g in enumerate(groups):
    fig, ax=plt.subplots(1,1)
    '''Does a linear regression on the data'''
    '''(a lot of this is based off of what pltw did'''
    m,b,r,p,E=linregress(income,percents[i])
    ax.plot(income, percents[i], 'ro')
    xmin,xmax=ax.get_xlim()
    x=np.linspace(xmin,xmax)
    y=m*x+b
    '''plots the line'''
    ax.plot(x,y,'b-')
    ax.set_title("Percent of %s Energy vs. Average Income in State\n2016"%g[0])
    ax.set_xlabel("Average income in State($)")
    ax.set_ylabel("Average %s Power Generation\n per Month (MWH)"%g[0])
    r2='$r^2$='+str(int(r**2*100))+'%'
    '''Sets the text and box (styles from what pltw did)'''
    text=ax.text(0.5, 0.1, r2+"\np=%.2f"%p, transform=ax.transAxes)
    if p<0.05:
        text.set_bbox(dict(boxstyle='round',facecolor='lime',alpha=0.6))
    else:
        text.set_bbox(dict(boxstyle='round',facecolor='white',alpha=0.6))
    fig.show()
#print p
#fig.show()#''' #This is a really nice trick I found to stop errors when making comments
                #If there is an open ''', the # is ignored and this closes it
                #if there isn't one, then the # makes the ''' be ignored and not give an error/warning