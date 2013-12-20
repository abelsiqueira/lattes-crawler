#!/usr/bin/python2

from BeautifulSoup import BeautifulSoup
import urllib2
import re

verbose = False

# Jose Mario Martinez Perez (provavelmente maior rede no imecc)
queue = ["8543703316798123"] 

ql = 0
max_queue = 5
keywords = ["Estudos", "Optimization"]

done = []
data = {}
journals = {}

while len(queue) > 0:
    current = str(queue.pop())
    data[current] = {}
    if verbose:
        print "Loading data of " + current
    html_page = urllib2.urlopen("http://lattes.cnpq.br/" + current)
    soup = BeautifulSoup(html_page)

    # Nome do Pesquisador
    name = str(soup.findAll('h2', attrs={'class': 'nome'}))
    name = name.split('>')[1].split('<')[0]
    data[current]["name"] = name

    if verbose:
        print "Processando dados de " + name 

    # Periodicos
    artigos = soup.findAll('div', attrs={'class': 'artigo-completo'})
    num_artigos = 0
    for artigo in artigos:
        for keyword in keywords:
            if str(artigo.contents[3]).lower().find(keyword.lower()) > 0:
                num_artigos = num_artigos + 1
                continue

    data[current]["total_artigos"] = len(artigos)
    data[current]["match_artigos"] = num_artigos

    # Colaboradores (entram na fila)
    for link in soup.findAll('a', attrs={'href':
        re.compile("^http://lattes.cnpq.br/[0-9]")}):
        link = link.get('href').split('/')[-1]
        if not link in done:
            queue.append(link)

    done.append(current)
    ql = ql + 1
    if ql > max_queue:
        print "Queue too long"
        break

if verbose:
    for key in data.keys():
        print data[key]

total = 0
match = 0
for key in data.keys():
    total = total + data[key]["total_artigos"]
    match = match + data[key]["match_artigos"]

print "Total de Artigos: " + str(total)
print "Artigos com palavra chave [" + ','.join(keywords) + "]: " + str(match)
