import reader
from PIL import Image
#initialise data variables
gens, income = reader.parse_data()

new_gens = gens
del gens['total']
new_gens = new_gens.items()
# 
# for energy_type in new_gens:
#     energy_type[1] = max(energy_type[1])

for state in range(52):
    highest=0
    tpe=''
    for power in powers:
        if power[i]>highest:
            highest=power[i]
            tpe=power
    


new_img = Image.new('RGB', (500, 500), color = 0)
new_canvas = ImageDraw.Draw(new_img)
