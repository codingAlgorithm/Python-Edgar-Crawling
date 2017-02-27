import urllib2, StringIO, sys, time
from lxml import etree

csvheaders = ['nameOfIssuer','titleOfClass','cusip','value','shrsOrPrnAmt/sshPrnamt','shrsOrPrnAmt/sshPrnamtType','investmentDiscretion',
    'votingAuthority/Sole','votingAuthority/Shared','votingAuthority/None']

genDate = time.strftime('%Y%m%d')

def find13FFile(tickerCIK,filingType):
    print 'Start to get the link'
    url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=%s&dateb=&owner=exclude&count=40&output=atom' % (tickerCIK,filingType)
    page = urllib2.urlopen(url).read()
    # Check if this file exists
    if not '<?xml' in page[:15]: sys.exit("Invalid CIK/Ticker.")
    # Parsing
    parsed = etree.parse(StringIO.StringIO(page))
    findSubstring = '{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}link'
    textUrlLink = parsed.find(findSubstring)
    if textUrlLink is not None:
        textUrlLink = textUrlLink.get('href')
        textUrlLink = textUrlLink.replace('-index.htm','.txt')
        return textUrlLink
    else:
        print 'txt file not found for ',filingType
        return None
