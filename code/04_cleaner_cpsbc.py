import pandas as pd
from bs4 import BeautifulSoup
import csv
import os

abs_file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(file_dir)

# raw = {}

# csv_file = open(project_dir + "/data-raw/dr-abbotsford.csv", newline='')
# pages = csv.DictReader(csv_file)

# cpsbc = {}
# for page in pages:
#     cpsbc[page['page']] = page['table']

# just want first name and last name for now

bc_names_raw = []
with open(project_dir + "/data-raw/dr-abbotsford.csv", newline='') as csv_file:
    pages = csv.DictReader(csv_file)
    for page in pages:
        soup = BeautifulSoup( page['table'], 'lxml' )
        for link in soup.find_all('a', href = True):
            bc_names_raw.append(link.text)

# clean up name
bc_first_names = []
bc_last_names = []
for name in bc_names_raw:
    bc_first_names.append(name[:-2].split(',')[1])
    bc_last_names.append(name.split(',')[0])

bc_doctors = pd.DataFrame({
    'first_name': bc_first_names,
    'last_name': bc_last_names
})

bc_doctors.to_csv( project_dir + "/data-doctors/dr-abbotsford.csv")