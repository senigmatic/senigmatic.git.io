import operator
from serviceParser import parseAndCreateForWebSite
serviceFile = '../services.txt'
def parseAndCreateForCV(servFile='../services.txt'):
    vals={}
    serviceFile = servFile
    with open(serviceFile) as text:
        for txt in text:
            lsp = txt.split(',')
            lsp[3] = lsp[3].strip()
            if lsp[0].strip() == 'TPC':
                temp='\n\n\hangindent=1em \hangafter=0\n\\textbf{Program Committee: }'+lsp[2]+' '+lsp[3]+', '+lsp[4]+'.'
            elif lsp[0].strip() == 'RVW':
                temp = '\n\n\hangindent=1em \hangafter=0\n\\textbf{Reviewer: }' + lsp[2] + ' ' + lsp[3] + ', ' + lsp[4]+ ('. External.' if lsp[1]=='E' else '.')
            elif lsp[0].strip() == 'WEB':
                temp = '\n\n\hangindent=1em \hangafter=0\n\\textbf{Web Chair: }' + lsp[2] + ' ' + lsp[3] + ', ' + lsp[4] +'.'
            elif lsp[0].strip() == 'SV':
                temp = '\n\n\hangindent=1em \hangafter=0\n\\textbf{Student Volunteer: }' + lsp[2] + ' ' + lsp[3] + ', ' + lsp[4] + '.'
            #print(txt,'\t\t\t',temp)
            if lsp[3] in vals:
                temp = vals[lsp[3]] + temp
            vals[lsp[3]] = temp
    vals=dict( sorted(vals.items(), key=operator.itemgetter(0),reverse=True))
    print(vals.keys())
    f = open("cvService.txt", "w")
    for item in vals:
        print(vals[item])
        f.write(vals[item])
    f.close()

if __name__ == '__main__':
    parseAndCreateForCV()
    parseAndCreateForWebSite()



