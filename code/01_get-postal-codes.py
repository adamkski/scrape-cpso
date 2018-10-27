import requests
from bs4 import BeautifulSoup
import pickle
import re
import sys
import os
absFilePath = os.path.abspath(__file__)
fileDir = os.path.dirname(os.path.abspath(__file__))
projectDir = os.path.dirname(fileDir)


"""# toronto
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

post_code_list = [row.find('td').text for row in soup.find("table", class_ = "wikitable sortable").find_all('tr')[1:]]
post_code_list = set(post_code_list)

with open(projectDir + '/data/fsa_toronto.pickle', 'wb') as f:
    pickle.dump(post_code_list, f)"""

# brampton
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_L"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

codes = soup.find("table").find_all('td')
post_code_list = set([code.b.text for code in codes if re.match("Brampton", code.span.text)])

with open(projectDir + '/data/fsa_brampton.pickle', 'wb') as f:
    pickle.dump(post_code_list, f)

# mississauga
post_code_list = set([code.b.text for code in codes if re.match("Mississauga", code.span.text)])

with open(projectDir + '/data/fsa_mississauga.pickle', 'wb') as f:
    pickle.dump(post_code_list, f)

# hamilton
post_code_list = set([code.b.text for code in codes if re.match("Hamilton", code.span.text)])

with open(projectDir + '/data/fsa_hamilton.pickle', 'wb') as f:
    pickle.dump(post_code_list, f)

# ottawa
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_K"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

codes = soup.find("table").find_all('td')
post_code_list = set([code.b.text for code in codes if re.match("Ottawa", code.span.text)])

with open(projectDir + '/data/fsa_ottawa.pickle', 'wb') as f:
    pickle.dump(post_code_list, f)

# london
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_K"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

codes = soup.find("table").find_all('td')
post_code_list = set([code.b.text for code in codes if re.match("London", code.span.text)])

with open(projectDir + '/data/fsa_london.pickle', 'wb') as f:
    pickle.dump(post_code_list, f)
