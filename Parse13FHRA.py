import urllib2, StringIO, re, time
from lxml import etree

csvheaders = ['nameOfIssuer','titleOfClass','cusip','value','shrsOrPrnAmt/sshPrnamt','shrsOrPrnAmt/sshPrnamtType','investmentDiscretion',
    'votingAuthority/Sole','votingAuthority/Shared','votingAuthority/None']

genDate = time.strftime('%Y%m%d')

def parse13FHRA(url,tickerCIK,filingType):
    #Parse and output text file according to schema
    print 'Parsing text file for ',filingType,' ...'
    page = urllib2.urlopen(url).read()
    #We only care about the <S>...</Table> part
    fundHoldingsStart = list(re.finditer(r"<S>", page))[0].start()
    fundHoldingsEnd = list(re.finditer(r"</Table>",page))[0].end()
    #Parse the table
    fundHoldings = page[fundHoldingsStart:fundHoldingsEnd]
    cs = list(re.finditer(r"<C>", fundHoldings))
    #List to hold the positions of various datapoints
    cspos = [c.start() for c in cs]
    cspos.insert(0,0)
    #Output the text file
    docName = '13F-HRA'
    filename = docName+'_'+tickerCIK+'_'+genDate+'.txt'
    fileio = open(filename,'w')
    fileio.write(','.join(csvheaders))
    fileio.write('\n')
    for fundline in fundHoldings.split('\n')[1:-1]:
        for i in xrange(0,len(cspos)-1):
            point = fundline[cspos[i]:cspos[i+1]-1].strip()
            if len(point):
                fileio.write(point.replace(',','')+',')
            else:
                fileio.write(',')
        fileio.write('\n')
    fileio.close()