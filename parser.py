
"""
FILE: skeleton_parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012

Skeleton parser for cs145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the xml files store dollar value amounts in 
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the xml files store dates/ times in the form 
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)
5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or 
is not of #PCDATA type)
6) A function to get all elements of a specific tag name that are children of a
given element
7) A function to get only the first such child

Your job is to implement the parseXml function, which is invoked on each file by
the main function. We create the dom for you; the rest is up to you! Get familiar 
with the functions at http://docs.python.org/library/xml.dom.minidom.html and 
http://docs.python.org/library/xml.dom.html

Happy parsing!
"""

import sys
from xml.dom.minidom import parse
from re import sub

columnSeparator = "<>"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
                'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


"""
Returns true if a file ends in .xml
"""
def isXml(f):
    return len(f) > 4 and f[-4:] == '.xml'


# DOM traversal
"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
    elements = []
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            elements.append(child)
    return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            return child
    return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
        return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
    if len(elem.childNodes) == 1:
        return pcdata(elem) 
    return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
    curElem = getElementByTagNameNR(elem, tagName)
    if curElem != None:
        return pcdata(curElem)
    return ''



# String formatting

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon] 
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)



# Initialize output files, one for each relation/table
item_file = open('item.dat', 'w')
category_file = open('category.dat', 'w')
user_file = open('user.dat', 'w')
bid_file = open('bid.dat', 'w')

# Write one line to the file corresponding to one tuple with the given attributes
# Attributes are written in order, separated by delimiter '<>'
def writeLine(dataFile, attributes):
    line = columnSeparator.join(attributes)
    dataFile.write(line)
    dataFile.write('\n')


def itemTuple(item):
    itemID = item.getAttribute('ItemID')
    sellerID = item.getElementsByTagName('Seller')[0].getAttribute('UserID')
    name = getElementTextByTagNameNR(item,'Name')
    currently = transformDollar(getElementTextByTagNameNR(item,'Currently'))
    buy_price = transformDollar(getElementTextByTagNameNR(item,'Buy_Price'))
    if (buy_price == ''): buy_price = 'NULL'
    first_bid = transformDollar(getElementTextByTagNameNR(item, 'First_Bid'))
    started = transformDttm(getElementTextByTagNameNR(item, 'Started'))
    ends = transformDttm(getElementTextByTagNameNR(item, 'Ends'))
    description = getElementTextByTagNameNR(item, 'Description')

    return [itemID, sellerID, name, currently, buy_price, first_bid, started, ends, description]

def sellerTuple(item, seller):
    sellerID = seller.getAttribute('UserID')
    rating = seller.getAttribute('Rating')
    location = getElementTextByTagNameNR(item, 'Location')
    country = getElementTextByTagNameNR(item, 'Country')
    return [sellerID, rating, location, country]

def bidTuple(bid):
    bidder = bid.getElementsByTagName('Bidder')[0]
    userID = bidder.getAttribute('UserID')
    rating = bidder.getAttribute('Rating')
    time = transformDttm(getElementTextByTagNameNR(bid, 'Time'))
    amount = transformDollar(getElementTextByTagNameNR(bid, 'Amount'))
    return [userID, rating, time, amount]


"""
Parses a single xml file. Currently, there's a loop that shows how to parse
item elements. Your job is to mirror this functionality to create all of the necessary SQL tables
"""
def parseXml(f):
    dom = parse(f) # creates a dom object for the supplied xml file
    """
    TO DO: traverse the dom tree to extract information for your SQL tables
    """

    Items = dom.getElementsByTagName('Item')
    sellers = []
    users = {}

    for item in Items:

        # write tuple into Item table
        item_tuple = itemTuple(item)
        itemID = item_tuple[0]
        writeLine(item_file, itemTuple(item))

        # write all tuples into Category table
        for node in item.getElementsByTagName('Category'):
            writeLine(category_file, [itemID, getElementText(node)])

        # get seller information
        seller = item.getElementsByTagName('Seller')[0]
        seller_tuple = sellerTuple(item, seller)
        sellerID = seller_tuple[0]

        # Keep track of previously encountered sellers
        if (sellerID not in sellers):
            sellers.append(sellerID)

            # If user is both bidder and seller, use seller data
            if (sellerID in users): del users[sellerID]
            
            # write tuple into User table
            writeLine(user_file, seller_tuple)


        # write all tuples into Bid table
        for bid in item.getElementsByTagName('Bid'):
            bid_tuple = bidTuple(bid)
            userID = bid_tuple[0]
            writeLine(bid_file, bid_tuple)

            # store bidderID for later processing
            if (userID not in sellers): users[userID] = bid_tuple[1]

    # after all items have been processed, write user tuples for
    # remaining bidderIDs that were not also sellerIDs
    for userID in users.keys():
        writeLine(user_file, [userID, users[userID], 'NULL', 'NULL'])



"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_parser.py <path to xml files>'
        sys.exit(1)
    # loops over all .xml files in the argument
    for f in argv[1:]:
        if isXml(f):
            parseXml(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
