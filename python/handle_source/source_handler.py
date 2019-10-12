import urllib.request

class SourceHandler:
    
    def __init__(self, url):
        self.url = url
        self.source = self.get_source()
        
    def get_source(self):
        """ Recupero la sorgente di una pagina web
        
        Return:
            sorgente della pagina
        """
        with urllib.request.urlopen(self.url) as response: 
            source = response.read().decode('utf-8')
            
        return source
    
    def check_if_exists(self, url):
        return True
    
    def delete_tag(self, source):
        """ Elimina i tag html
        es. <span style="..." ...>ciao</span> -> ciao
        
        Parameters:
            source (str): sorgente della pagina html da "bonificare"
            
        Return:
            sorgente "bonificato"
        """
        new_source = "" # sorgente bonificato
        start = False   # se True vuol dire che ho trovato l'apertura di un tag (<) e non devo più salvare i caratteri
                        # se False invece salvo i caratteri
                        
        #Per ogni carattere nella sorgente controllo se è "<" o ">"
        # nel primo caso start prende True e fino a che è True non salvo i caratteri
        # nel secondo caso start prende False e da ora in poi posso riprendere a salvare i caratteri
        for c in source:
            if c == "<":
                start = True
                continue
            if c == ">":
                start = False
                continue
            if start == False:
                new_source += c
        return new_source

    def delete_brackets(self, source):
        """ Elimina le parentesi e ciò che c'è dentro
        
        Parameters:
            source (str): sorgente della pagina html da "bonificare"
            
        Return:
            sorgente "bonificato"
        """
        new_source = "" # sorgente bonificato
        start = ""   # prende la parentesi trovata o False
        open_brackets = ["(","[","{"] # i tipi di parentesi
        close_brackets = [")","]","}"]
                        
        #Per ogni carattere nella sorgente controllo se è "<" o ">"
        # nel primo caso start prende True e fino a che è True non salvo i caratteri
        # nel secondo caso start prende False e da ora in poi posso riprendere a salvare i caratteri
        for c in source:
            if c in open_brackets:
                if start in "":
                    start = c
            elif c in close_brackets:
                if open_brackets[close_brackets.index(c)] in start:
                    start = ""
            else:
                if start in "":
                    new_source += c
                    
        return new_source    

    def replace_accent(self, txt):
        """ Sostituisce la forma html degli accenti (es. &egrave;) con la relativa lettera accentata (es. è)
        
        Parameters:
            txt (str): testo su cui lavorare
            
        Return:
            testo modificato
        """
        chars = {"&ograve;":"ò", "&egrave;":"è", "&igrave;":"ì", "&ugrave;":"ù"} # dizionario degli accenti
        for key in chars:
            txt = txt.replace(key, chars[key])
        return txt

    def delete_more_digit(self, txt):
        """ Elimina i numeri quando ce ne sono di più consecutivi
        es. "142 ciao 1 co232me" -> " ciao 1 come"
        
        Parameters:
            txt (str): testo su cui lavorare
            
        Return:
            testo modificato
        """
        
        last_digit = None   # salvo l'ultimo numero incontrato, nel caso in cui devo salvarlo poiché non è seguito o preceduto da altre cifre
        i = 0   # se è 0 vuol dire che non ho ancora incontrato un numero
                # se è 1 vuol dire che ne ho incontrato solo 1, quindi và tenuto (salvato in last_digit)
                # se è > 1 vuol dire che ne ho incontrati di più, quindi non li salvo
        new_txt = ""
        
        #Per ogni carattere nel testo controllo se sia un numero
        # se è un numero, lo salvo in last_digit ed incremento i
        # se non è un numero, controllo se i > 0
        #   se è 1 allora vuol dire che prima ho incontrato un numero solo quindi lo salvo (da last_digit)
        #   se è > 1 allora vuol dire che i numeri incontrati prima non vanno salvati
        #   in ogni caso, continuo poi a salvare i nuovi caratteri fino al prossimo numero
        for c in txt:
            if c.isdigit():
                i += 1
                last_digit = c
            else:
                if i == 1:
                    new_txt += last_digit
                new_txt += c
                i = 0
            
        return new_txt

