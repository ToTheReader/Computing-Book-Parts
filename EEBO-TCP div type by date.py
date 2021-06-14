# Iterates through the EEBO-TCP P4 corpus, and counts use of a target div type per date
# produces a chart of frequencies against date

import os
import xml.etree.ElementTree as ET
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker

# define the target div type
target = 'encomium'

# create a dict structure for the date range, with counters set at 0:
type_by_date = {}
for i in range(1470, 1701):
    type_by_date[i] = 0

# walk through the corpus and parse XML
for troot, dirs, files in os.walk('EEBO-TCP'):
    for file in files:
        path = troot + '\\' + file
        tree = ET.parse(path)
        root = tree.getroot()
        
        # extracting a date
        
        dates = root.findall(".//*PUBLICATIONSTMT/DATE") # this usually gives a list of 2 dates (the first is the tcp date, the second the book date)
        if len(dates) > 1: # so check if the list of dates has 2 values first
            date_text = dates[1].text # if it does, take the second value, which will be the book date
            date_match = re.search(r'1[4|5|6|7]\d\d', date_text) # because these are often transcriptions from the imprints, we need to use a regex to extract a single date.
       
            # that regex won't capture them all, so if there are any not covered, we'll say date = 0 (a more thorough study would have to account for these with more detailed regexes)
            if date_match: 
                date = date_match.group(0)
                date = int(date)
            else:
                date = 0
                
        # if the list of dates in the XML didn't have a date for the book, we'll just make it 0 too 
        else:
            date = 0
        
        
        # finding the target TYPE
        
        targets = root.findall('.//*[@TYPE="' + target + '"]') # an XPath query that finds any element with the target div type
        target_count = len(targets) # count the number of hits
        
        if date in type_by_date:
            type_by_date[date] += target_count # add number of hits to the value of the dictionary for that year



# Visualization

# convert the dict to pandas dataframe
df = pd.DataFrame({str(target):pd.Series(type_by_date)})

# create plot
ax = df[target].plot(kind='bar', figsize=(30, 20), fontsize=20)
ax.set_xlabel("Year", fontsize=12)
ax.xaxis.set_major_locator(plticker.MultipleLocator(5))
plt.show()

