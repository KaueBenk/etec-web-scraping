import bs4 as bs
import requests
import csv
from os import mkdir, path, chdir, getcwd
from time import sleep
from sys import exit

# configurable variables
get_html_from_url = True
get_html_from_disk = False
auto_or_manual_url = int(input('Quer informar a URL manualmente ou prefere automaticamente?\n[1] - Manual\n[2] - Automático\nEscolha uma opção: '))
if auto_or_manual_url == 1:
    url = str(input('Informe a URL: '))
elif auto_or_manual_url == 2:
    ensino = int(input('Informe o código do tipo de ensino desejado: '))
    etec = str(input('Informe o código da ETEC desejada: '))
    varios_cursos = int(input('Quer pegar os dados de vários cursos?\n[1] - SIM\n[2] - NÃO\nEscolha uma opção: '))
    if varios_cursos == 1:
        curso = int(input('Informe o código do primeiro curso: '))
        url = f'https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino={ensino}&codetec={etec}&codescolacurso={curso}&n=&o=1'
    elif varios_cursos == 2:
        curso = int(input('Informe o código do curso desejado: '))
        url = f'https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino={ensino}&codetec={etec}&codescolacurso={curso}&n=&o=1'
    else:
        print('Esta opção nao exite.')
else:
    print('Esta opção nao exite.')
    
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
    url = f'https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino={ensino}&codetec={etec}&codescolacurso={curso}&n=&o=1'
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
    curso += 1
