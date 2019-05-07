# download raw html table for each page of search results in abbotsford, bc

import requests
from bs4 import BeautifulSoup
import time
from random import randint
import os
import csv

abs_file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(file_dir)

url_search = "https://www.cpsbc.ca/physician_search"

headers_search = {
    "Host": "www.cpsbc.ca",
    "User-Agent": "Adam Kowalczewski, Service Canada, adam.kowalczewski@servicecanada.gc.ca",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.cpsbc.ca/physician_search",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "402",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.1291641330.1536174231; _pk_id.1.3ae9=d53891f703291249.1541692075.2.1541791079.1541791079.; _pk_ref.1.3ae9=%5B%22%22%2C%22%22%2C1541791079%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; device=3; device_type=0; SSESS46e5ac66c3cb256f0a441094408a6223=aeWdQpCtrGyXwLtoKrImOXR0lD2R_-pyK6iO8XiUrIg; has_js=1; _gid=GA1.2.1817195007.1542394287; _gat=1",
    "Upgrade-Insecure-Requests": "1"
}



payload = {
    "filter[accept_new_pat]":"1",
    "filter[gp_or_spec]":"A",
    "filter[city]":"Abbotsford",
    "filter[active]":"A",
    "op":"Search",
    "form_build_id":"form-Ss6cCwl0c7Os_BMDUaPuWbQJjBm2MMtMREjFpFNTuvY",
    "form_id":"college_physio_search_filter_form"
}



#with requests.Session() as s:
results = {}
s = requests.Session()

# get nonce
r = s.get( url_search )
soup = BeautifulSoup(r.content, 'html.parser')
nonce = soup.find(id="edit-filter").input['value']
payload["filter[nonce]"] = nonce

next_page = "https://www.cpsbc.ca/physician_search?filter_first_name=&filter_last_name=&filter_city=Abbotsford&filter_gp_or_spec=A&filter_specialty=&filter_accept_new_pat=0&filter_gender=&filter_active=A&filter_radius=&filter_postal_code=&filter_language=&filter_nonce={}&page={}"

# submit search
r = s.post( url_search, data = payload )

# starting from... (0 = beginning)
i = 0
# move to next page until end
while True:
#for i in range(0, 3):

    time.sleep(randint(1,3))

    print(f"Scraping page {i+1}")
    r = s.get( next_page.format(nonce, i) )
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # add a page of results to dict
    page_num = soup.find(class_ = "active" ).text
    tbl = soup.find('div', class_ = "college-physio-search-results-wrapper")
    results[page_num] = tbl

    if 'last' in soup.find(class_ = "active" ).parent['class']:
        break

    i += 1

with open( f'{project_dir}/data-raw/dr-abbotsford.csv', 'w' ) as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow( ['page', 'table'] )
    for key, val in results.items():
        writer.writerow( [key, val] )
    

