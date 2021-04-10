import operator
#use serviceParseCV to create the files
serviceFile = '../data/services.txt'
serviceKey = '../data/serviceKey.txt'
serviceAbbr ={}
serviceWeb = {}
serviceCV = {}


'''Get all the services that exist'''
def parseServices():
    with open(serviceKey) as text:
        for txt in text:
            lsp = txt.split(',')
            serviceAbbr[lsp[0]]={"abbr":lsp[1],"pos":lsp[2].strip()}

def parseAndCreate():
    for ctr in serviceAbbr:
        serviceWeb[ctr['abbr']]={}
        serviceCV[ctr['abbr']] = {}

    with open(serviceFile) as text:
        for txt in text:
            lsp = txt.split(',')
            if lsp[3].strip() in serviceWeb[lsp[0].strip()]:
                serviceWeb[lsp[0].strip()][lsp[3].strip()] = serviceWeb[lsp[0].strip()][lsp[3].strip()] + '\t<li><strong><a href=\"'+lsp[5]+'\">['+lsp[2].strip()+']</a></strong>&nbsp;&nbsp;'+lsp[4].strip()+'.&nbsp;'+lsp[3].strip()+'.'+'<REV>External</REV></li>\n' if lsp[1].strip()=='E' else '</li>\n'
            else:
                serviceWeb[lsp[0].strip()][lsp[3].strip()] = '\t<li><strong><a href=\"' + lsp[
                                                                 5] + '\">[' + lsp[
                                                                 2].strip() + ']</a></strong>&nbsp;&nbsp;' + lsp[
                                                                 4].strip() + '.&nbsp;' + lsp[
                                                                 3].strip() + '.' + '<REV>External</REV></li>\n' if lsp[
                                                                                                                        1].strip() == 'E' else '</li>\n'
#            serviceCV[lsp[0].strip()] = serviceCV[lsp[0].strip()]+''

parseServices()
print(serviceAbbr)
print(serviceWeb)