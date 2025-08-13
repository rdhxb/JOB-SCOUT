import requests
from bs4 import BeautifulSoup

TARGET_URL = 'https://www.pracuj.pl/'

POSITION = str(input('Podaj stanowisko jakiego szukasz > ')).lower()
CITY = str(input('Podaj miasto  > ')).lower()
DISTANCE = int(input(f'podaj maksymalna odleglosc od {CITY} > '))
JOB_LEVEL = 'bedzie wybieral z listy bo bedzie dict np junior == 17 , mid == 4 itp. bo na pracuj pl tak jest i chuj '
TYPE_OF_CONTRACT = 'tak samo'
SHOW_SALLARY = 'input 0 - 1 wystaryczy i wtedy do url dodamy'
WORKLOAD = 'SAME'
REMOTE_TYPE = 'SAME'
PUBLISH_TIME = 'to kaloes dziwne sie ogarnie jak sie uda CLI zrobic wybierane to bedzie git'



if ' ' in POSITION:
    first, sec = POSITION.split(' ', 1)

    print(f'first = {first} sec = {sec}')
    TARGET_URL = f'{TARGET_URL}praca/{first}%20{sec};kw/{CITY};wp?rd={DISTANCE}&ao=false' #ao false to zeby bylo bezxposrednio od pracodawcy
else:
    TARGET_URL = f'{TARGET_URL}praca/{POSITION};kw/{CITY};wp?rd={DISTANCE}&ao=false'

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
# https://it.pracuj.pl/praca/administrator%20it;kw
# URL looks like 
# https://it.pracuj.pl/praca/ Stanowisko, slowo_klucz itp. ;kw/ miasto z malej ;wp/?rd = ilosc  kilometrow od 