import requests
from bs4 import BeautifulSoup

TARGET_URL = 'https://www.pracuj.pl/'

POSITION = str(input('Podaj stanowisko jakiego szukasz > ')).lower()
CITY = str(input('Podaj miasto  > ')).lower()
DISTANCE = int(input(f'podaj maksymalna odleglosc od {CITY} > '))

print(CITY)

TARGET_URL = f'{TARGET_URL}praca/{POSITION};kw/{CITY};wp?rd={DISTANCE}'
print(TARGET_URL)
try:
    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(response)
    # print(soup.prettify())

except:
    print(f'Error cannot connect to side {TARGET_URL}')




# https://it.pracuj.pl/praca/it;kw/warszawa;wp?rd=20
# https://it.pracuj.pl/praca/sales%20engineer;kw/lublin;wp?rd=30

# URL looks like 
# https://it.pracuj.pl/praca/ Stanowisko, slowo_klucz itp. ;kw/ miasto z malej ;wp/?rd = ilosc  kilometrow od 