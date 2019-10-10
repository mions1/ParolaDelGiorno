import urllib.request

class MainIntentHandler():
    """Handler for Main Intent"""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MainIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        word, mean = self.main()
        speak_output = "La parola di oggi è: "+word
        speak_output += "\nChe significa: "+mean
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    
    def main(self):
        #-----------ZANICHELLI for word
        url = "https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/"
        source = self.get_source(url)
        main_source = self.get_main_source(source)
        opt_main_source = self.delete_more_digit(self.replace_accent(self.delete_tag(main_source)))
        
        word = self.get_word(opt_main_source)
        #------------TRECCANI for meaning
        url = "http://www.treccani.it/vocabolario/"+word+"/"
        source = self.get_source(url)
        main_source = self.get_main_source(source, "treccani")
        
        mean = self.get_meaning(self.delete_tag(main_source), word, "treccani")
        
        return word, mean
    
    def delete_tag(self, txt):
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
        for c in txt:
            if c == "<":
                start = True
                continue
            if c == ">":
                start = False
                continue
            if start == False:
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
                
    def get_source(self, url):
        """ Recupero la sorgente di una pagina web
        
        Parameters:
            url (str): url della pagina da recuperare
        
        Return:
            sorgente della pagina
        """
        with urllib.request.urlopen(url) as response: 
            source = response.read().decode('utf-8')
        return source
    
    def get_main_source(self, source, src="zanichelli"):
        """ Funzione euristica, dovrebbe prendere la sezione principale della pagina, dove è presente il vocabolo e la definizione
    
        Parameters:
            source (str): sorgente della pagina
            src (str): sito della sorgente (default: "zanichelli") (altri: "treccani", ) 
            
        Return:
            sorgente con solo la sezione principale
        """
        main_start = main_end = ""
        
        if src == "zanichelli":
            main_start = '<div class="main-content light-txt">'
            main_end = '</div>'
        elif src == "treccani":
            main_start = '<!-- module article full content -->'
            main_end = '<!-- end module -->'
        
        main_source = source[source.index(main_start):(source[source.index(main_start):]).index(main_end)+len(source[:source.index(main_start)])+len(main_end)]
        return main_source
        
    
    def get_word(self, main_source, src="zanichelli"):
        """ Funzione euristica, recupera il vocabolo di oggi
    
        Parameters:
            main_source (str): sorgente della pagina (in generale meglio se solo la sezione principale e se bonificata)
            src (str): sito della sorgente (default: "zanichelli") (altri: )
            
        Return:
            vocabolo del giorno
        """
        word_start = word_end = ""  # da dove inizia e finisce il vocabolo nella sorgente
        
        #In zanichelli la parola sta dopo la stringa word_start e finisce al primo \n dopo di esso
        if src=="zanichelli":
            word_start = 'La parola di oggi è: '
            word_end = '\n'
            i = 2 if main_source.index(word_end) == 1 else 1    # elimina la possibilità che la prima riga della sorgente sia un \n
            word = main_source[main_source.index(word_start)+len(word_start):main_source.index(word_end,i)]
            
        return word
    
    def get_meaning(self, main_source, word, src="treccani"):
        """ Funzione euristica, recupera il significato del vocabolo
        
        Parameters:
            main_source (str): sorgente della pagina (in generale meglio se solo la sezione principale e se bonificata)
            src (str): sito della sorgente (default: "treccani") (altri: "zanichelli")
            
        Return:
            vocabolo del giorno
        """
        special_char = ["|",";","(","[","#"]    # possono essere utili per trovare quando finisce il significato
        mean = ""
        
        #In zanichelli inizia spesso dopo '1 ' (ma non sempre, per questo sono passato a treccani) e finisce al primo carattere speciale
        if src == "zanichelli":
            main_start = '1 '
            tmp = main_source[main_source.index(main_start)+len(main_start):]
            for c in tmp:
                if c in  special_char:
                    break
                mean += c
        
        #In treccani inizia al primo carattere in maiuscolo dopo il trattino "–" e finisce al primo carattere speciale
        elif src == "treccani":
            trattino = upper = False
            for c in main_source:
                if trattino:
                    if upper:
                        if c in special_char:
                            break
                        mean += c
                    elif c.isupper():
                        upper = True
                        mean += c
                elif "–" in c:
                    trattino = True
            mean = mean.replace(word[0]+".", word)
        
        return mean
    
if __name__ == "__main__":
    m = MainIntentHandler()
    word, mean = m.main()
    print(word)
    print(mean)
