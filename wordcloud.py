import reader
import sys
import os
from PIL import Image, ImageDraw, ImageFont

def get_color(etype):
    if not avgincome[etype]:
        return '#FFB16F'
    keys = [(50000, '#59FF6B'), (55000, '#71E851'), (60000, '#BCFF65'), ( 65000, '#DBE851')]
    for key in keys:
        if avgincome[etype] >= key[0]:
            color = key[1]
    
    return color
    

#initialise data variables and path variables
gens, income = reader.parse_data()
directory = os.path.dirname(os.path.abspath(__file__))

#make a copy of gens dict, excluding the 'total' data pair
new_gens = gens
del new_gens['total']

#create new dictionary to store a count of countries that have x type of energy as its most energy produced
emaxes = {e[0]:0 for e in new_gens.items()}
avgincome = {e[0]:[] for e in new_gens.items()}
for state in range(51):
    emax = -sys.maxint - 1
    emaxtype = ''
    for e in new_gens.items():            
        if e[1][state] > emax:
            emax = e[1][state]
            emaxtype = e[0]
    emaxes[emaxtype] += 1
    avgincome[emaxtype].append(income[state])

#calculate average income
for etype in avgincome.keys():
    if emaxes[etype] != 0:
        avgincome[etype] = sum(avgincome[etype]) / float(emaxes[etype])

#normalise the data    
norm_sizeMax = 140.0
norm_sizeMin = 25.0
norm_emaxes = sorted([(etype,
                        int((norm_sizeMin + (eproduced - min(emaxes.values())) * (norm_sizeMax - norm_sizeMin) / float(max(emaxes.values()) - min(emaxes.values()))))) 
                        for etype, eproduced in emaxes.items()],
                        key = lambda x: x[1], reverse = True)

#generate new Pillow canvas
fnt = ImageFont.truetype(os.path.join(directory, 'helvetica.ttf'), int(norm_sizeMax))
canvas_size = (fnt.getsize(''.join([emax[0] for emax in norm_emaxes]))[0], int(norm_sizeMax * 3))
text = Image.new('RGBA', canvas_size, (0, 0, 0, 255))
draw = ImageDraw.Draw(text)

#display words on canvas with proper offset
word_offset = (120, canvas_size[1] / 3)
for value in norm_emaxes:
    fnt_size = value[1]
    fnt = ImageFont.truetype(os.path.join(directory, 'helvetica.ttf'), fnt_size)

    draw.text(word_offset, value[0], font=fnt, fill=get_color(value[0]))    
    
    word_offset = (word_offset[0] + fnt.getsize(value[0])[0] + 20, word_offset[1] + 2)

#crop image to proper height
text = text.crop((0, 0, word_offset[0] + 100, text.height))

#refresh ImageDraw object and prepare font
draw = ImageDraw.Draw(text)
fnt = ImageFont.truetype(os.path.join(directory, 'helvetica.ttf'), 20)

#create legend offset and values
legend_offset = (text.width - 1050, text.height - 75, text.width - 975, text.height - 50)
legend = [('> 50,000', '#59FF6B'), ('> 55,000', '#71E851'), ('> 60,000', '#BCFF65'), ('> 65,000', '#DBE851'), ('No States Available', '#FFB16F')]

#draw a color legend into bottom right corner
for key in legend:
    draw.rectangle(legend_offset, fill = key[1], outline = None)
    draw.text((legend_offset[0] + 85, legend_offset[1], legend_offset[2] + 85, legend_offset[3]), key[0], font = fnt, fill='white')
    legend_offset = (legend_offset[0] + 100 + fnt.getsize(key[0])[0], legend_offset[1], legend_offset[2] + 100 + fnt.getsize(key[0])[0], legend_offset[3])

text.show()