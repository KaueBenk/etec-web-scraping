import bs4 as bs
import requests
import csv
from os import mkdir, path, chdir, getcwd
from time import sleep

while True:
    # configurable variables
    get_html_from_url = True
    url = input('Insira a URL:\n')
    get_html_from_disk = False
    file = 'Administração | Classificação geral.html'
    max_lines = 60  # define te maximum number of lines in csv file

    # getting html from site
    if get_html_from_url:
        req = requests.get(url).content
        html = bs.BeautifulSoup(req, 'lxml')
        erro = html.find('Nenhum registro encontrado.')
        if erro:
            print(erro)

    # getting html from disk
    if get_html_from_disk:
        html_doc = open(file, 'r').read()
        html = bs.BeautifulSoup(html_doc, 'lxml')

    # getting course and school
    school = html.find('h3')
    course = html.find_all('h4')

    # formatting course and school
    school = str(school)[4:-5]
    course = course[1]
    course = str(course)[4:-5]

    # getting table_content
    table = html.find("table", attrs={'class': 'table table-bordered table-striped'})
    table_rows = table.find_all("tr")

    # variables
    max_lines += 1
    count = 0

    # creating directory and csv file if they doesn't exists
    if getcwd != course:
        if path.exists(school) == False:
            folder = mkdir(school)
        chdir(school)
        arquivo = open(f'{course}.csv', 'x')
    else:
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
