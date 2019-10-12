from handle_source import source_handler as sh

class Zanichelli(sh.SourceHandler):
    
    def __init__(self, url, word=None):
        super().__init__(url)
        self.word = word
        
    def init(self):
        self.set_main_source()
        self.set_opt_main_source()
        self.set_word()
        #self.set_meaning()
        #self.set_other_meaning()
        
        return True
        
    """ Funzione euristica, dovrebbe prendere la sezione principale della pagina,
        dove sono presenti i contenuti interessanti """
    def set_main_source(self):
        main_start = '<div class="main-content light-txt">'
        main_end = '</div>'
        
        main_source = self.source
        if main_start in self.source and main_end in self.source:
            main_source = self.source[self.source.index(main_start):(self.source[self.source.index(main_start):]).index(main_end)+len(self.source[:self.source.index(main_start)])+len(main_end)]
            
        self.main_source = main_source
        return main_source

    def set_opt_main_source(self):
        self.opt_main_source = super().delete_more_digit(super().replace_accent(super().delete_tag(self.main_source)))
        return self.opt_main_source

    def set_word(self):
        """ Funzione euristica, recupera il vocabolo di oggi
            
        Return:
            vocabolo del giorno
        """
        
        word_start = word_end = ""  # da dove inizia e finisce il vocabolo nella sorgente
        
        #In zanichelli la parola sta dopo la stringa word_start e finisce al primo \n dopo di esso
        word_start = 'La parola di oggi è: '
        word_end = '\n'
        i = 2 if self.opt_main_source.index(word_end) == 1 else 1    # elimina la possibilità che la prima riga della sorgente sia un \n
        word = self.opt_main_source[self.opt_main_source.index(word_start)+len(word_start):self.opt_main_source.index(word_end,i)]
            
        self.word = word
        return word
    
    def set_meaning(self):
        """ Funzione euristica, recupera il significato del vocabolo
            
        Return:
            definizione del vocabolo
        """
        special_char = ["|",";","(","[","#"]    # possono essere utili per trovare quando finisce il significato
        mean = ""
        
        #In zanichelli inizia spesso dopo '1 ' (ma non sempre, per questo sono passato a treccani) e finisce al primo carattere speciale
        main_start = '1 '
        tmp = self.opt_main_source[self.opt_main_source.index(main_start)+len(main_start):]
        for c in tmp:
            if c in  special_char:
                break
            mean += c
            
        self.mean = mean
        return mean
    
    def set_other_meaning(self):
        """ Funzione euristica, recupera il secondo significato (se c'è)
            
        Return:
            altro significato del vocabolo
        """
        special_char = ["|",";","(","[","#"]    # possono essere utili per trovare quando finisce il significato
        mean = ""
        
        #In zanichelli inizia spesso dopo '2 ' (ma non sempre, per questo sono passato a treccani) e finisce al primo carattere speciale
        main_start = '2 '
        tmp = self.opt_main_source[self.opt_main_source.index(main_start)+len(main_start):]
        for c in tmp:
            if c in  special_char:
                break
            mean += c
            
        self.mean2 = mean
        return mean
