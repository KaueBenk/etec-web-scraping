# Web Scraping with Python

When ETEC releases the classification list they remove it after some weeks, so if you want to know the grade needed to enter the course you need to save it on your computer.

So I made this script to facilitate saving the classification list of my interest courses.

## How to use

Open links.txt and paste the links of the courses you want to save the classification list, line by line with an enter at the end of each link in the following model:

```url
https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino=4&codetec=015.00S&codescolacurso=1639&n=&o=1
https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino=4&codetec=015.00S&codescolacurso=1643&n=&o=1
https://www.vestibulinhoetec.com.br/classificacao-final/lista.asp?ensino=4&codetec=015.00S&codescolacurso=1650&n=&o=1
```

Run "start.py" and watch your .csv files being created inside folders named with the school's name.

## Dependencies

* BeautifulSoup
* csv
* os
* requests
* time
