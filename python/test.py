import urllib.request
from handle_source import source_handler as sh
from handle_source.zanichelli import zanichelli as zanni
from handle_source.treccani import treccani as trecc
from handle_source.virgilio import virgilio as virgi

def get_words_from_file(file_name):
    words = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.replace("\n", "")
            line = line.replace("’", "")
            words.append(line)
    return words

def create_file_words(words, file_name="test/parole.txt", overwrite=True):
    words_list = []
    if overwrite:
        with open(file_name, "w+") as f:
            pass
    for word in words:
        if check_if_exists(word):
            with open(file_name, "a") as f:
                f.write(word+"\n")
                words_list.append(word)
    return words_list

def get_all(word):
    print(word)
    mean = mean2 = sinonimi = sinonimi2 = contrari = contrari2 = ""
    
    url_tre = "http://www.treccani.it/vocabolario/"+word+"/"
    tre = trecc.Treccani(url_tre, word)
    tre.init()

    #----------Treccani per sinonimi e contrari
    #url_sin = "http://www.treccani.it/vocabolario/"+word+"_(Sinonimi-e-Contrari)/"
    #source_sin = get_source(url_sin)
    #main_source_sin = get_main_source(source_sin, "treccani")
    #opt_main_source_sin = replace_accent(delete_tag(main_source_sin))

    #---------Virgilio per sinoni e contrari
    url_vir = "https://sapere.virgilio.it/parole/sinonimi-e-contrari/"+word
    vir = virgi.Virgilio(url_vir, word)
    vir.init()

    #sinonimi, contrari = get_sinonimi_contrari(opt_main_source_sin, "treccani")
    #sinonimi2, contrari2 = get_other_sinonimi_contrari(opt_main_source_sin, "treccani")
    mean, mean2 = tre.mean, tre.mean2
    sinonimi, contrari = vir.sins if vir.exists else "False", vir.cons if vir.exists else "False"
    fields = {"M":mean, "M2":mean2, "S":sinonimi, "C":contrari}
    return fields

def test(file_from="test/lista_bon.txt", file_to="test/parole.txt", log_file="test/log_test", crea_file=True):
    words = []
    if crea_file:
        parole = get_words_from_file(file_from)
        words = create_file_words(parole, file_to, True)
    else:
        words = get_words_from_file(file_to)
    words = ["eco"]
    with open(log_file,"w+") as f:
        pass
    for word in words:
        fields = get_all(word)
        with open(log_file,"a") as f:
            f.write(word+":\n")
            for key, value in fields.items():
                f.write(key+">"+value+"\n")
            f.write("\n\n\n")


#-------------------ZANICHELLI PER PAROLA
zan = zanni.Zanichelli("https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/")
zan.init()
print(zan.word)
#zan.set_main_source()
#zan.set_opt_main_source()
#zan.set_word()
#zan.set_meaning()

#-------------------TRECCANI PER SIGNIFICATO
tre = trecc.Treccani("http://www.treccani.it/vocabolario/"+zan.word+"/", zan.word)
tre.init()
#tre.set_main_source()
#tre.set_opt_main_source()
#tre.set_meaning()
#tre.set_other_meaning()

#-------------------VIRGILIO PER SINONIMI E CONTRARI
vir = virgi.Virgilio("https://sapere.virgilio.it/parole/sinonimi-e-contrari/"+zan.word, zan.word)
vir.init()
#vir.set_main_source()
#vir.set_opt_main_source()
#vir.set_sinonimi_contrari()


#---------------------VARIE PRINT
"""
print("Zanichelli:")
print(zan.main_source)
print(zan.opt_main_source)
print(zan.word)
print(zan.mean)
print("Treccani:")
print(tre.main_source)
print(tre.opt_main_source)
if tre.exists:
    print(tre.mean)
    print(tre.mean2)
print("Virgilio:")
print(vir.main_source)
print(vir.opt_main_source)
if vir.exists:
    print(vir.sins)
    print(vir.cons)
"""

#-----------------------Test
test(crea_file=False)
