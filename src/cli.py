# main.py
import typer
from InquirerPy import inquirer
from answers import process_answers
import csv

# ++++++++++++++++++++++++++++++++++++++++++++++++++
# poziom stanowika trzeba dodac do niektorysz spec 
# ++++++++++++++++++++++++++++++++++++++++++++++++++

app = typer.Typer()


spec_it = []
spec_fiz_worker = []

spec_sellers = []
spec_engineer = []

targets = {
    "spec_it": spec_it,
    "spec_fiz_worker": spec_fiz_worker,
    "spec_sellers": spec_sellers,
    "spec_engineer": spec_engineer,
}

for value, key in targets.items():
    with open(f'data/spec/{value}.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # non-empty
                key.append(row[0].strip())

# IT only for now 
job_type = ['IT']
location = ['Warszawa','Poznan','Krakow','Lodz','Wroclaw','Gdansk','Szczecin','Bydgoszcz']
distance = ['0','10','20','30','50']
contract_type = ['Umowa o prace','Umowa o dzielo','Umowa zlecenie', 'Kontrakt B2B']
show_salary = ['Tak','Nie']
workload = ['Czesc etatu','dodatkowa/tymczasowa','pelny etat']
remote_type = ['Stacjonarna','hybrydowa','zdalna','mobilna']
publish_time = ['24h','3 dni','7 dni', '14 dni','30 dni']



@app.command()
def ask():
# job type 
    jt = inquirer.fuzzy(
        message = 'Jaki rodzaj pracy wybierasz',
        choices = job_type
    ).execute()

    print(jt)

# Do zmiany bo po chuju elseif
    if jt == 'IT':
        spec = inquirer.fuzzy(
            message = 'Wybierz specjalizacje',
            choices = spec_it
        ).execute()
    elif jt == 'Paca Fizyczna':
        spec = inquirer.fuzzy(
            message = 'Wybierz specjalizacje',
            choices = spec_fiz_worker
        ).execute()
    elif jt == 'Sprzedaz':
        spec = inquirer.fuzzy(
            message = 'Wybierz specjalizacje',
            choices = spec_sellers
        ).execute()
    elif jt == 'Inzynieria':
        spec = inquirer.fuzzy(
            message = 'Wybierz specjalizacje',
            choices = spec_engineer
        ).execute()

    loc = inquirer.fuzzy("Lokalizacja:", choices=location).execute()
    dist = inquirer.select("Maksymalna odległość (km):", choices=distance).execute()
    remote = inquirer.select("Tryb pracy:", choices=remote_type).execute()
    contract = inquirer.select("Typ umowy:", choices=contract_type).execute()
    wl = inquirer.select("Wymiar etatu:", choices=workload).execute()
    salary = inquirer.select("Pokazywać tylko oferty z widełkami?", choices=show_salary).execute()
    pub = inquirer.select("Opublikowane w:", choices=publish_time).execute()

    answers = {
        "job_type": jt,
        "specialization": spec,
        "location": loc,
        "distance_km": dist,
        "remote_type": remote,
        "contract_type": contract,
        "workload": wl,
        "show_salary_only": salary,
        "published_within": pub,
    }

    
    return process_answers(answers)



if __name__ == "__main__":
    app()
