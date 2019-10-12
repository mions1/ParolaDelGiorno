from handle_source import source_handler as sh

class Treccani(sh.SourceHandler):
    
    def __init__(self, url, word):
        super().__init__(url)
        self.word = word
    
    def init(self):
        self.set_main_source()
        self.set_opt_main_source()
        self.check_if_exists()
        if not self.exists:
            return False
        self.set_meaning()
        self.set_other_meaning()
        
        return True
    
    """ Funzione euristica, dovrebbe prendere la sezione principale della pagina,
    dove sono presenti i contenuti interessanti """
    def set_main_source(self):
        main_start = '-- module article full content -->'
        main_end = '-- end module -->'
        
        main_source = self.source
        if main_start in self.source and main_end in self.source:
            main_source = self.source[self.source.index(main_start):(self.source[self.source.index(main_start):]).index(main_end)+len(self.source[:self.source.index(main_start)])+len(main_end)]
            
        self.main_source = main_source
        return main_source

    def set_opt_main_source(self):
        self.opt_main_source = super().replace_accent(super().delete_tag(self.main_source))
        return self.opt_main_source
    
    """ Funzione euristica, recupera il significato del vocabolo """
    def set_meaning(self):
        trattino = upper = False
        special_char = ["|",";","(","[","#"]    # possono essere utili per trovare quando finisce il significato
        mean = ""
        for c in self.opt_main_source:
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
        mean = mean.replace(self.word[0]+".", self.word)
        mean = mean.replace(self.word[0:2]+".", self.word)
        mean = mean.replace(self.word[0:3]+".", self.word)
        mean = mean.replace ("\n", "")
        
        self.mean = mean
        return mean
    
    """ Funzione euristica, recupera il secondo significato (se c'è) """
    def set_other_meaning(self):
        special_char = ["|",";","(","[","#"]    # possono essere utili per trovare quando finisce il significato
        start = "2. "
        mean = ""
        
        if start in self.opt_main_source:
            self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
        
        upper = False
        for c in self.opt_main_source:
            if c in special_char:
                break
            if not upper:
                if c.isupper():
                    upper = True
                    mean += c
            else:
                mean += c
        mean = mean.replace(self.word[0]+".", self.word)
        mean = mean.replace(self.word[0:2]+".", self.word)
        mean = mean.replace(self.word[0:3]+".", self.word)
        
        self.mean2 = mean
        return mean
    
    def get_sinonimi_contrari(self):
        """ Funzione euristica, recupera i sinonimi del vocabolo.
        
        Return:
            sinonimi e contrari della parola odierna
        """
        special_char = ["|",";",".","(",")","[","#"]    # possono essere utili per trovare quando finisce il significato
        sins = cons = ""
        
        #In treccani inizia al primo carattere in maiuscolo dopo il trattino "–" e finisce al primo carattere speciale
        #-------SINONIMI
        start = "≈"
        #start2 = "↔"
        if start in self.opt_main_source:
            self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
        #if start2 in main_source:
            #main_source = main_source[main_source.index(start2)+len(start2):]
        
        for c in self.opt_main_source:
            if c in special_char:
                break
            sins += c
        
        #--------CONTRARI
        start = "↔"
        
        if start in self.opt_main_source:
            self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
            if ")" in self.opt_main_source:
                self.opt_main_source = self.opt_main_source[self.opt_main_source.index(")")+1:]
        
        for c in self.opt_main_source:
            if c in special_char:
                break
            cons += c
            
        return sins, cons
    
    def get_other_sinonimi_contrari(self):
        """ Funzione euristica, recuperare altri sinonimi del vocabolo.
            
        Return:
            altri sinonimi e contrari della parola
        """
        special_char = ["|",";",".","(","[","#"]    # possono essere utili per trovare quando finisce il significato
        sins = cons = ""
        
        #In treccani inizia al primo carattere in maiuscolo dopo il trattino "–" e finisce al primo carattere speciale
        if src == "treccani":
            #-------SINONIMI
            start = "2. "
            if start in self.opt_main_source:
                self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
                
            start = "≈"
            start2 = "↔"
            if start in self.opt_main_source:
                self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
            if start2 in self.opt_main_source:
                self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start2)+len(start2):]
            
            for c in self.opt_main_source:
                if c in special_char:
                    break
                sins += c
            
            #--------CONTRARI
            start = "2. "
            if start in self.opt_main_source:
                self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
                
            start = "↔"
            if start in self.opt_main_source:
                self.opt_main_source = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
            
            for c in self.opt_main_source:
                if c in special_char:
                    break
                cons += c
        
        return sins, cons
    
    """ Controllo se la parola esiste nel dizionario """
    def check_if_exists(self):
        not_found = "La tua ricerca non ha prodotto risultati in nessun documento"
        if not_found in self.source:
            self.exists = False
            return False
        self.exists = True
        return True
