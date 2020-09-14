# import pkg_resources
# pkg_resources.require("future==0.14.3")
import bibtexparser


# Expected tags
# inproceedings -- url, author, title, booktitle, series, year
# article -- url, author, title, journal, volume, number, year

# optional tags
# inproceedings -- abstract, slides
# article -- abstract


html=''
htmlThesis=''
htmlPatent=''
htmlBook=''

with open('../pandoc/myPub.bib',errors='ignore') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)



def arrangeAuthors(authList):
    lsp = authList.split('and')
    authStr=''
    for entrye in lsp:
        auth = entrye.strip()
        if authStr!='':
            authStr+=', '
        if 'Sen, Sougata' in auth:
            authStr+='<me>Sougata Sen</me>'
        else:
            authStr+= entrye.split(',')[1].strip()+' '+entrye.split(',')[0].strip()
    return authStr

#print(bib_database.entries)

arranged={}
for entry in bib_database.entries:
    arrVal = []
    try:
        if entry['year'] in arranged:
            arrVal = arranged[entry['year']]
        arrVal.append(entry)
        arranged[entry['year']]=arrVal
    except:
        #print(entry)
        continue

years = sorted(arranged,reverse=True)
cnt =0
for year in years:
    print(arranged[year])
    for entry in arranged[year]:
        if entry['ENTRYTYPE']=='misc':
            #put it in the patent list
            continue
        elif entry['ENTRYTYPE']=='phdthesis':
            #put in thesis
            continue
        elif entry['ENTRYTYPE']=='incollection':
            #put in book chapter
            continue
        elif entry['title'].startswith('Demo:') or entry['title'].startswith('Poster:'):
            #put it in demo or poster
            continue
        link=''
        try:
            link = entry['url']
        except:
            print("XXXXXX")
            print(entry['ID'])
            continue

        cnt+=1
        html+='<A id="bibTag" href=\''+link+'\'>[P'+str(cnt)+']</a>&nbsp;'+arrangeAuthors(entry['author'])+', \"<paper>'+entry['title']+'</paper>\", '
        if entry['ENTRYTYPE']=='article':
            html+=' '+entry['journal']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'.<BR>'
        else:
            html+= ' In ' +entry['booktitle']+' ('+entry['series']+').<BR>'

        abstract='-'
        slides='-'
        try:
            abstract=entry['abstract']
        except:
            print('Error in abstract')

        try:
            slides=entry['slides']
        except:
            print('Error in slides')

        if slides!='-':
            html+='<a href=\''+entry['slides']+'\'><img src="images/slides.png" style="width: 55px;align:middle;"></a>'

        if abstract!='-':
            html+='<a data-toggle=\"collapse\" href=\"javascript:toggleDiv(\'P'+str(cnt)+'-abstract\')\">' \
                    '<img src=\"images/abstract.png\" style=\"width: 75px;align:middle;\"></a>' \
                    '<div id=\'P'+str(cnt)+'-abstract\' class=\'abstract\' style=\"display:none;margin:0 2.5% 0 ' \
                    '2.5%;padding:0 2.5% 0 2.5%\">'+entry['abstract']+'</div></br>'

print("______________________________\n\n\n")
print(html)