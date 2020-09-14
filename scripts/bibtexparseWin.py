import bibtexparser

bibFile = '../pandoc/myPub.bib'
def generateBib(cv=False,htmlC=True,separateJCW=False,bibfile='../pandoc/myPub.bib'):#set false incase you dont want either one
    html=''
    htmlSeparated =''
    bibtex = ''
    htmlThesis=''
    htmlPatent=''
    htmlBook=''
    bibFile=bibfile
    dictJCW={'JHtml':'','JBib':'','CHtml':'','CBib':'','WHtml':'','WBib':''}
    dictJCWC = {'J':0,'C':0,'W':0}

    with open(bibFile,errors='ignore') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    print(bib_database.entries)

    def arrangeAuthors(authList):
        lsp = authList.split('and')
        authStr=''
        for entrye in lsp:
            auth = entrye.strip()
            #print(auth)
            if authStr!='':
                authStr+=', '
            if 'Sen, Sougata' in auth:
                authStr+='<me>Sougata Sen</me>'
            else:
                authStr+= entrye.split(',')[1].strip()+' '+entrye.split(',')[0].strip()
        return authStr

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
            elif ('Demo:') in entry['title'] or 'Poster:' in entry['title']:
                #put it in demo or poster
                continue
            print(cnt,entry['title'])
            link=''
            try:
                link = entry['url']
            except:
                try:
                    link = 'https://dx.doi.org/' + entry['doi']
                except:
                    print("XXXXXX")
                    print(entry['ID'])
                    continue

            if separateJCW:
                if entry['type'] == 'Journal':
                    dictJCWC['J'] = dictJCWC['J']+1
                    cnt = 'J'+str(dictJCWC['J'])
                elif entry['type'] == 'Conference':
                    dictJCWC['C'] = dictJCWC['C']+1
                    cnt = 'C'+str(dictJCWC['C'])
                else:
                    dictJCWC['W'] = dictJCWC['W']+1
                    cnt = 'W'+str(dictJCWC['W'])
            else:
                cnt=cnt+1


            if entry['title'].startswith('{'):
                entry['title']=entry['title'][1:]
            if entry['title'].endswith('}'):
                entry['title']=entry['title'][:-1]

            if separateJCW:
                toAddHtml = '<A id="bibTag" href=\''+link+'\'>['+cnt+']</a>&nbsp;'+arrangeAuthors(entry['author'])+', \"<paper>'+entry['title']+'</paper>\", '
                toAddBib = '\n\\hangindent=3em\\hangafter=1['+cnt+'.] '+arrangeAuthors(entry['author']).replace('<me>Sougata Sen</me>','\\textbf{Sougata Sen}')+'. \emph{'+entry['title']+'. }'
                print('Working on',entry)
                if entry['ENTRYTYPE']=='article':
                    if 'archiveprefix' in entry:
                        toAddHtml+=' '+entry['archiveprefix']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'.<BR>'
                        toAddBib+=entry['archiveprefix']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'. '
                    else:
                        toAddHtml+=' '+entry['journal']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'.<BR>'
                        toAddBib+=entry['journal']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'. '
                else:
                    toAddHtml+= ' In ' +entry['booktitle']+' ('+entry['series']+' '+entry['year']+').<BR>'
                    toAddBib+=' In ' +entry['booktitle']+' ('+entry['series']+' '+entry['year']+'). '

                toAddBib+='\\url{'+link+'}.\\vspace{0.1in} \n\n'
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
                    toAddHtml+='<a href=\''+entry['slides']+'\'><img src="images/slides.png" style="width: 55px;align:middle;"></a>'

                if abstract!='-':
                    toAddHtml+='<a data-toggle=\"collapse\" href=\"javascript:toggleDiv(\'P'+str(cnt)+'-abstract\')\">' \
                            '<img src=\"images/abstract.png\" style=\"width: 75px;align:middle;\"></a>' \
                            '<div id=\'P'+str(cnt)+'-abstract\' class=\'abstract\' style=\"display:none;margin:0 2.5% 0 ' \
                            '2.5%;padding:0 2.5% 0 2.5%\">'+entry['abstract'].replace('{\%}','%')+'</div></br>'

                if entry['type'] == 'Journal':
                    dictJCW['JHtml']=dictJCW['JHtml']+toAddHtml
                    dictJCW['JBib'] = dictJCW['JBib']+toAddBib
                elif entry['type'] == 'Conference':
                    dictJCW['CHtml']=dictJCW['CHtml']+toAddHtml
                    dictJCW['CBib'] = dictJCW['CBib']+toAddBib
                else:
                    dictJCW['WHtml']=dictJCW['WHtml']+toAddHtml
                    dictJCW['WBib'] = dictJCW['WBib']+toAddBib



            else:

                html+='<A id="bibTag" href=\''+link+'\'>[P'+str(cnt)+']</a>&nbsp;'+arrangeAuthors(entry['author'])+', \"<paper>'+entry['title']+'</paper>\", '
                bibtex+='\n\\hangindent=3em\\hangafter=1{'+arrangeAuthors(entry['author']).replace('<me>Sougata Sen</me>','\\textbf{Sougata Sen}')+'. \emph{'+entry['title']+'.}'
                print('Working on',entry)
                if entry['ENTRYTYPE']=='article':
                    if 'archiveprefix' in entry:
                        html+=' '+entry['archiveprefix']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'.<BR>'
                        bibtex+=entry['archiveprefix']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'. '
                    else:
                        html+=' '+entry['journal']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'.<BR>'
                        bibtex+=entry['journal']+'. '+entry['volume']+'('+entry['number']+'), '+entry['year']+'. '
                else:
                    html+= ' In ' +entry['booktitle']+' ('+entry['series']+' '+entry['year']+').<BR>'
                    bibtex+=' In ' +entry['booktitle']+' ('+entry['series']+' '+entry['year']+'). '
                bibtex+='\\url{'+link+'}.}'
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
                            '2.5%;padding:0 2.5% 0 2.5%\">'+entry['abstract'].replace('{\%}','%')+'</div></br>'

    print("______________________________\n\n\n")
    if separateJCW:
        html=' <!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge,chrome=1\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1\">    <meta http-equiv=\"Cache-Control\" content=\"no-cache, no-store, must-revalidate\" />' \
             '<meta http-equiv=\"Pragma\" content=\"no-cache\" /><meta http-equiv=\"Expires\" content=\"0\" />\n<title>Sougata Sen</title><link rel=\"icon\" href=\"images//favicon-32x32.png\"><link  rel=\"stylesheet\" href=\"css/style_2.0.0.css?v=2.0.2\" />' \
             '<link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"><link rel=\"stylesheet\" href=\"css/academicons.min.css\"/><link rel=\"stylesheet\" type=\"text/css\" href=\"css/basecss.css\">'\
            '<script src=\"js/jquery-3.3.1.min.js\"></script><script src=\"js/func.js\"></script><script>$(function(){$(\"#header\").load(\"commonHead_2.0.0.html\");});</script>\n</head>'\
             '\n<body><div class=\"clearfix fit mxn2\"><div class=\"col-10 px1 mx-auto\"><div class=\"\"><div class=\"overflow-hidden rounded\"><div class=\"flex flex-column\" style=\"min-height:100vh\">'\
            '<div id=\"header\" class=\"container clearfix col-10\" style=\"float: right;\"></div><div id=\"main\" class=\" clearfix\"><div class=\"col-11\"><h3 style=\"float: right;\">Jump to <a href=\"#thesis\"> Thesis</a>&nbsp;|&nbsp;<a href=\"#papers\">Journal, Conference and Workshop Publications</a>&nbsp;|&nbsp;<a href=\"#patents\">Patents</a>&nbsp;|&nbsp;<a href=\"#book\"> Book Chapters</a></h3></div><BR/><hr/>'\
            '<div class=\"col-11\" id=\"thesis\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Thesis</h2><A id=\"bibTag\" href=\"http://ink.library.smu.edu.sg/etd_coll_all/23/\">[T1]</A> <Me>Sougata Sen</Me>, \"<paper>Fusing mobile, wearable and infrastructure sensing for immersive daily lifestyle analytics</paper>\", Ph.D. thesis advised by Prof. Archan Misra, at School of Information Systems, Singapore Management University, 2017.'\
            '</div></div><div class=\"col-11\" id=\"papers\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Journal, Conference and Workshop Publication</h2>'
        html+='<h3 class=\"h3 upper\">Journals</h2>'+dictJCW['JHtml']+'<h3 class=\"h3 upper\">Conferences</h2>'+dictJCW['CHtml']+'<h3 class=\"h3 upper\">Workshops</h2>'+dictJCW['WHtml']
        html+='</div></div><div class=\"col-11\" id=\"patents\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Patents</h2><A id=\"bibTag\">[PT3]</A> Kumar Padmanabh, Puneet Gupta,<Me> Sougata Sen</Me>. <paper>System and method for forming application dependent dynamic data packet in wireless sensor networks</paper> (US Patent 8,588,192)<BR><BR><A id=\"bibTag\">[PT2]</A> Kumar Padmanabh, Adi M. R. Vanteddu, <Me>Sougata Sen</Me>, Amrit Kumar, Puneet Gupta, Lakshya Malhotra, Sunil Vuppala,<paper> Method and system for creating a virtual wireless sensor network</paper> (US Patent 8,649,298)<BR><BR><A id=\"bibTag\">[PT1]</A> <Me> Sougata Sen</Me>, Ketan Patil, Animikh Ghosh, Parag Chauhan, Kumar Padmanabh, <paper>Method and system to dynamically detect and form a master slave network</paper>. (US Patent 8,873,429)</div></div><div class=\"col-11\" id=\"book\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Book Chapter</h2><A id=\"bibTag\">[B1]</A> Kumar Padmanabh,<Me> Sougata Sen</Me>, Sanjoy Paul. <paper>ZigBee versus Other Protocols and Standards</paper>. In ZigBee® Network Protocols and Applications (pp. 301-344). Auerbach Publications.</div></div></div></div></div></div></div></div></body></html>'
        print(html)


        bibtex='\\section{Journal, Conference and Workshop Publications}\n'
        bibtex+='\\subsection{Journals}\n%\\begin{itemize-noindent} [label={}]\n'+dictJCW['JBib']+'\n%\\end{itemize-noindent}\n\\noindent\\rule{\\textwidth}{0.5pt}\n'
        bibtex+='\\subsection{Conferences}\n%\\begin{itemize-noindent} [label={}]\n'+dictJCW['CBib']+'\n%\\end{itemize-noindent}\n\\noindent\\rule{\\textwidth}{0.5pt}\n'
        bibtex+='\\subsection{Workshops}\n%\\begin{itemize-noindent} [label={}]\n'+dictJCW['WBib']+'\n%\\end{itemize-noindent}\n\\noindent\\rule{\\textwidth}{0.5pt}\n'
        bibtex+='\n\\section{Demos and Posters}\n\t\\begin{itemize-noindent} [label={}]\n\\item \\textbf{Sougata Sen}, Vigneshwaran Subbaraju, Archan Misra, Youngki Lee, and Rajesh Krishna Balan, \\emph{Demo: Smartwatch based Food Diary \\& Eating Analytics.} In Proceedings of the International Conference on Mobile Systems, Applications, and Services (Mobisys \'16). \\url{https://doi.org/10.1145/2938559.2938569}'\
        '\n\t\\item Meeralakshmi Radhakrishnan, Sharanya Eswaran, \\textbf{Sougata Sen}, Vigneswaran  Subbaraju, Archan Misra, and Rajesh Krishna Balan. \\emph{Demo: Smartwatch based shopping gesture recognition.} In Proceedings of the International Conference on Mobile Systems, Applications, and Services (Mobisys \'16). \\url{https://doi.org/10.1145/2938559.2938572}.'\
        '\n\t\\item \\textbf{Sougata Sen}, Dipanjan Chakraborty, Dipyaman Banerjee, Archan Misra, Nilanjan Banerjee, Vigneshwaran Subbaraju, and Sumit Mittal. \\emph{Poster: SHOP: Store Habits Of People.} In Workshop on Mobile Computing Systems and Applications (HotMobile \'14). \\url{http://www.hotmobile.org/2014/papers/posters/sen_shop.pdf}\n\\end{itemize-noindent}'
        print(bibtex)

    else:
        html=' <!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge,chrome=1\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1\">    <meta http-equiv=\"Cache-Control\" content=\"no-cache, no-store, must-revalidate\" />' \
             '<meta http-equiv=\"Pragma\" content=\"no-cache\" /><meta http-equiv=\"Expires\" content=\"0\" />\n<title>Sougata Sen</title><link rel=\"icon\" href=\"images//favicon-32x32.png\"><link  rel=\"stylesheet\" href=\"css/style_2.0.0.css?v=2.0.2\" />' \
             '<link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"><link rel=\"stylesheet\" href=\"css/academicons.min.css\"/><link rel=\"stylesheet\" type=\"text/css\" href=\"css/basecss.css\">'\
            '<script src=\"js/jquery-3.3.1.min.js\"></script><script src=\"js/func.js\"></script><script>$(function(){$(\"#header\").load(\"commonHead_2.0.0.html\");});</script>\n</head>'\
             '\n<body><div class=\"clearfix fit mxn2\"><div class=\"col-10 px1 mx-auto\"><div class=\"\"><div class=\"overflow-hidden rounded\"><div class=\"flex flex-column\" style=\"min-height:100vh\">'\
            '<div id=\"header\" class=\"container clearfix col-10\" style=\"float: right;\"></div><div id=\"main\" class=\" clearfix\"><div class=\"col-11\"><h3 style=\"float: right;\">Jump to <a href=\"#thesis\"> Thesis</a>&nbsp;|&nbsp;<a href=\"#papers\">Journal, Conference and Workshop Publications</a>&nbsp;|&nbsp;<a href=\"#patents\">Patents</a>&nbsp;|&nbsp;<a href=\"#book\"> Book Chapters</a></h3></div><BR/><hr/>'\
            '<div class=\"col-11\" id=\"thesis\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Thesis</h2><A id=\"bibTag\" href=\"http://ink.library.smu.edu.sg/etd_coll_all/23/\">[T1]</A> <Me>Sougata Sen</Me>, \"<paper>Fusing mobile, wearable and infrastructure sensing for immersive daily lifestyle analytics</paper>\", Ph.D. thesis advised by Prof. Archan Misra, at School of Information Systems, Singapore Management University, 2017.'\
            '</div></div><div class=\"col-11\" id=\"papers\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Journal, Conference and Workshop Publication</h2>'+html
        html+='</div></div><div class=\"col-11\" id=\"patents\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Patents</h2><A id=\"bibTag\">[PT3]</A> Kumar Padmanabh, Puneet Gupta,<Me> Sougata Sen</Me>. <paper>System and method for forming application dependent dynamic data packet in wireless sensor networks</paper> (US Patent 8,588,192)<BR><BR><A id=\"bibTag\">[PT2]</A> Kumar Padmanabh, Adi M. R. Vanteddu, <Me>Sougata Sen</Me>, Amrit Kumar, Puneet Gupta, Lakshya Malhotra, Sunil Vuppala,<paper> Method and system for creating a virtual wireless sensor network</paper> (US Patent 8,649,298)<BR><BR><A id=\"bibTag\">[PT1]</A> <Me> Sougata Sen</Me>, Ketan Patil, Animikh Ghosh, Parag Chauhan, Kumar Padmanabh, <paper>Method and system to dynamically detect and form a master slave network</paper>. (US Patent 8,873,429)</div></div><div class=\"col-11\" id=\"book\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Book Chapter</h2><A id=\"bibTag\">[B1]</A> Kumar Padmanabh,<Me> Sougata Sen</Me>, Sanjoy Paul. <paper>ZigBee versus Other Protocols and Standards</paper>. In ZigBee® Network Protocols and Applications (pp. 301-344). Auerbach Publications.</div></div></div></div></div></div></div></div></body></html>'

        print(html)


        print('-------------------------------------------------\n\n')
        bibtex='\\section{Journal, Conference and Workshop Publications}\n\\begin{itemize-noindent} [label={}]'+bibtex

        bibtex+='\n\\end{itemize-noindent}\\noindent\\rule{\\textwidth}{0.5pt}\n\n\\section{Demos and Posters}\n\t\\begin{itemize-noindent} [label={}]\n\\item \\textbf{Sougata Sen}, Vigneshwaran Subbaraju, Archan Misra, Youngki Lee, and Rajesh Krishna Balan, \\emph{Demo: Smartwatch based Food Diary \\& Eating Analytics.} In Proceedings of the International Conference on Mobile Systems, Applications, and Services (Mobisys \'16). \\url{https://doi.org/10.1145/2938559.2938569}'\
        '\n\t\\item Meeralakshmi Radhakrishnan, Sharanya Eswaran, \\textbf{Sougata Sen}, Vigneswaran  Subbaraju, Archan Misra, and Rajesh Krishna Balan. \\emph{Demo: Smartwatch based shopping gesture recognition.} In Proceedings of the International Conference on Mobile Systems, Applications, and Services (Mobisys \'16). \\url{https://doi.org/10.1145/2938559.2938572}.'\
        '\n\t\\item \\textbf{Sougata Sen}, Dipanjan Chakraborty, Dipyaman Banerjee, Archan Misra, Nilanjan Banerjee, Vigneshwaran Subbaraju, and Sumit Mittal. \\emph{Poster: SHOP: Store Habits Of People.} In Workshop on Mobile Computing Systems and Applications (HotMobile \'14). \\url{http://www.hotmobile.org/2014/papers/posters/sen_shop.pdf}\n\\end{itemize-noindent}'
        print(bibtex)

    if cv:
        f = open("pubs.txt", "w")
        f.write(bibtex)
        f.close()
    if htmlC:
        f = open("..\pubs.html", "w")
        f.write(html)
        f.close()

if __name__ == '__main__':
    generateBib(cv=True,htmlC=True,separateJCW=True)
