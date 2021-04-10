import operator
#use serviceParseCV to create the files

def parseAndCreateForWebSite():
    tpc = {}
    rvw = {}
    web = {}
    sv = {}
    with open('../data/services.txt') as text:
        for txt in text:
            lsp = txt.split(',')
            if lsp[0].strip()=='TPC':
                temp = '\t<li><strong><a href=\"'+lsp[5]+'\">[' + lsp[2].strip() + ']</a></strong>&nbsp;&nbsp;' + lsp[4].strip() + '.&nbsp;' + lsp[3].strip() + '.</li>\n'
                if lsp[3].strip() in tpc:
                    temp=tpc[lsp[3].strip()]+temp
                tpc[lsp[3].strip()]=temp
            elif lsp[0].strip()=='RVW':
                temp = '\t<li><strong><a href=\"'+lsp[5]+'\">[' + lsp[2].strip() + ']</a></strong>&nbsp;&nbsp;' + lsp[4].strip() + '.&nbsp;' + lsp[3].strip() + '.'
                if lsp[1].strip()=='E':
                    temp+='<REV>External</REV>'
                temp+='</li>\n'
                if lsp[3].strip() in rvw:
                    temp=rvw[lsp[3].strip()]+temp
                rvw[lsp[3].strip()]=temp
            elif lsp[0].strip()=='WEB':
                temp = '\t<li><strong><a href=\"'+lsp[5]+'\">[' + lsp[2].strip() + ']</a></strong>&nbsp;&nbsp;' + lsp[4].strip() + '.&nbsp;' + lsp[3].strip() + '.</li>\n'
                if lsp[3].strip() in web:
                    temp=web[lsp[3].strip()]+temp
                web[lsp[3].strip()]=temp
            elif lsp[0].strip()=='SV':
                temp = '\t<li><strong><a href=\"'+lsp[5]+'\">[' + lsp[2].strip() + ']</a></strong>&nbsp;&nbsp;' + lsp[4].strip() + '.&nbsp;' + lsp[3].strip() + '.</li>\n'
                if lsp[3].strip() in sv:
                    temp=web[sv[3].strip()]+temp
                sv[lsp[3].strip()]=temp

    tpc=dict( sorted(tpc.items(), key=operator.itemgetter(0),reverse=True))
    rvw=dict( sorted(rvw.items(), key=operator.itemgetter(0),reverse=True))
    web=dict( sorted(web.items(), key=operator.itemgetter(0),reverse=True))
    sv=dict( sorted(sv.items(), key=operator.itemgetter(0),reverse=True))

    html=''
    html+='<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta http-equiv=\"X-UA-Compatible\" ' \
          'content=\"IE=edge,chrome=1\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, ' \
          'maximum-scale=1\"><meta http-equiv=\"Cache-Control\" content=\"no-cache, no-store, must-revalidate\" /><meta ' \
          'http-equiv=\"Pragma\" content=\"no-cache\" /><meta http-equiv=\"Expires\" content=\"0\" /><title>Sougata ' \
          'Sen</title><link rel=\"icon\" href=\"images//favicon-32x32.png\"><link  rel=\"stylesheet\" ' \
          'href=\"css/style_2.0.0.css\" /><link rel=\"stylesheet\" ' \
          'href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" ' \
          'integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" ' \
          'crossorigin=\"anonymous\"><link rel=\"stylesheet\" href=\"css/academicons.min.css\"/><link rel=\"stylesheet\" ' \
          'type=\"text/css\" href=\"css/basecss.css\"><script src=\"js/jquery-3.3.1.min.js\"></script><script>$(function(' \
          '){$(\"#header\").load(\"commonHead_2.0.0.html\");});</script></head><body><div class=\"clearfix fit ' \
          'mxn2\"><div class=\"col-10 px1 mx-auto\"><div class=\"overflow-hidden rounded\"><div class=\"flex ' \
          'flex-column\" style=\"min-height:100vh\">            <div id=\"header\" class=\"container clearfix col-10\" style=\"float: right;\"></div><div id=\"main\" class=\" clearfix\">'

    html+='<div class=\"col-11\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Program Committee Member</h2>\n<ul>\n'
    for vals in tpc:
        html+=tpc[vals]
    html+='</ul></div> </div>\n<div class=\"col-11\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Reviewer</h2>\n<ul>\n'
    for vals in rvw:
        html+=rvw[vals]
    html+='</ul></div> </div>\n<div class=\"col-11\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Web Chair</h2>\n<ul>\n'
    for vals in web:
        html+=web[vals]
    html+='</ul></div> </div>\n<div class=\"col-11\"><div class=\"clearfix justified\"><h2 class=\"h2 upper\">Student Volunteer</h2>\n<ul>\n'
    for vals in sv:
        html+=sv[vals]
    html+='</ul></div> </div>'
    html+=' </div></div></div></body></html>'

    file1 = open("../service.html","w")#write mode
    file1.write(html)
    file1.close()

    print(html)

# if __name__ == '__main__':
#     parseAndCreateForWebSite()

