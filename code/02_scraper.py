import requests
from bs4 import BeautifulSoup
import re
import time
from random import randint
import pickle
import csv
import sys
import os

url_search = "https://www.cpso.on.ca/Public-Information-Services/Find-a-Doctor?search=general"
url_paging = "https://www.cpso.on.ca/Public-Register-Info-(1)/Doctor-Search-Results"

absFilePath = os.path.abspath(__file__)
fileDir = os.path.dirname(os.path.abspath(__file__))
projectDir = os.path.dirname(fileDir)

# progess bar
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status[0:40].ljust(40)))
    sys.stdout.flush()

def scrape_doctors(soup):
    for doctor in soup.find_all('article'):
        doc_str = doctor.find('h3').text
        doctors[ (re.search("\d+", doc_str).group()) ] = doctor

headers_search = {
    "Host": "www.cpso.on.ca",
    "User-Agent": "Adam Kowalczewski, Service Canada, adam.kowalczewski@servicecanada.gc.ca",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.cpso.on.ca/Public-Information-Services/Find-a-Doctor?search=general",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
    "Cookie": "CMSPreferredCulture=en-CA; _ga=GA1.3.788028045.1540596057; _gid=GA1.3.1509832542.1540596057; CMSCsrfCookie=PB+DjsX3FE9SCgAk3jGZzc65Ld6NEaE755HpaDB9; ASP.NET_SessionId=pek14izhwnw4u0curdgkxygh; _gat_UA-36725164-1=1",
    "Upgrade-Insecure-Requests": "1"
}

headers_paging = {
    "Referer": "https://www.cpso.on.ca/Public-Register-Info-(1)/Doctor-Search-Results"
}

manScript = "%3b%3bAjaxControlToolkit%2c+Version%3d4.1.60919.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d28f01b0e84b6d53e%3aen-CA%3aee051b62-9cd6-49a5-87bb-93c07bc43d63%3a475a4ef5%3aeffe2a26%3a7e63a579"
manScript = manScript.replace( "%3b", ";" )
manScript = manScript.replace( "%2c", "," )
manScript = manScript.replace( "%3d", "=" )
manScript = manScript.replace( "%3a", ":" )
manScript = manScript.replace( "en-CA", "en-US")

def crawl_fsa( fsa ):
    # get HTML to generate POST data
    with requests.Session() as s:
        r = s.get(url_search)
        soup = BeautifulSoup(r.content, 'html.parser')

        payload = {
            "__CMSCsrfToken": soup.find("input", id="__CMSCsrfToken")['value'],
            "__VIEWSTATE": soup.find("input", id="__VIEWSTATE")['value'],
            "__VIEWSTATEGENERATOR": soup.find("input", id="__VIEWSTATEGENERATOR")['value'],
            "lng": 'en-CA',
            "manScript_HiddenField": manScript,
            "searchType":"general",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$advancedState":"closed",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$ConcernsState":"closed",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$txtPostalCode": fsa,
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$grpGender":"+",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$grpDocType":"rdoDocTypeAll",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$ddHospitalName":"-1",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$ddLanguage":"08",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkActiveDoctors":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkPracticeRestrictions":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkPendingHearings":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkPastHearings":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkHospitalNotices":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkConcerns":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$chkNotices":"on",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$btnSubmit1":"Submit"
        }

        # send POST request
        time.sleep(randint(1,3))
        r = s.post( url_search, data = payload )
        soup = BeautifulSoup(r.content, 'html.parser')

        while True:
            # each search group lands on page 1, scrape it first
            #print('new postal code in', city, 'scraping', fsa, soup.find('div', class_ = 'doctor-search-count').find('div', class_ = 'text-align--right').text)
            scrape_doctors(soup)

            # stop if there's no more pages
            try:
                n_in_group = len(soup.find('div', class_ = "doctor-search-paging").find_all('a', id = re.compile("rptPages")))
            except:
                break

            # page through the rest of the group
            for i in range(1, n_in_group):
                payload_paging = {
                    "__CMSCsrfToken": soup.find("input", id="__CMSCsrfToken")['value'],
                    "__VIEWSTATE": soup.find("input", id="__VIEWSTATE")['value'],
                    "__VIEWSTATEGENERATOR": soup.find("input", id="__VIEWSTATEGENERATOR")['value'],
                    "__EVENTTARGET": "p$lt$ctl04$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$rptPages$ctl0{:1}$lnbPage",
                    "lng": 'en-CA',
                    "manScript_HiddenField": manScript,
                    "p$lt$ctl04$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$hdnCurrentPage": 1
                    }
                payload_paging['__EVENTTARGET'] = payload_paging['__EVENTTARGET'].format(i)

                time.sleep(randint(1,3))
                r = s.post( url_paging, headers = headers_search.update(headers_paging), data = payload_paging )
                soup = BeautifulSoup(r.content, 'html.parser')
                #print("scraping", fsa, soup.find('div', class_ = 'doctor-search-count').find('div', class_ = 'text-align--right').text)
                scrape_doctors(soup)

                payload_paging['p$lt$ctl04$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$hdnCurrentPage'] += 1

            # stop if there's no more groups
            if soup.find(class_ = "aspNetDisabled next") != None:
                break

            # switch to the next group
            payload_paging['__EVENTTARGET'] = 'p$lt$ctl04$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$lnbNextGroup'
            time.sleep(randint(1,3))
            r = s.post( url_paging, data = payload_paging )
            soup = BeautifulSoup(r.content, 'html.parser')
            #print("next group, scraping", fsa, soup.find('div', class_ = 'doctor-search-count').find('div', class_ = 'text-align--right').text)


# scrape one fsa
"""doctors = {}
one_fsa = "K1C"
crawl_fsa( one_fsa )
with open( projectDir + '/data-raw/doctors-' + one_fsa + '.csv', 'w' ) as csv_file:
    writer = csv.writer(csv_file)
    for key, val in doctors.items():
        writer.writerow( [key, val] )
"""
# scrape big cities by fsa
cities = ['fsa_brampton', 'fsa_hamilton', 'fsa_london', 'fsa_mississauga', 'fsa_ottawa']

start_time = time.time()

for j, city in enumerate(cities):

    print( city, j+1, "of", len(cities) )

    with open( projectDir + '/data/' + city + '.pickle', 'rb') as f:
        fsas = pickle.load(f)

    # progress bar settings
    total = len(fsas) - 1
    k = 0

    for fsa in fsas:
        doctors = {}
        progress(k, total, status= 'scraping ' + fsa )

        with open( projectDir + '/data-raw/doctors-' + fsa + '.csv', 'w' ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow( ['city_name', 'fsa', 'CPSO', 'article'] )

            try:
                crawl_fsa( fsa )
                for key, val in doctors.items():
                    writer.writerow( [city, fsa, key, val] )
            except:
                #print( "no doctors in", fsa )
                writer.writerow( [city, fsa, "NA", "NA"] )

            finally:
                k += 1

        # blank link for progress bar
        print()

elapsed_time = time.time() - start_time
print(time.strftime("-- time elapsed for scrape: %H:%M:%S -- ", time.gmtime(elapsed_time)))
