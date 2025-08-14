BASE_IT = "https://it.pracuj.pl/praca"

# 2) publish window (path segments must be URL-encoded)
PUBLISHED_PATH = {
    "24h": "/ostatnich%2024h;p,1",
    "3 dni": "/ostatnich%203%20dni;p,3",
    "7 dni": "/ostatnich%207%20dni;p,7",
    "14 dni": "/ostatnich%2014%20dni;p,14",
    "30 dni": "/ostatnich%2030%20dni;p,30",
}

# 3) work mode (path segments)
WORK_MODE_PATH = {
    "stacjonarna": "/praca%20stacjonarna;wm,full-office",
    "hybrydowa": "/praca%20hybrydowa;wm,hybrid",
    "zdalna": "/praca%20zdalna;wm,home-office",
    "mobilna": "/praca%20mobilna;wm,mobile",
}

# 5) contract -> tc
CONTRACT_TC = {
    "Umowa o prace": "0",
    "Umowa o dzielo": "1",
    "Umowa zlecenie": "2",
    "Kontrakt B2B": "3",
    "Umowa na zastepstwo": "4",
    "Umowa agencyjna": "5",
    "Umowa o prace tymczasowa": "6",
    "Umowa o staz/praktyki": "7",
}

# 6) workload -> ws
WORKLOAD_WS = {
    "pelny etat": "0",
    "Czesc etatu": "1",
    "dodatkowa/tymczasowa": "2",
}

SPEC_OVERRIDES = {
    "Full-stack": "fullstack",
    "Game dev": "gamedev",
    "Big Data / Data science": "big-data-science",
    "QA/Testing": "testing",
    "Product management": "product-management",
    "Project management": "project-management",
    "UX/UI": "ux-ui",
    "Buisness analytics": "business-analytics",
    "System analytics": "system-analytics",
    "SAP&ERP": "sap-erp",
    "IT admin": "it-admin",
    "AL/ML": "al-ml"
}










def process_answers(answers):
    base = BASE_IT
    path = ''

    loc = answers.get("location")
    if loc:
        path += f'/{loc.lower()};wp'

    publish = answers.get('published_within')
    if publish in PUBLISHED_PATH:
        path += f'/{PUBLISHED_PATH[publish]}'
    
    remot_type = answers.get('remote_type')
    if remot_type:
        remot_type_key = remot_type.lower()
        if remot_type_key in WORK_MODE_PATH:
            path += WORK_MODE_PATH[remot_type_key]

        
    print(f'Full path: {BASE_IT}{path}')


#     print("\n--- Your Answers ---")
# # dziala ale chyba trzeba bedzie zrovi dict i jednak IT fiz i tak dalej moaja jakies inne URl wiec tylko dla IT 
#     for q , ans in answers.items():
#         print(f"{q}: {ans}")

#         if ans == 'Warszawa':
#             URL += '/warszawa;wp'
#         elif ans == '3 dni':
#             URL += "/ostatnich%203%20dni;p,3"
#         print(URL)





    



# --- Your Answers ---
# job_type: IT
# specialization: Security
# location: Warszawa
# distance_km: 10
# remote_type: Stacjonarna
# contract_type: Umowa o prace
# workload: pelny etat
# show_salary_only: Nie
# published_within: 3 dni

# to dostane url 
# https://it.pracuj.pl/praca/warszawa;wp/ostatnich%203%20dni;p,3/praca%20stacjonarna;wm,full-office?rd=10&tc=0&ws=0&its=security

# kolejnosc
# baza dla spec_it https://it.pracuj.pl/praca/

# 1 miasto /krakow;wp
# 2 kiedy ostatnich%203%20dni;p,3
# 3 rodzaj pracy czy stacjonarna itp /praca%20stacjonarna;wm,full-office
# 4 kilosy ?rd=10
# 5 &tc=0 rodzaj umowy np o prace
# 6 &ws=0 pelny etat
# 7 &its=security spec

# legenda
# praca zdalna - /praca%20zdalna;wm,home-office
# praca hybrydowa - /praca%20hybrydowa;wm,hybrid
# praca stacjonarna - /praca%20stacjonarna;wm,full-office
# praca mobilna - /praca%20mobilna;wm,mobile

# spec :
# ?its=mobile etc.  azwa specjalizacji 
# ?its=big-data-science jako Big Data / Data science
# ?its=product-management jako product menager

# salary 
# ?sal=1 albo brak 

# rodzaj umowy 
# umowa o prace  - ?tc=0
# umowa o dzielo - ?tc=1
# umowa o zlecenie - ?tc=2
# kontrakt b2b - ?tc=3
# umowa na zastepstwo - ?tc=4
# umowa agencyjna - ?tc=5
# umowa o prace tymczasowa - ?tc=6
# umowa o staz/praktyki - ?tc=7


# wymiar pracy 
# czesc etatu - ?ws=1
# dodatkowa/ tymczasowa - ?ws=2
# pelny etat - ?ws=0


# czas publikacji 
# 24h - /ostatnich%2024h;p,1
# 3dni - /ostatnich%203%20dni;p,3
# 7dni - ostatnich%207%20dni;p,7
# 14dni - /ostatnich%2014%20dni;p,14
# 30dni - /ostatnich%2030%20dni;p,30