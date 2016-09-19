from amazon.api import AmazonAPI
import requests
from bs4 import BeautifulSoup
import sys
import os
import os.path
reload(sys)
sys.setdefaultencoding('utf-8')
AMAZON_ACCESS_KEY = "xxxxxx"
AMAZON_SECRET_KEY = "xxxxxx"
AMAZON_ASSOC_TAG = "xxxxxx"
save_path="C:/"
completeName=os.path.join(save_path,"output.txt")
if os.path.isfile(completeName) and os.access(completeName, os.R_OK):
    os.remove(completeName)
else:
    print "File does not exist"
result=[]
amazon_searchProd = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region="US")
products_search = amazon_searchProd.search(Keywords='Books', SearchIndex='Books')
for i, product in enumerate(products_search):
    #print "{0}. '{1}'".format(i, product.title)
    #print "{0}. '{1}'".format(i, product.author)
    url= product.reviews[1]
    productTitle = product.title
    productAuthor = product.author
    if productTitle is None:
        productTitle = "No value"
    else:
        productTitle = productTitle
    if productAuthor is None:
        productAuthor = "No value"
    else:
        productAuthor = productAuthor
    result.append(productTitle)
    
    result.append(productAuthor)
    #result.append(",")
    r = requests.get(url)
    bs = BeautifulSoup(r.text)
    totalReviews = bs.findAll("div",{"class":"crIFrameNumCustReviews"})
    for reviewCount in totalReviews:
        reviewCountTot = reviewCount.findAll("a")
        for rev in reviewCountTot:
            reviewC = rev.contents[0].string
            #print reviewC
            if reviewC is None:
                reviewC=""
            else:
                reviewC=reviewC
            result.append(reviewC)
            
        reviewURL = reviewCount.find("a").get("href")
        result.append(reviewURL)
        
    g_data = bs.findAll("div", style = "margin-bottom:0.5em;")
    for nobr in g_data:
        reviewDates = nobr.findAll("nobr")
        for reviewDate in reviewDates:
            revDate = reviewDate.string
            
            #print (revDate)
            if revDate is None:
                revDate="No value"
            else:
                revDate= revDate
            
            result.append(revDate)
            
    result.append("\n")
myfile = open(completeName, 'a')
myfile.write("\n".join(result))
myfile.close()
