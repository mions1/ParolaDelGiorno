from handle_source import source_handler as sh

class Virgilio(sh.SourceHandler):
    
    def __init__(self, url, word):
        self.word = word
        self.main_source = ""
        self.opt_main_source = ""
        self.sins = ""
        self.cons = ""
        self.mean = ""
        self.exists = False
        super().__init__(url)
    
    def init(self):
        self.set_main_source()
        self.set_opt_main_source()
        self.check_if_exists()
        if not self.exists:
            return False
        self.set_sinonimi_contrari()
        self.set_meaning()
        
        return True
    
    """ Funzione euristica, dovrebbe prendere la sezione principale della pagina,
    dove sono presenti i contenuti interessanti """
    def set_main_source(self):
        main_start = '<div class="sct-descr">'
        main_end = "</div>"
        
        main_source = self.source
        if main_start in self.source and main_end in self.source:
            main_source = self.source[self.source.index(main_start):(self.source[self.source.index(main_start):]).index(main_end)+len(self.source[:self.source.index(main_start)])+len(main_end)]
            
        self.main_source = main_source
        return main_source

    def set_opt_main_source(self):
        self.opt_main_source = super().replace_accent(super().delete_brackets(super().delete_tag(self.main_source)))
        return self.opt_main_source
    
    def set_sinonimi_contrari(self):
        """ Funzione euristica, recupera i sinonimi del vocabolo.
            
        Return:
            sinonimi e contrari della parola
        """
        start = "Sinonimi"
        end = "Contrari"
        if start not in self.opt_main_source and end not in self.opt_main_source:
            self.sins = self.cons = ""
            return self.sins, self.cons
        if start in self.opt_main_source:
            if end in self.opt_main_source:
                sins = self.opt_main_source[self.opt_main_source.index(start)+len(start):self.opt_main_source.index(end)]
                cons = self.opt_main_source[self.opt_main_source.index(end)+len(end):]
            else:
                sins = self.opt_main_source[self.opt_main_source.index(start)+len(start):]
                cons = ""
        else:
            if end in self.opt_main_source:
                sins = ""
                cons = self.opt_main_source[self.opt_main_source.index(end)+len(end):]
         
        self.sins = sins
        self.cons = cons
        return sins, cons
    
    def set_meaning(self):
        start = "<li>"
        end = "</li>"
        if start not in self.main_source:
            self.mean = ""
        else:
            self.mean = "".join([c for c in self.main_source[self.main_source.index(start)+len(start):self.main_source.index(end)] ])
            
        return self.mean
    
    """ Controllo se la parola esiste nel dizionario """
    def check_if_exists(self):
        not_found = "Nessun risultato presente"
        if not_found in self.source:
            self.exists = False
            return False
        self.exists= True
        return True
