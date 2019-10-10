import urllib.request
import requests
from lxml import html
import re

"""
Delete every recurrence of seq in s.
Seq can be a regex
"""
def delete(s, seq):
    s = re.sub(seq, "", s)
    return s

"""
Text to delete
"""
def toDelete(n):
    #opening tag
    n = delete(n, '<EM>')
    n = delete(n, '<STRONG>')
    n = delete(n, '<SPAN CLASS=.{1,20}>')
    n = delete(n, '<annotation .{1,100}>')
    n = delete(n, '&.{1,7};')

    #closing tag
    n = delete(n,'</SPAN>')
    n = delete(n,'</STRONG>')
    n = delete(n,'</EM>')
    n = delete(n, '</annotation>')

    #other
    n = delete(n, '<!-- DEBUG -->')
    return n

"""
Other min fix to the text
"""
def optimization(n):
    #newline after reference word and get only first section
    i = 0
    for c in n:
        if c.isdigit() and c == '1':
            n = n[0:i]+'\n'+n[i:]
        if c.isdigit() and c=='2':
            n = n[0:i] #+'\n'+n[i:]
            break
        i = i+1

    #delete surplus spaces
    n = delete(n, "[\t]")

    return n

def delete_tag(txt):
    tmp = ""
    start = False
    for c in txt:
        if c == "<":
            start = True
            continue
        if c == ">":
            start = False
            continue
        if start == False:
            tmp += c
    return tmp

def special(txt):
    txt = txt.replace("&ograve;", "ò")
    txt = txt.replace("&egrave;", "è")
    txt = txt.replace("&igrave;", "ì")
    return txt

"""
Get an entry from treccani-vocabulary, get first definition and save it
in a file
"""
#word = 'amore'
#sito = ( str(urllib.request.urlopen("http://www.treccani.it/vocabolario/"+word+"/").read().decode('utf-8')) ).split('\n')

url_sign = "https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/"
with urllib.request.urlopen(url_sign) as response: 
    al = response.read().decode('utf-8')
  
main = '<div class="main-content light-txt">'

al_main = al[al.index(main):(al[al.index(main):]).index("</div>")+len(al[:al.index(main)])+6 ]

start='<p>La parola di oggi &egrave;: <strong>'
end = '</strong></p>'
parola = al_main[al_main.index(start)+len(start):al_main.index(end)]
print(parola)

#for line in al_main.split("</span>"):
    #print(line)

start_1 = ">1 "
end_1 = ">;"
al_sign_1 = al_main[al_main.index(start_1)+len(start_1) : (al_main[al_main.index(start_1):]).index(end_1)+len(al_main[:al_main.index(start_1)])+len(end_1) ]

print(special(delete_tag(al_sign_1)))
#significato_1 = al_main[al_main.index("<1 ")+3:al_main()]

#print(al)

#print(sito)

page = requests.get('https://unaparolaalgiorno.it/')
tree = html.fromstring(page.content)
#print(page.json())

"""
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://unaparolaalgiorno.it/')

html = driver.page_source
soup = BeautifulSoup(html,features="lxml")

h2 = soup.find_all("h2",) #class_="td1_normal_class")
p = soup.find_all("p")

frase_parola = None
for l in list(h2):
    l = str(l)
    if "</a>" in l:
        frase_parola = l[l.index("<a"):l.index("</h2>")]
        parola = frase_parola[frase_parola.index(">")+1:frase_parola.index("</")]
        break

for l in list(p):
    l = str(l)
    if "word-significato" in l:
        significato = l[l.index(">")+1:l.index("</")]

print(parola)
print(significato)
"""

#print (h2)

#f = open("dizionario.txt", 'w')
#str_tmp = sito[:]

#for n in str_tmp:
    #if "<SPAN CLASS='lemma'" in n:
        #n = toDelete(n)
        #n = optimization(n)
        #f.write(n)
        #f.write('\n')
        #break
#f.close()
