import pandas as pd
from bs4 import BeautifulSoup
import csv
import pickle
import sys
import os
import re

abs_file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(file_dir)

# progess bar
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status[0:40].ljust(40)))
    sys.stdout.flush()

file_list = os.listdir(project_dir + "/data-raw")
# process a shorter list
#short_list = ['K1H', 'M5G', 'M5T', 'N6A']
#short_list = ['Brampton', 'Hamilton', "London", "Mississauga", "Ottawa", 'Toronto']
short_list = ['Brampton']

file_list = list( filter( lambda x: any(y in x for y in short_list), file_list) )
print( f'cleaning short list... {file_list}')
# progress bar settings
total = len(file_list)
k = 0

# get list of files to clean
for file in file_list:

    progress(k, total, status= f'cleaning...{file[-20:]}' )
    k += 1

    file = file.split('.')[0]

    city_name = []
    #fsa = []
    CPSO_num = []
    first_name = []
    last_name = []
    address = []
    postal_code = []
    phone = []
    fax = []
    specialization = []

    with open(project_dir + "/data-raw/" + file + ".csv", newline='') as csv_file:
        doctors = csv.DictReader(csv_file)

        for row in doctors:

            # CPSO num
            CPSO_num.append( row['CPSO'])
            # metadata
            city_name.append( row['city_name'])
            #fsa.append( row['fsa'])

            soup = BeautifulSoup( row['article'], 'html.parser')

            # name
            try:
                raw_name = soup.find('h3').text
                raw_name = raw_name[0:raw_name.find(' (')].split(', ')
                first_name.append(raw_name[1])
                last_name.append(raw_name[0])
            except:
                first_name.append('')
                last_name.append('')

            # contact details
            try:
                raw_location = soup.find('h4').next_sibling.next_sibling.get_text(separator=" ")
            except:
                raw_location = "NA"

            # try parsing in order of most detail to least
            loc1 = re.search( "(.*?)( Phone\: )(.*?)( Fax\: )(.*)", raw_location )
            loc2 = re.search( "(.*?)( Phone\: )(.*?)", raw_location )
            loc3 = re.search( "(.*)", raw_location )

            loc_keep = ""
            for loc in [loc1, loc2, loc3]:
                if loc != None:
                    loc_keep = loc
                    break

            # address
            try:
                address.append( loc.group(1) )
            except:
                address.append( 'NA' )

            # phone
            try:
                phone.append( loc.group(3) )
            except:
                phone.append( 'NA' )

            # fax
            try:
                fax.append( loc.group(5) )
            except:
                fax.append( 'NA' )

            # specialization
            doc_spec = [tag.next_sibling.next_sibling.text for tag in soup.find_all('h4') if tag.text == "Area(s) of Specialization:"]
            if len(doc_spec) > 0:
                specialization.append( doc_spec[0] )
            else:
                specialization.append( 'NA' )

    # extract postal code
    for item in address:
        try:
            postal_code.append( item.split('ON')[1].strip() )
        except:
            postal_code.append( 'NA' )

    # remove postal code from address
    address2 = []
    for item in address:
        try:
            address2.append( item.split('ON')[0].strip() )
        except:
            address2.append( 'NA' )

    clean = pd.DataFrame( {
        "city_name": city_name,
        #"fsa": fsa,
        "CPSO_num": CPSO_num,
        "first_name": first_name,
        "last_name": last_name,
        "address": address2,
        "postal_code": postal_code,
        "phone": phone,
        "fax": fax,
        "specialization": specialization
    })

    clean.to_csv( project_dir + '/data-doctors/' + file + '.csv', index = False )

progress(k, total, status= 'done!' )
print()
