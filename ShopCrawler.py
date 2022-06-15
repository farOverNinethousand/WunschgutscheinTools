import csv
import logging
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Any

import simplejson as json
from json import loads

API_BASE = "https://einloesen.wunschgutschein.de/api"
basicHeaders = {"X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
PATH_SHOPS_JSON = "shops.json"
PATH_SHOPS_RAW_JSON = "shops_raw.json"
# These ones are the interesting/most common possible card values
relevantRedeemableCardValues = [10, 15, 20, 25, 50, 100]
debugmode = True


def doPostRequest(targetURL: str, postData: dict, thisheaders: dict) -> str:
    request = urllib.request.Request(targetURL, data=urllib.parse.urlencode(postData).encode(), headers=thisheaders)
    thisanswer = urllib.request.urlopen(request).read().decode()
    return thisanswer


def doGetRequest(targetURL: str) -> str:
    request = urllib.request.Request(targetURL)
    thisanswer = urllib.request.urlopen(request).read().decode()
    return thisanswer


def callAPI(path: str, returnJson: bool = True) -> Any:
    """ Performs API request. """
    request = urllib.request.Request(API_BASE + path, headers=basicHeaders)
    response = urllib.request.urlopen(request).read().decode()
    if returnJson:
        return loads(response)
    else:
        return response


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


def isCardValuePossible(shop: dict, cardValueEUR: int) -> bool:
    voucherValues = shop.get('voucherValues', [])
    for possibleCardValue in relevantRedeemableCardValues:
        cardValuePossible = False
        for voucherValue in voucherValues:
            valueInCent = voucherValue['valueInCent']
            if valueInCent == possibleCardValue * 100:
                return True
    return False


def isRelevantCardValue(cardValueCent: int) -> bool:
    if (cardValueCent / 100) in relevantRedeemableCardValues:
        return True
    else:
        return False


def saveJson(obj, path):
    with open(path, 'w') as ofile:
        json.dump(obj, ofile)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    canReUseExistingDatabase = os.path.exists(PATH_SHOPS_JSON) and 'allow_update_shops' in sys.argv
    if debugmode:
        print("DEBUGMODE!!!")
    if 'skip_vpn_warning' not in sys.argv:
        if canReUseExistingDatabase:
            print("Existierende " + PATH_SHOPS_JSON + " wird verwendet!")
        print("Hinweis: Es wird empfohlen einen VPN zu verwenden, bevor du dieses Script durchlaufen lässt!")
        print("Falls du nach dem Crawlvorgang mit derselben IP zeitnah Gutscheine einlöst, könnte es zu Sperrungen kommen!")
        print("ENTER = Fortfahren")
        input()
        print("Let's go!")
    timestampStart = datetime.now().timestamp()
    # Crawl all categories and make a mapping
    categoriesList = callAPI('/shop/categories/1')
    # TODO: Find out why category 31 is missing in the API response we get
    categoriesList.append({'id': 31, 'name': 'Restaurant', 'slug': 'Lokalhelden'})
    categoriesMapping = {}
    for category in categoriesList:
        categoriesMapping.setdefault(category['id'], category)
    # Save categories mapping as json file
    saveJson(categoriesMapping, 'categories.json')
    # Get list of basic shop information
    crawledShopsRawOriginal = callAPI('/shop/wall/1?onlyWithLogo=1')
    crawledShopsRaw = crawledShopsRawOriginal.copy()
    # Save as json for later offline examination
    saveJson(crawledShopsRaw, PATH_SHOPS_RAW_JSON)

    shopIDsToUpdate = []
    storedShops = []
    if canReUseExistingDatabase:
        # Load last state so we can crawl faster
        print("Vorherige " + PATH_SHOPS_JSON + " gefunden. Es werden nur neue Shops gecrawlt, Informationen bestehender werden nicht aktualisiert!!")
        with open(os.path.join(os.getcwd(), PATH_SHOPS_JSON), encoding='utf-8') as infile:
            storedShops = json.load(infile)
        newShops = []
        for currentShop in crawledShopsRaw:
            currentShopID = currentShop['id']
            foundShop = False
            for storedShop in storedShops:
                if storedShop['id'] == currentShopID:
                    foundShop = True
                    break
            if not foundShop:
                print("SHOP_NEW: " + currentShop['name'] + " | ID: " + str(currentShopID))
                shopIDsToUpdate.append(currentShopID)
                newShops.append(currentShop)
        print("Number of new shops: " + str(len(newShops)))
        # Continue with old dataset now that we know which shops need re-crawl
        crawledShopsRaw = storedShops
        crawledShopsRaw += newShops
    else:
        # Add all shopIDs to list so we will update data of all shops
        for currentShop in crawledShopsRaw:
            shopIDsToUpdate.append(currentShop['id'])
    # Beautify some data so in the end we got one json that contains everything
    for shop in crawledShopsRaw:
        categoryIDs = shop['categories']
        categoriesHumanReadable = []
        for categoryID in categoryIDs:
            categoriesHumanReadable.append(categoriesMapping[categoryID]['name'])
        shop['categories_human_readable'] = categoriesHumanReadable
        voucherValues = shop.get('voucherValues', [])
        otherCardValues = []
        for voucherValue in voucherValues:
            valueInCent = voucherValue['valueInCent']
            if not isRelevantCardValue(valueInCent):
                otherCardValues.append(valueInCent / 100)
        shop['voucherValuesMisc'] = otherCardValues

    # Collect detailed info for all shops - will may take some time
    print('Crawling details of shops: ' + str(len(shopIDsToUpdate)))
    progress = 1
    shops = []
    for shop in crawledShopsRaw:
        shopID = shop['id']
        if shopID in shopIDsToUpdate:
            print("Working on shop " + str(progress) + " / " + str(len(shopIDsToUpdate)))
            extendedShopInfo = callAPI('/shop/' + str(shopID))
            # Merge both dicts so we got all shop information in one dict
            shops.append({**shop, **extendedShopInfo})
            progress += 1
            if progress >= 4 and debugmode:
                break
        else:
            # Append old dataset without updating it
            shops.append(shop)

    # Check for possible new fields
    for shop in shops:
        redeemable = shop['redeemable']
        redeemableKnownFields = ['REDEEMABLE_ONLINE', 'REDEEMABLE_BRANCH']
        for redeemableStatus in redeemable:
            if redeemableStatus not in redeemableKnownFields:
                print("Found new redeemable field: " + redeemableStatus)

    # Save shop information as json file
    saveJson(shops, PATH_SHOPS_JSON)

    # Look for deleted shops (only possible if we got data from previous crawl process)
    for oldShop in storedShops:
        foundShop = False
        oldShopID = oldShop['id']
        for shop in crawledShopsRawOriginal:
            if shop['id'] == oldShopID:
                foundShop = True
                break
        if not foundShop:
            print('SHOP_DELETED: ' + str(oldShopID) + ' | ' + oldShop['name'] + ' | ' + oldShop['link'])

    # Create csv file with most relevant human readable results
    ignoreInactiveShopsInCSV = 'csv_skip_inactive_shops' in sys.argv
    skippedInactiveShops = []
    with open('shops.csv', 'w', newline='') as csvfile:
        # TODO: Add column "Beschreibung" but atm this will fuck up our CSV formatting, maybe we need to escape that String before
        fieldnames = ['Shop', 'Beschreibung_net_fertig', 'URL', 'Einlöseurl', 'Kategorien', 'Online', 'OfflineFiliale']
        for possibleCardValueEuros in relevantRedeemableCardValues:
            fieldnames.append("Kartenwert " + str(possibleCardValueEuros) + "€")
        fieldnames.append("Sonstige Kartenwerte")
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for shop in shops:
            if ignoreInactiveShopsInCSV and not shop['active']:
                skippedInactiveShops.append(shop)
                continue
            redeemable = shop['redeemable']
            columns = {'Shop': shop['name'], 'URL': shop['link'],
                       'Einlöseurl': 'https://einloesen.wunschgutschein.de/shops/' + str(shop['id']) + '/' + shop['slug'],
                       "Kategorien": str(shop["categories_human_readable"]),
                       'Online': booleanToExcel('REDEEMABLE_ONLINE' in redeemable), 'OfflineFiliale': booleanToExcel('REDEEMABLE_BRANCH' in redeemable)
                       # TODO: Using "booleanToExcel" for "OfflineFiliale" will break our CSVs column headers? -.-
                       }
            voucherValues = shop.get('voucherValues', [])
            for possibleCardValue in relevantRedeemableCardValues:
                if isCardValuePossible(shop, possibleCardValue):
                    # columns["Kartenwert " + str(possibleCardValue)] = True
                    columns["Kartenwert " + str(possibleCardValue) + "€"] = booleanToExcel(True)
                else:
                    # columns["Kartenwert " + str(possibleCardValue)] = False
                    columns["Kartenwert " + str(possibleCardValue) + "€"] = booleanToExcel(False)
            otherCardValues = shop.get('voucherValuesMisc', [])
            if len(otherCardValues) > 0:
                columns['Sonstige Kartenwerte'] = str(shop.get('voucherValuesMisc', []))
            else:
                columns['Sonstige Kartenwerte'] = 'KEINE'
            """ TODO: Check:
             UnicodeEncodeError: 'charmap' codec can't encode character '\u0308' in position 109: character maps to <undefined>
             """
            writer.writerow(columns)
    if ignoreInactiveShopsInCSV:
        print("Number of skipped inactive shops: " + str(len(skippedInactiveShops)))
    if len(skippedInactiveShops) > 0:
        print("Skipped inactive shops:")
        print(str(skippedInactiveShops))
    print("Total time required: " + getFormattedPassedTime(timestampStart))
    print("DONE")
