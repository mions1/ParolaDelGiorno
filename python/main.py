import urllib.request
import sys
from handle_source import source_handler as sh
from handle_source.zanichelli import zanichelli as zanni
from handle_source.treccani import treccani as trecc
from handle_source.virgilio import virgilio as virgi

def header():
    """ Titolo del programma
    
    Return:
        Stringa da stampare come header
    """
    return "---------------PAROLA DEL GIORNO----------------"

def prints(zan, tre, vir, vir_mean):
    """ Stampa dei contenuti
    
    Parameters:
        zan (SourceHandler): variabile di classe che contiene la parola
        tre (SourceHandler): variabile di classe che contiente la definizione
        vir (SourceHandler): variabile di classe che contiene sinonimi e contrari
        
    Return:
        Stringa da stampare
    """
    s = ""
    
    word = zan.word
    if word == "":
        s = "Oggi la parola non è disponibile"
        return s
    
    #mean = tre.mean
    mean = vir_mean.mean
    #mean2 = tre.mean2
    sins = vir.sins
    cons = vir.cons
    
    s += "La parola di oggi è: "+word
    s += "\nDefinizione: "+mean if tre.exists else "\nDefinizione non disponibile"
    #s += "\nAltra definizione: "+mean2 if tre.exists and mean2 != "" else ""
    s += "\nSinonimi: "+sins if sins != "" else "\nNessun sinonimo trovato"
    s += "\nContrari: "+cons if cons != "" else "\nNessun contrario trovato"
    
    return s

if __name__ == "__main__":

    #-------------------ZANICHELLI PER PAROLA
    zan = zanni.Zanichelli("https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/")
    zan.init()

    #-------------------TRECCANI PER SIGNIFICATO
    tre = trecc.Treccani("http://www.treccani.it/vocabolario/"+zan.word+"/", zan.word)
    tre.init()

    #-------------------VIRGILIO PER SINONIMI E CONTRARI
    vir = virgi.Virgilio("https://sapere.virgilio.it/parole/sinonimi-e-contrari/"+zan.word, zan.word)
    vir.init()
    
    #-------------------VIRGILIO PER SIGNIFICATO
    vir_mean = virgi.Virgilio("https://sapere.virgilio.it/parole/vocabolario/"+zan.word, zan.word)
    vir_mean.init()

    print(header())
    print(prints(zan, tre, vir, vir_mean))
