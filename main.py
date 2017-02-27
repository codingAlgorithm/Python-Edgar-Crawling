import sys
from FindTheFile import find13FFile
from Parse13FHRA import parse13FHRA
from parse13 import parse13


def main():
    #Parsing Argument
    if not sys.argv[1]: sys.exit("Script needs CIK/Ticker.")
    tickerCIK = sys.argv[1]
    filingTypes = ['13F-HR','13F-HR/A']
    for filingType in filingTypes:
        url = find13FFile(tickerCIK,filingType)
        if url is not None and filingType == '13F-HR/A': parse13FHRA(url,tickerCIK,filingType)
        if url is not None and filingType == '13F-HR': parse13(url,tickerCIK,filingType)
    print 'Done!'

if __name__ == '__main__':
    main()