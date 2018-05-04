import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import reader
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
shp_info = m.readshapefile('st99_d00','states',drawbounds=True)
p = reader.parse_data()[0]
long_state_order=['Alaska','Alabama','Arkansas','Arizona','California','Colorado','Connecticut','District of Columbia','Delaware','Florida','Georgia','Hawaii','Iowa','Idaho','Illinois','Indiana',
    'Kansas','Kentucky','Louisiana','Massachusetts','Maryland','Maine','Michigan','Minnesota','Missouri','Mississippi','Montana','North Carolina', 'North Dakota','Nebraska','New Hampshire',
    'New Jersey','New Mexico','Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Virginia','Vermont',
    'Washington','Wisconsin','West Virginia','Wyoming']
bio = dict(zip(long_state_order,p['biomass']))
colors={}
statenames=[]
cmap = plt.cm.Purples
vmin = 0; vmax = 500000
for shapedict in m.states_info:
    statename = shapedict['NAME']
    if statename not in ['District of Columbia','Puerto Rico']:
        energy = bio[statename] * 1.0
        colors[statename] = cmap(1.-np.sqrt((energy-vmin)/(vmax-vmin)))[:3]
    statenames.append(statename)
ax = plt.gca()
for nshape,seg in enumerate(m.states):
    if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
plt.title('Biomass Energy Production per State (MW-hr)')
plt.show()