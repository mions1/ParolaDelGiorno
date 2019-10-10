import urllib.request

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
    txt = txt.replace("&ugrave;", "ù")
    return txt

def delete_more_digit(txt):
    i = 0
    last_digit = None
    tmp_txt = ""
    
    for c in txt:
        if c.isdigit():
            i += 1
            last_digit = c
        else:
            if i == 1:
                tmp_txt += last_digit
            tmp_txt += c
            i = 0
        
    return tmp_txt
                
def get_source(url):
    with urllib.request.urlopen(url) as response: 
        source = response.read().decode('utf-8')
    return source

def get_main_source(source, src="zanichelli"):
    main_start = main_end = ""
    
    if src == "zanichelli":
        main_start = '<div class="main-content light-txt">'
        main_end = '</div>'
    elif src == "treccani":
        main_start = '<!-- module article full content -->'
        main_end = '<!-- end module -->'
    
    main_source = source[source.index(main_start):(source[source.index(main_start):]).index(main_end)+len(source[:source.index(main_start)])+len(main_end)]
    return main_source
    

def get_word(main_source):
    word_start = 'La parola di oggi è: '
    word_end = '\n'
    i = 2 if main_source.index(word_end) == 1 else 1
    word = main_source[main_source.index(word_start)+len(word_start):main_source.index(word_end,i)]
    return word

def get_meaning(main_source, src="zingarelli"):
    
    
    """
    mean_start = mean_end = ""
    
    if ">1" in main_source:
        mean_start = ">1 "
        mean_end = ">;"
    else:
        mean_start = ">) "
        mean_end = "</span><!--"
        
    mean = main_source[main_source.rindex(mean_start)+len(mean_start) : (main_source[main_source.rindex(mean_start):]).rindex(mean_end) + len(main_source[:main_source.rindex(mean_start)])+len(mean_end)]
    mean = special(delete_tag(mean))
    """
    special_char = ["|",";",".","(","[","#"]
    mean = ""
    if src == "zingarelli":
        main_start = '1 '
        tmp = main_source[main_source.index(main_start)+len(main_start):]
        for c in tmp:
            if c in  special_char:
                break
            mean += c
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
    
    return mean

url = "https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/"

url = "https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/cono/"

word = mean = ""

source = get_source(url)
main_source = get_main_source(source)
opt_main_source = delete_more_digit(special(delete_tag(main_source)))
word = get_word(opt_main_source)
#mean = get_meaning(opt_main_source)

print("La parola è: "+word)
print("Il significato è: "+mean)
print(delete_more_digit(special(delete_tag(main_source))))

#----------------TRECCANI

url = "http://www.treccani.it/vocabolario/puleggia/"
source = get_source(url)
main_source = get_main_source(source, "treccani")
mean = get_meaning(delete_tag(main_source), "treccani")

print("MEAN: "+mean)
