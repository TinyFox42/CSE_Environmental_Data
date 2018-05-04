'''
Name:       Elijah Thorpe
Course:     CSE
Assignment: Data Modeling
Purpose:    This parses all of the data files.
            parse_data() is what you want to do, returning:
                ({'Wind':[int(megawatthours of wind in Alaska),etc.],etc.},
                [int(average income in Alaska),etc.])
            do_it() returns two dictionaries of data that is used, in a really annoying format.
            neaten_generation(data) takes in the power generation dictionary, groups it into categories, and makes it average per month, and then returns a dictionary
              of {type:[average per month per state]}.
            neaten_income(data) takes in the income dictionary, and puts it in the same order as the power generation lists, so that it is easier to use.
            parse_data() uses the above three functions to return a dictionary from neaten_generation and the list from neaten_income, all in one function call.
            gen_types(data) and states() were helper functions to write this, letting me look to see what the categories used were without having to read all of it manually.
'''
#reads the .csv files, returns lists
import os.path
#For the record, this is the order of everything:
['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL',
 'IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ',
 'NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']
['Alaska','Alabama','Arkansas','Arizona','California','Colorado','Connecticut','District of Columbia','Delaware','Florida','Georgia','Hawaii','Iowa','Indiana','Illinois','Indiana',
    'Kansas','Kentucky','Louisiana','Massachusetts','Maryland','Maine','Michigan','Minnesota','Missouri','Mississippi','Montana','North Carolina', 'North Dakota','Nebraska','New Hampshire',
    'New Jersey','New Mexico','Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Virginia','Vermont',
    'Washington','Wisconsin','West Virginia','Wyoming']
#Yes, it is alphabetical by state abreviation
#List of power generation types (arbitrary order, they are dictionary keys so not ordered):
pwrs=['total', 'coal', 'geothermal', 'hydroelectric', 'gas', 'nuclear', 'petroleum', 'solar', 'wind', 'biomass', 'other']
def do_it():
    '''Returns 2 dictionaries of the data read:
    Power generation:
        State(str):
            Month(int):
                Type(str):Megawatts(int)
                Type(str):Megawatts(int)
            Month(int):
                ``
        State(str):
            ``
    And then the much simpler one, average income:
        State(str):Income$(int)
    '''
    directory=os.path.dirname(os.path.abspath(__file__))
    #print directory
    gens_data=os.path.join(directory, "generation_monthly_2016.csv")
    gens_file=open(gens_data,'r')
    gens_lines=gens_file.readlines()
    #print gens_lines[6]
    gens_file.close()
    gen_data={}
    a=0
    b=0
    c=0
    d=0
    #so, the data will be {State:{Month:{Power_type:Amount,},},}
    for line in gens_lines[6:]:
    #while False:#Well, I could comment all of this out, or I could just do this
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
    
    
    #Now to do average incomes
    income_filename=os.path.join(directory,'average_income.csv')
    income_file=open(income_filename,'r')
    income_lines=income_file.readlines()
    income_file.close()
    income_data={}#this will be a simpler format of {state:income}
    for line in income_lines[2:]:
        parts=line.split(',')
        if not parts[1].isdigit() and (parts[1][-1]=='\n' and not parts[1][:-1].isdigit()):
            print "Skipped"+parts[0]+" because "+parts[1]
            continue
        val=int(parts[1])
        state=parts[0]
        income_data[state]=val
    return gen_data, income_data
states_order=['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL',
 'IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ',
 'NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']#generated using states(), then edited a bit
gents=['total', 'coal', 'geothermal', 'hydroelectric', 'gas', 'nuclear', 'petroleum', 'solar', 'wind', 'biomass', 'other']
gen_synonyms={'total':['Total'], 'coal':['Coal'], 'geothermal':['Geothermal'],'hydroelectric':['Hydroelectric Conventional'],'gas':['Natural Gas','Other Gases'],
    'nuclear':['Nuclear'],'petroleum':['Petroleum'],'solar':['Solar Thermal and Photovoltaic'],'wind':['Wind'],'biomass':['Wood and Wood Derived Fuels','Other Biomass'],
    'other':['Other','Pumped Storage']}#made from gen_types, then trimmed a bit
def neaten_generation(data):
    '''Makes it so that the power generation data is more readable.
    Data in this case will be the gen_data returned in do_it().
    Returns a dictionary in the format {type:[generation for each state]}'''

    #setup the dictionary
    vals={}
    for gent in gents:
        vals[gent]=[]
    '''state=states_order[0]
    mons=data[state].keys()
    mon=mons[0]
    gents=data[state][mon].keys()
    for gent in gents: #set up the dictionary
        vals[gent]=[]'''
    #start making the return values
    for i, state in enumerate(states_order):#I don't remember why I enumerated this, but I figure that as I debug it I will realize what I forgot
        last_state=state
        mons=data[state].keys()
        totals={}
        for gen in gen_synonyms.keys():
            totals[gen]=[]
        for mon in mons:
            keys=data[state][mon].keys()
            for key in keys:
                slot='other'
                for gent in gents:
                    if key in gen_synonyms[gent]:
                        slot=gent
                        break
                totals[slot].append(data[state][mon][key])
        for slot in totals.keys():
            if len(totals[slot])==0:
                vals[slot].append(0)
            else:
                vals[slot].append(sum(totals[slot])/len(totals[slot]))
        '''for gent in gents[:-1]:
            val=0
            for mon in mons:#average the generations for that state
                here=data[state][mon].keys()
                gen=''
                for h in here:
                    if h in gen_synonyms[gent]:
                        gen=h
                if gen=='':
                    val+=0
                else:
                    val+=data[state][mon][gen]
            val/=len(mons)
            vals[gent].append(val)
        gent=gents[-1]#other
        val=0
        for mon in mons:
            here=data[state][mon].keys()'''
            
    return vals
    
def states():
    '''Just something helpful for making this, makes a list of the state abbreviations in alphabetical order'''
    directory=os.path.dirname(os.path.abspath(__file__))
    #print directory
    gens_data=os.path.join(directory, "generation_monthly_2016.csv")
    gens_file=open(gens_data,'r')
    gens_lines=gens_file.readlines()
    #print gens_lines[6]
    gens_file.close()
    states=[]
    for line in gens_lines[6:]:
        parts=line.split(',')
        if parts[2] not in states:
            states.append(parts[2])
    states.sort()
    return states
def gen_types(data):
    '''Another thing to help, returns a list of all of the power generation types, based off of the data that we are actually using'''
    types=[]
    for state in data.keys():
        for mon in data[state].keys():
            for gent in data[state][mon].keys():
                if gent not in types:
                    types.append(gent)
    types.sort()
    return types

long_state_order=['Alaska','Alabama','Arkansas','Arizona','California','Colorado','Connecticut','District of Columbia','Delaware','Florida','Georgia','Hawaii','Iowa','Indiana','Illinois','Indiana',
    'Kansas','Kentucky','Louisiana','Massachusetts','Maryland','Maine','Michigan','Minnesota','Missouri','Mississippi','Montana','North Carolina', 'North Dakota','Nebraska','New Hampshire',
    'New Jersey','New Mexico','Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Virginia','Vermont',
    'Washington','Wisconsin','West Virginia','Wyoming']#that was really painful to make, and would have been much easier if the abbreviations actually made sense
def neaten_income(data):
    '''Just puts the incomes in the same order as the power generation data'''
    vals=[]
    for state in long_state_order:
        vals.append(data[state])
    return vals
def parse_data():
    '''Just makes it easier to do everything, returns generation data and income data
    Returns 2 values (as a tuple, technically):
        {'Type1':[int(power for state 1),int(power state 2)],'Type2':[you get the idea]}
        [int(average income state 1), int(average income state 2)]'''
    gens, income=do_it()
    gens=neaten_generation(gens)
    income=neaten_income(income)
    return gens, income