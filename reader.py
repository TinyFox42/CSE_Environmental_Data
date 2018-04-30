#reads the .csv files, returns lists
import os.path
directory=os.path.dirname(os.path.abspath(__file__))
#print directory
gens_data=os.path.join(directory, "generation_monthly_2016.csv")
gens_file=open(gens_data)
gens_lines=gens_file.readlines()
print gens_lines[6]
gens_file.close()
gen_data={}
a=0
b=0
c=0
d=0
#so, the data will be {State:{Month:{Power_type:Amount,},},}
for line in gens_lines[6:]:
    #print "a"
    a+=1
    line=line.split(",")
    
    if line[3]!="Total Electric Power Industry":
        #print line[3]
        continue
    val=0
    mon=0
    try:
        val=int(line[5])
        mon=int(line[1])
        b+=1
    except ValueError:
        print "Yeah, something went wrong, stopping everything from crashing now..."
        c+=1
        break
    tpe=line[4]
    state=line[2]
    if state not in gen_data.keys():
        gen_data[state]={}
    if mon not in gen_data[state].keys():
        gen_data[state][mon]={}
    gen_data[state][mon][tpe]=val
    #print gen_data
    d+=1
#print gen_data
# print "a=%d"%a
# print "b=%d"%b
# print "c=%d"%c
# print "d=%d"%d