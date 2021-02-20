import bs4 as bs
import requests
import csv
from os import mkdir, path, chdir, getcwd
from time import sleep
from sys import exit

# configurable variables
get_html_from_url = True
# ensino = int(input('Informe o código do tipo de ensino desejado: '))
# etec = int(input('Informe o código da etec desejada'))
url = f'https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino=4&codetec=015.00S&codescolacurso=1637&n=&o=1'
get_html_from_disk = False
file = 'Administração | Classificação geral.html'
max_lines = 60  # define te maximum number of lines in csv file

# getting html from site
def get_html_from_url(url):
    req = requests.get(url).content
    html = bs.BeautifulSoup(req, 'lxml')
    erro = html.find_all('p')
    erro = erro[2]
    erro = str(erro)[3:-4]
    if erro == 'Nenhum registro encontrado.':
        exit(erro)
    else: 
        return html  

# getting html from disk
def get_html_from_disk(file):
    html_doc = open(file, 'r').read()
    html = bs.BeautifulSoup(html_doc, 'lxml')
    return html

# creating directory
i = 0 # in Brazil we call this gambiarra or technical temporary permanent adjust. Without this, script create a folder inside a folder inside a folder...
def create_directory(dir_school, school):
    cwd = getcwd()
    if not path.exists(dir_school) and cwd != dir_school:
        mkdir(school)
        sleep(1)
        chdir(dir_school)
    else:
        chdir(dir_school)
    return

# loop
while True:
    if get_html_from_url:
        html = get_html_from_url(url)
    elif get_html_from_disk:
        html = get_html_from_disk(file)

    # getting course and school
    school = html.find('h3')
    course = html.find_all('h4')

    # formatting course and school
    school = str(school)[4:-5]
    dir_school = getcwd() + '/' + school
    course = course[1]
    course = str(course)[4:-5]

    # getting table_content
    table = html.find("table", attrs={'class': 'table table-bordered table-striped'})
    table_rows = table.find_all("tr")

    # variables
    max_lines += 1
    count = 0

    # creating directory and csv file if they doesn't exists
    if i == 0:
        create_directory(dir_school, school)
        i = 1
    arquivo = open(f'{course}.csv', 'x')

    # writing into csv file
    for tr in table_rows:
        td = tr.find_all(["th", "td"])
        row = [i.text for i in td]
        wr = csv.writer(arquivo, quoting=csv.QUOTE_ALL)
        wr.writerow(row)
        count += 1
        if count == max_lines:
            break
