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
absFilePath = os.path.abspath(__file__)
fileDir = os.path.dirname(os.path.abspath(__file__))
projectDir = os.path.dirname(fileDir)

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

manScript = "%3b%3bAjaxControlToolkit%2c+Version%3d4.1.60919.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d28f01b0e84b6d53e%3aen-CA%3aee051b62-9cd6-49a5-87bb-93c07bc43d63%3a475a4ef5%3aeffe2a26%3a7e63a579"
manScript = manScript.replace( "%3b", ";" )
manScript = manScript.replace( "%2c", "," )
manScript = manScript.replace( "%3d", "=" )
manScript = manScript.replace( "%3a", ":" )
manScript = manScript.replace( "en-CA", "en-US")

def ping_specialization( city, special ):
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
    #            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$txtPostalCode": fsa,
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$ddCity": city,
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$grpGender":"+",
            #{}"p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$grpDocType":"rdoDocTypeAll",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$grpDocType": "rdoDocTypeSpecialist",
            "p$lt$ctl04$pageplaceholder$p$lt$ctl02$AllDoctorsSearch$ddSpecialist": special,
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

        # get doctor search result count
        time.sleep(randint(1,3))
        r = s.post(url_search, data = payload)
        soup = BeautifulSoup(r.content, 'html.parser')
        target = soup.find('div', class_ = "doctor-search-count").strong.text
        results[ special ] = re.search( "\d+", target ).group()

# list all specializations
specs = {}
with requests.Session() as s:
    r = s.get(url_search)
    soup = BeautifulSoup(r.content, 'html.parser')

    # get list of all specializations
    options = soup.find(id = 'ddSpecialist').find_all('option')

    for option in options :
        specs[ option['value'] ] = option.text

results = {}
ping_specialization( 1977, 119 )
ping_specialization( 1977, 151 )
print(results)
