import pandas as pd
from bs4 import BeautifulSoup
import csv
import pickle
import sys
import os
import re

absFilePath = os.path.abspath(__file__)
fileDir = os.path.dirname(os.path.abspath(__file__))
projectDir = os.path.dirname(fileDir)

# get list of files to clean
for file in os.listdir(projectDir + "/data-raw"):
    if not re.match('doctors', file):
        break
    file = file.split('.')[0]

    CPSO_num = []
    first_name = []
    last_name = []
    location = []
    specialization = []

    with open(projectDir + "/data-raw/" + file + ".csv", newline='') as csv_file:
        doctors = csv.DictReader(csv_file, fieldnames = ['CPSO', 'article'])

        for row in doctors:
            # CPSO num
            CPSO_num.append( row['CPSO'])

            soup = BeautifulSoup( row['article'], 'html.parser')

            # name
            raw_name = soup.find('h3').text
            raw_name = raw_name[0:raw_name.find(' (')].split(', ')
            first_name.append(raw_name[1])
            last_name.append(raw_name[0])

            # location
            location.append(soup.find('p').get_text(separator=" "))

            # specialization
            doc_spec = [tag.next_sibling.next_sibling.text for tag in soup.find_all('h4') if tag.text == "Area(s) of Specialization:"]
            if len(doc_spec) > 0:
                specialization.append( doc_spec[0] )
            else:
                specialization.append( "" )

    clean = pd.DataFrame( {
        "CPSO_num": CPSO_num,
        "first_name": first_name,
        "last_name": last_name,
        "location": location,
        "specialization": specialization
    })

    with open(projectDir + '/data/' + file + '.pickle', 'wb') as f:
        pickle.dump(clean, f)
