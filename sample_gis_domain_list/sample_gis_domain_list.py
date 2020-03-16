#
# GISinc Contractor: Alec B.
# Description: Script assumes that the user has full permissions in the sde in order to read each dataset and feature class.
# The purpose of this script is to produce a domain list, coded value list, descriptions, and feature for each domain. This is helpful to check and see if a state has implemented
# a certain domain correctly. This was originally used to check the 'EM' dash issues we had with GTLF and SIGNS datasets.
# This script could be modified with a long try and except statement in order to bypass the datasets the user is unable to connect to.
# 02/21/2020

import time
import os,sys
import arcpy
import pandas as pd
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

# Make a dictionary from scratch by appending
def add_element(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)
    
if (sys.version_info > (3, 0)):
    # Python 3 code in this block
    #domains = arcpy.da.ListDomains(r"\\blm\dfs\loc\EGIS\ReferenceState\NV\CorporateData\NV_EDT_USER.sde") # Hard-coded
    print ('''SDE example: \\blm\dfs\loc\EGIS\ProjectsNational\NationalDataQuality\Sprint\analysis_tools\_sde_connections\california_publication.sde''')
    print ('As of 02/05/2020, script assumes you have permissions to user chosen sde. Script can be modified to run subset in the future.')
    domains = arcpy.da.ListDomains(eval(input("Enter SDE Location: ")))
else:
    # Python 2 code in this block
    #domains = arcpy.da.ListDomains(r"\\blm\dfs\loc\EGIS\ReferenceState\NV\CorporateData\NV_EDT_USER.sde") # Hard-coded
    print ('''SDE example: \\blm\dfs\loc\EGIS\ProjectsNational\NationalDataQuality\Sprint\analysis_tools\_sde_connections\california_publication.sde''')
    print ('As of 02/05/2020, script assumes you have permissions to user chosen sde. Script can be modified to run subset in the future.')
    domains = arcpy.da.ListDomains(raw_input("Enter SDE Location: ")) # User input
    print ('Running...')
    
dom_desc = {} # Blank dictionary
# Keys will be the domain name and the vals will be the domain description.
# Dictionary will match things up. We can include this later if we want/needed.

for domain in domains:
    if domain.description == '':
        add_element(dom_desc,domain.name,'NA')
    elif domain.description == None:
        add_element(dom_desc,domain.name,'NA')
    elif domain.description == ' ':
        add_element(dom_desc,domain.name,'NA')
    else:
        add_element(dom_desc,str(domain.name.encode('utf-8')),str(domain.description.encode('utf-8')))

dom_list = [] # Domain Name
types = [] # Domain type
dom_cora_vals = [] # code and range values together
dom_code_desc = [] # Code and range descriptions

for domain in domains:
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        for val, desc in coded_values.items():
            dom_list.append(domain.name)
            types.append(domain.domainType) # Get type
            if val == '':
                dom_cora_vals.append('NA')
            elif val == None:
                dom_cora_vals.append('NA')
            elif val == ' ':
                dom_cora_vals.append('NA')
            else:
                dom_cora_vals.append(val)
        for val, desc in coded_values.items():
            if desc == '':
                dom_code_desc.append('NA')
            elif desc == None:
                dom_code_desc.append('NA')
            elif desc == ' ':
                dom_code_desc.append('NA')
            else:
                dom_code_desc.append(desc)
    elif domain.domainType == 'Range': 
        dom_list.append(domain.name)
        types.append(domain.domainType) # Get type
        dom_code_desc.append('NA')
        dom_cora_vals.append(str(domain.range[0])+'-'+str(domain.range[1])) # Min - Max for range

## Should be same length:
#print len(dom_list)
#print len(types)
#print len(dom_cora_vals)
#print len(dom_code_desc)

#### Fix encoding and change to strings ######
dom_list = [x.encode('utf-8') for x in dom_list] # Fix encoding issue
dom_list = [str(r) for r in dom_list]
dom_desc = [x.encode('utf-8') for x in dom_desc] # Fix encoding issue
dom_desc = [str(r) for r in dom_desc]
types = [x.encode('utf-8') for x in types] # Fix encoding issue
types = [str(r) for r in types]

dom_cora_vals_FIXED = []
for u in dom_cora_vals:
    try:
        dom_cora_vals_FIXED.append(u.encode('utf-8'))
    except:
        dom_cora_vals_FIXED.append(str(u))

dom_cora_vals_FIXED = [str(r) for r in dom_cora_vals_FIXED]
dom_code_desc = [x.encode('utf-8') for x in dom_code_desc] # Fix encoding issue
dom_code_desc = [str(r) for r in dom_code_desc]
############
############

#natural_sort(dom_list) # Call the custom function to begin sort

# This line might not always be needed all the time, but I used it here to fix a couple lower_case issues that refused to be in the correct order.
# Final domain sort, same order as NV_EDT_USER.sde (Database Properties)
#dom_list.sort(key=lambda v: v.lower())  

# create pandas dataframe
columns = ['Domain Name', 'Domain_Type', 'Coded Values', 'Coded Values Description']

df = pd.DataFrame(list(zip(dom_list,types,dom_cora_vals_FIXED,dom_code_desc)), columns = columns)

#print len(dom_desc_2) # Should be same # of rows as df

# Sort dataframe by 'Domain Name' then Coded Values
## If you want to sort by two columns, pass a list of column labels to sort_values with the column labels ordered according to sort priority.
df = df.sort_values(['Domain Name', 'Coded Values'])
#print df.iloc[0:25]

df.to_csv(r'\\blm\dfs\loc\EGIS\ProjectsNational\NationalDataQuality\Sprint\analysis_tools\domain_review\Domain_CodedValues_list.csv',index = False) # encoding = 'utf-8'

df.to_csv(r'\\blm\dfs\loc\EGIS\ProjectsNational\NationalDataQuality\Sprint\analysis_tools\Sprint_gui\outputs\Domain_CodedValues_list.csv', index = False) # encoding = 'utf-8'

print('script is complete!!!')

# Wait for 5 seconds
time.sleep(5)
            
    
    

