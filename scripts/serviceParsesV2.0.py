import operator
#use serviceParseCV to create the files
serviceFile = '../data/services_v2.txt'
serviceKey = '../data/serviceKey.txt'
serviceAbbr ={}
serviceWeb = {}
serviceCV = {}
webOut = ''


'''Get all the services that exist'''
def parseServices():
    with open(serviceKey) as text:
        for txt in text:
            lsp = txt.split(',')
            serviceAbbr[lsp[0]]={"abbr":lsp[1],"pos":lsp[2].strip()}

def parseAndCreate():
    for ctr in serviceAbbr:
        serviceWeb[serviceAbbr[ctr]['abbr']] = {}
        serviceCV[serviceAbbr[ctr]['abbr']] = {}

    with open(serviceFile) as text:
        for txt in text:
            lsp = txt.split(',')
            getTheYears = lsp[3].strip().split(';')
            getYear = getTheYears[len(getTheYears)-1]
#            print(getYear,serviceWeb[lsp[0].strip()])
            if getYear in serviceWeb[lsp[0].strip()]:#year
                serviceWeb[lsp[0].strip()][getYear] = serviceWeb[lsp[0].strip()][getYear] + '\t<li><strong><a href=\"' + \
                                                      lsp[5]+'\">[' + \
                                                      lsp[2].strip()+ ']</a></strong>&nbsp;&nbsp;' + \
                                                      lsp[4].strip()+'.&nbsp;' + \
                                                      groupYears(lsp[3].strip())+'.'+\
                                                      ('<REV>External</REV></li>\n' if lsp[1].strip()=='E' else '</li>\n')
            else:
                # if lsp[0].strip() not in serviceWeb[lsp[0].strip()]:
                #     serviceWeb[lsp[0].strip()]={}
                serviceWeb[lsp[0].strip()][getYear] = '\t<li><strong><a href=\"' + \
                                                      lsp[5].strip() + '\">[' + \
                                                      lsp[2].strip() + ']</a></strong>&nbsp;&nbsp;' + \
                                                      lsp[4].strip() + '.&nbsp;' + \
                                                      groupYears(lsp[3].strip()) + '.' + \
                                                      ('<REV>External</REV></li>\n' if lsp[1].strip() == 'E' else '</li>\n')
#            serviceCV[lsp[0].strip()] = serviceCV[lsp[0].strip()]+''
def groupYears(yearList='2010;2013;2014;2015;2016;2018;2019;2021'):
    lsp = sorted(yearList.split(';'))
    output = ''
    startYear=-1
    lastYear =-1
    for ii in lsp:
        if startYear==-1:
            startYear=ii
            lastYear=ii
#        print(int(ii),startYear,int(lastYear),int(ii) - int(lastYear),int(lsp[len(lsp)-1]),int(ii),int(lsp[len(lsp)-1])==int(ii))
        if int(ii)-int(lastYear)>1:
#            print('IFFED',ii)
            if int(startYear)!=int(lastYear):
                output=output+startYear+'-'+lastYear+';'
            else:
                output = output + startYear+';'
            startYear=ii
            lastYear=ii
        if int(lsp[len(lsp) - 1]) == int(ii):
            if int(startYear)!=int(ii):
                output=output+startYear+'-'+ii
            else:
                output = output + startYear

        lastYear=ii
    return output



def organizeInOrder():
    webOut=''
    for i in sorted(serviceAbbr.keys()):
        webOut=webOut+'<div class="col-11"><div class="clearfix justified"><h2>'+serviceAbbr[i]['pos']+':</h2>\n'
#        print(webOut,serviceWeb[serviceAbbr[i]['abbr']])
        for j in sorted(serviceWeb[serviceAbbr[i]['abbr']],reverse=True):
            webOut=webOut+\
                   serviceWeb[serviceAbbr[i]['abbr']][j]
        webOut=webOut+'</div></div>'
    return webOut

def writeToFile(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()

parseServices()
#print(serviceAbbr)
parseAndCreate()
#print(serviceWeb)
serv = organizeInOrder()
print(serv)
writeToFile('../content-serv.html',serv)
#groupYears()
