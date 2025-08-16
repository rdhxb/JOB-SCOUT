import requests
from bs4 import BeautifulSoup
import csv

# TARGET_URL = 'https://sprzedaz.pracuj.pl/praca'
# TARGET_URL = 'https://inzynieria.pracuj.pl/praca'
TARGET_URL = 'https://it.pracuj.pl/praca'
# TARGET_URL = 'https://pracafizyczna.pracuj.pl/praca'
spec_fiz_worker = []
spec_sellers = []
spec_engineer = []
spec_it = []
try:
    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(response)
    # print(soup.prettify())

except:
    print(f'Error cannot connect to side {TARGET_URL}')

# can make it better but no need one time usage change and rerun if needed 
def take_specialization():
        spec = soup.find_all('div', class_='accordion with-label-background core_a39flr4')
        spec = spec[2]
        spec = spec.find('ul',class_='core_cpcfbp4')
        spec = spec.find_all('span',class_='core_okfuuwj')

        for span in spec:
            spec_it.append(span.text.strip())

             

take_specialization()

with open(f'data/spec/spec_it.csv','w',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerows([[item] for item in spec_it])  # one per line
