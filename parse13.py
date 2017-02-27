import urllib2, StringIO, re, time
from lxml import etree

csvheaders = ['nameOfIssuer','titleOfClass','cusip','value','shrsOrPrnAmt/sshPrnamt','shrsOrPrnAmt/sshPrnamtType','investmentDiscretion',
    'votingAuthority/Sole','votingAuthority/Shared','votingAuthority/None']

genDate = time.strftime('%Y%m%d')


def parse13(url,tickerCIK,filingType):
    #Parse and output text file according to schema
    print 'Parsing text file for ',filingType,' ...'
    page = urllib2.urlopen(url).read()
    #We only care about the <XML>...</XML> part
    fundHoldingsStart = list(re.finditer(r"<XML>", page))[1].start()
    fundHoldingsEnd = list(re.finditer(r"</XML>",page))[1].end()
    fundHoldings = page[fundHoldingsStart:fundHoldingsEnd]
    #lxml parsing
    dataparse = etree.parse(StringIO.StringIO(fundHoldings))
    #Xpaths we need
    path = "/XML/*[local-name()='informationTable']/*[%s]/*[local-name()='%s']"
    path2= "/XML/*[local-name()='informationTable']/*[%s]/*[local-name()='%s']/*[local-name()='%s']"
    #Count the number of holdings
    infoTableNodeCount = int(dataparse.xpath("count(/XML/*[local-name()='informationTable']/*[local-name()='infoTable'])"))
    #Output the text file
    docName = '13FHR'
    filename = docName+'_'+tickerCIK+'_'+genDate+'.txt'
    fileio = open(filename,'w')
    fileio.write(','.join(csvheaders))
    for infoTableNodeNum in xrange(0,infoTableNodeCount+1):
        for csvheader in csvheaders:
            if '/' not in csvheader:
                xpath = path % (str(infoTableNodeNum),csvheader)
            else:
                csvSplit = csvheader.split('/')
                xpath = path2 % (str(infoTableNodeNum),csvSplit[0],csvSplit[1])
            for elem in dataparse.xpath(xpath):
                fileio.write(elem.text+',')
        fileio.write('\n')
    fileio.close()



