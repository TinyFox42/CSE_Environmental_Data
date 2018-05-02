import reader
#going to make a scatter plot of the data
gens, income=reader.parse_data()
green_gens=['geothermal','hydroelectric','nuclear','solar','wind']
greens=[]
for i in range(51):
    total=0
    for gre in green_gens:
        total+=gens[gre][i]
    greens.append(total/len(green_gens))
#print greens
percents=[]
for i in range(51):
    per=(100.0*greens[i]/gens['total'][i])
    percents.append(round(per,3))
#print percents
import matplotlib.pyplot as plt
fig, ax=plt.subplots(1,1)
ax.plot(list(range(51)), percents, 'ro')
fig.show()