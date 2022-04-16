import csv
import logging
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Union, List

import simplejson as json
from json import loads
import html


def userInputGetCookieValue() -> str:
    print("Gib den Wert des PHPSESSID Cookies einer aktiven Einlöse-Session ein:")
    while True:
        userinput = input()
        validateInputRegEx = re.compile(r"^[a-z0-9]{26}$").search(userinput)
        if validateInputRegEx:
            return userinput
        else:
            print("Ungueltige Eingabe!")


def doPostRequest(targetURL: str, postData: dict, thisheaders: dict) -> str:
    request = urllib.request.Request(targetURL, data=urllib.parse.urlencode(postData).encode(), headers=thisheaders)
    thisanswer = urllib.request.urlopen(request).read().decode()
    return thisanswer


def doGetRequest(targetURL: str) -> str:
    request = urllib.request.Request(targetURL)
    thisanswer = urllib.request.urlopen(request).read().decode()
    return thisanswer


def crawlShops(allCategories: List, shops: dict) -> dict:
    print("Crawling all shops inside categories")
    categoryIndex = 0
    for categoryInfo in categories:
        categoryID = categoryInfo[0]
        categoryName = html.unescape(categoryInfo[1]).strip()
        print("Crawling shops in category " + str(categoryIndex + 1) + " / " + str(len(categories)) + ": " + categoryName)
        print("Crawling " + categoryName + " ONLINE...")
        # Get all shops of this category which provide online usable vouchers
        updateShops(shops, categoryName, categoryID, True)
        # Get all shops of this category which can be used offline
        print("Crawling " + categoryName + " OFFLINE...")
        updateShops(shops, categoryName, categoryID, False)
        categoryIndex += 1
        if debugmode:
            break
        # Wait some time - don't crawl too obvious!
        time.sleep(2)

    # Now get all stores without category, each online- and offline
    print("Crawling shops without category ONLINE...")
    # Get all shops without category which can be used online
    updateShops(shops, None, None, True)
    print("Crawling shops without category OFFLINE...")
    # Get all shops without category which can be used offline
    updateShops(shops, None, None, False)
    # Get all shop URLs
    print("Crawling shop URLs and voucher values...")
    # shopIndex = 0
    shopNames = list(shops.keys())
    for shopIndex in range(len(shops)):
        shopname = shopNames[shopIndex]
        shop = shops.get(shopname)
        logging.info("Working on shop " + str(shopIndex + 1) + " / " + str(len(shops)) + ": " + shopname)
        shopRedeemName = shop.get("redeem_name")
        if "url" in shop:
            # Skip items that already contain an URL to speedup this process
            continue
        elif shopRedeemName is None:
            logging.warning("Cannot crawl shop information without redeem_name" + shopname)
            continue
        answer = doPostRequest("https://www.wunschgutschein.de/shops/1/" + shopRedeemName, {}, loggedinHeaders)
        jsonSrc = loads(answer)
        htmlSrc = jsonSrc["context"]["#content"]
        shopURLRegEx = re.compile(r"href=\"(https?://[^\"]+)\"[^>]*>\s*Im Shop stöbern").search(htmlSrc)
        if shopURLRegEx is not None:
            shop["url"] = html.unescape(shopURLRegEx.group(1))
        else:
            # This should never happen
            if "Jetzt spenden" in htmlSrc:
                # No shop to buy something but we can donate to some charity
                if "DMSG" in htmlSrc:
                    shop["url"] = "https://www.dmsg.de/spenden-und-helfen/"
                elif "Baker Tilly" in htmlSrc:
                    shop["url"] = "https://www.bakertilly.de/index.html"
                else:
                    # Use dummy URL
                    logging.info("Found new unknown donation possibility --> Using dummy URL for it")
                    shop["url"] = "https://www.spendenseite.de/"
            else:
                logging.warning("Failed to find shopURL --> Stopping!")
                break
        shopDescriptionRegEx = re.compile(r"content-margin-small\">(.*?)</div>\s*<strong>", re.DOTALL).search(htmlSrc)
        if shopDescriptionRegEx:
            shop["description"] = html.unescape(shopDescriptionRegEx.group(1).strip())
        else:
            # Not tragic but this should never happen nontheless!
            logging.warning("Failed to find shop description")
        shopRedeemableCardAmounts = shop.setdefault("redeemableCardValues", [])

        # Now find all possible card values
        foundAtLeastOneValue = False
        for possibleCardValueEuros in allRedeemableCardValues:
            # possibleCardValueCents = str(possibleCardValueEuros * 100)
            valueRegEx = re.compile(str(possibleCardValueEuros) + ",00\\s*€\\s*</option>").search(htmlSrc)
            if valueRegEx:
                foundAtLeastOneValue = True
                if possibleCardValueEuros not in shopRedeemableCardAmounts:
                    shopRedeemableCardAmounts.append(possibleCardValueEuros)
        foundAtLeastOneUnexpectedCardValue = False
        # 2021-05-21: E.g. required for shop "Gymondo" which has special values: 60, 80 while it doesn't have any of our expected values
        possibleAdditionalValues = re.compile(r"(\d+),00\s*€\s*</option>").findall(htmlSrc)
        foundAdditionalValues = []
        for possibleAdditionalValue in possibleAdditionalValues:
            possibleAdditionalValue = int(possibleAdditionalValue)
            if possibleAdditionalValue not in allRedeemableCardValues and possibleAdditionalValue not in foundAdditionalValues:
                # Collect extra amounts so we can log them later
                foundAdditionalValues.append(possibleAdditionalValue)
            # Now add the stuff we've missed before
            if possibleAdditionalValue not in shopRedeemableCardAmounts:
                shopRedeemableCardAmounts.append(possibleAdditionalValue)
        if not foundAtLeastOneValue and len(foundAdditionalValues) == 0:
            # This should never happen
            logging.warning("Failed to find ANY card value")
        elif len(foundAdditionalValues) > 0:
            logging.info("Found some additional card values: " + str(foundAdditionalValues))
        shopIndex += 1
        if debugmode and shopIndex > 2:
            break
        # Wait some time - don't crawl too obvious!
        time.sleep(2)
    return shops


def updateShops(thisshops: dict, thisCategoryName: Union[str, None], thisCategoryID: Union[str, None], isOnline: bool) -> None:
    """ Crawls all shops in given json/html code and adds information to given thisshops dict. """
    thishtml = getShopViewHTML(thisCategoryName, thisCategoryID, isOnline, True)
    if thishtml is None:
        # Skip empty categories/filters
        return
    shopInfos = re.compile("<div class=\"image\">\\s*<a href=\"([^\"]+)\" title=\"([^\"]+)\"").findall(thishtml)
    for shopInfo in shopInfos:
        shopRedeemURL = shopInfo[0]
        shopName = shopInfo[1]
        shopName = html.unescape(shopName)
        if shopName not in thisshops:
            thisshops[shopName] = {"name": shopName}
            print("!! Neuer Shop gefunden !!: " + shopName)
        thisshop = thisshops[shopName]
        # This is only available when we're logged in. Else shopRedeemURL == "#".
        shopReedemNameRegex = re.compile("/shops/1/([^/]+)").search(shopRedeemURL)
        if shopReedemNameRegex:
            thisshop["redeem_name"] = shopReedemNameRegex.group(1)
        else:
            logging.warning("Ungueltiges Cookie?? Konnte Shop redeem_name nicht finden für Shop: " + shopName)
            sys.exit(1)
        if isOnline:
            thisshop["usableOnline"] = True
        else:
            thisshop["usableOffline"] = True
        if thisCategoryName is None:
            realCategoryName = "KEINE"
            realCategoryID = -1
        else:
            realCategoryName = thisCategoryName
            realCategoryID = thisCategoryID
        shopCategoryNames = thisshop.setdefault("categories", [])
        shopCategoryIDs = thisshop.setdefault("categoryIDs", [])
        if realCategoryName not in shopCategoryNames:
            shopCategoryNames.append(realCategoryName)
        if realCategoryID not in shopCategoryIDs:
            shopCategoryIDs.append(realCategoryID)


def crawlFakeShops(allCategories: List, shops: dict) -> List:
    print("Crawling all fake shops inside categories")
    catIndex = 0
    fakeShops = []
    for catInfo in allCategories:
        catID = catInfo[0]
        catName = html.unescape(catInfo[1]).strip()
        print("Crawling fake shops in category " + str(catIndex + 1) + " / " + str(len(allCategories)) + ": " + catName)
        print("Crawling " + catName + " ONLINE...")
        # Get all shops of this category which provide online usable vouchers
        updateFakeShops(fakeShops, shops, catName, catID, True)
        # Get all shops of this category which can be used offline
        print("Crawling " + catName + " OFFLINE...")
        updateFakeShops(fakeShops, shops, catName, catID, False)
        catIndex += 1
        # Wait some time - don't crawl too obvious!
        time.sleep(2)

    # Now get all stores without category, each online- and offline
    print("Crawling fake shops without category ONLINE...")
    # Get all shops without category which can be used online
    updateFakeShops(fakeShops, shops, None, None, True)
    print("Crawling fake shops without category OFFLINE...")
    # Get all shops without category which can be used offline
    updateFakeShops(fakeShops, shops, None, None, False)
    return fakeShops


def updateFakeShops(fakeShops: List, shops: dict, thisCategoryName: Union[str, None], thisCategoryID: Union[str, None], isOnline: bool):
    thishtml = getShopViewHTML(thisCategoryName, thisCategoryID, isOnline, False)
    if thishtml is None:
        # Skip empty categories/filters
        return
    potentialFakeShopNames = re.compile("<a href=\"#\" title=\"([^\"]+)\"").findall(thishtml)
    for potentialFakeShopName in potentialFakeShopNames:
        potentialFakeShopName = html.unescape(potentialFakeShopName)
        if potentialFakeShopName not in shops and potentialFakeShopName not in fakeShops:
            logging.info("Found fake shop: " + potentialFakeShopName)
            fakeShops.append(potentialFakeShopName)


def getShopViewHTML(thisCategoryName: Union[str, None], thisCategoryID: Union[str, None], isOnline: bool, loggedIN: bool) -> Union[str, None]:
    postData = {"searchText": ""}
    if thisCategoryName is not None:
        postData["categories[]"] = thisCategoryID
    if isOnline:
        postData["redeemableOnline"] = "1"
    else:
        postData["redeemableOffline"] = "1"
    if loggedIN:
        thisanswer = doPostRequest(targetURL="https://www.wunschgutschein.de/einloesen/shopWall/1", postData=postData, thisheaders=loggedinHeaders)
    else:
        thisanswer = doPostRequest(targetURL="https://www.wunschgutschein.de/einloesen/shopWall/1", postData=postData, thisheaders=basicHeaders)
    thisjson = loads(thisanswer)
    thishtml = thisjson["context"]["#content"]

    if thisCategoryName is not None:
        # We need to filter out html else we might get stuff we dont want ("TOP AUSWAHL")!
        targetHTML = re.compile(r"shopWall suchtreffer(.+)", re.DOTALL).search(thishtml)
        if targetHTML:
            return targetHTML.group(1)
        else:
            # E.g. "Baby & Kind" + offline only --> No shops available!
            logging.info("Failed to find search results for category: " + thisCategoryName + " |isOnline=" + str(isOnline))
            return None
    return thishtml


def booleanToExcel(mybool: bool) -> str:
    if mybool:
        return "X"
    else:
        return ""


def getFormattedPassedTime(pastTimestamp: float) -> str:
    """ Returns human readable duration until given future timestamp is reached """
    # https://stackoverflow.com/questions/538666/format-timedelta-to-string
    secondsPassed = datetime.now().timestamp() - pastTimestamp
    # duration = datetime.utcfromtimestamp(secondsPassed)
    # return duration.strftime("%Hh:%Mm")
    return str(timedelta(seconds=secondsPassed))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# These are all possible "card" values e.g. 100 is not a card value but just indicates that for this shop, you could redeem e.g. max. 50€ voucher and top up to max. 100€
allRedeemableCardValues = [10, 15, 20, 25, 50, 100]
# These ones are the interesting possible card values for us
relevantRedeemableCardValues = [10, 15, 20, 25, 50]
basicHeaders = {"X-Requested-With": "XMLHttpRequest"}
loggedinHeaders = basicHeaders.copy()
debugmode = False

phpssid = userInputGetCookieValue()
# phpssid = "debugtest"
loggedinHeaders["Cookie"] = "PHPSESSID=" + phpssid

if debugmode:
    print("DEBUGMODE!!!")
timestampStart = datetime.now().timestamp()
htmlSrc = doGetRequest("https://www.wunschgutschein.de/einloesen/")
categories = re.compile("name=\"categories\\[\\]\" value=\"(\\d+)\" />([^>]+)</label>").findall(htmlSrc)

allShops = {}
# Load last state so we can crawl faster
if os.path.exists("shops.json"):
    print("Fahre fort mit vorheriger shops.json - das sollte den Crawlvorgang erheblich beschleunigen!")
    with open(os.path.join(os.getcwd(), "shops.json"), encoding='utf-8') as infile:
        allShops = json.load(infile)
else:
    print("Starte von null")

crawlShops(categories, allShops)

with open('shops.json', 'w') as outfile:
    json.dump(allShops, outfile)

with open('shops.csv', 'w', newline='') as csvfile:
    fieldnames = ['Shop', 'URL', 'Einlöseurl', 'Kategorien', 'Online', 'OfflineFiliale']
    for possibleCardValueEuros in relevantRedeemableCardValues:
        fieldnames.append("Kartenwert " + str(possibleCardValueEuros) + "€")
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for shopname, shop in allShops.items():
        columns = {'Shop': shopname, 'URL': shop.get("url", "WTF"),
                   'Einlöseurl': "https://www.wunschgutschein.de/shops/1/" + shop.get("redeem_name", "WTF"),
                   "Kategorien": shop["categories"],
                   'Online': booleanToExcel(shop.get("usableOnline", False)), 'OfflineFiliale': shop.get("usableOffline", False)
                   # TODO: Using "booleanToExcel" for "OfflineFiliale" will break our CSVs column headers? -.-
                   }
        foundCardValues = shop.get("redeemableCardValues", [])
        for possibleCardValue in relevantRedeemableCardValues:
            if possibleCardValue in foundCardValues:
                # columns["Kartenwert " + str(possibleCardValue)] = True
                columns["Kartenwert " + str(possibleCardValue) + "€"] = booleanToExcel(True)
            else:
                # columns["Kartenwert " + str(possibleCardValue)] = False
                columns["Kartenwert " + str(possibleCardValue) + "€"] = booleanToExcel(False)

        writer.writerow(columns)

# logging.info("Main crawler done - looking for 'fake shops'")
# fakeShops = crawlFakeShops(categories, allShops)
# with open('fakeShops.json', 'w') as outfile:
#     json.dump(fakeShops, outfile)

print("Total time required: " + getFormattedPassedTime(timestampStart))
print("DONE")
