import argparse
import csv
import logging
import os
from datetime import datetime, timedelta
from typing import Any, List, Dict

import httpx
import simplejson as json
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
API_BASE = "https://app.wunschgutschein.de/api"
""" 2022-01-09: The Accept-Language header is really important as the returned json response can vary based on that.
 For example "en-EN,en;q=0.5" will return a different list of supported shops on GET "/shop/categories/1".  """
basicHeaders = {"X-Requested-With": "XMLHttpRequest",
                "Accept-Language": "de-DE,de;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
debugmode = False


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


def isCardValuePossible(thisShop: dict, checkValueEuros: int) -> bool:
    """ Checks if given shop supports redeeming vouchers for given card value in EUR. """
    thisVoucherValues = thisShop.get('voucherValues', [])
    for thisVoucherValue in thisVoucherValues:
        thisValueInCent = thisVoucherValue['valueInCent']
        if thisValueInCent == checkValueEuros * 100:
            return True
    return False


def saveJson(obj, path):
    """ Saves given object as json to desired path. """
    with open(path, 'w') as ofile:
        json.dump(obj, ofile)


class WGCrawler:
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-a', '--allow_update_shops',
                           help='Alte shops.json wiederverwenden und nur neue Shops crawlen/hinzufügen. Alte Shop-Daten werden nicht aktualisiert und nicht mehr existente Shops bleiben in der Liste!',
                           type=bool, default=False)
    my_parser.add_argument('-c', '--csv_skip_inactive_shops',
                           help='Als \'inaktiv\' markierte Shops nicht mit in die Liste aufnehmen. Was \'inaktiv\' bedeutet ist noch unklar, daher sollte man diesen Parameter nicht verwenden.',
                           type=bool, default=False)
    args = my_parser.parse_args()

    def __init__(self, wgAT: bool = False, shopTypeWhitelist: List = None, relevantRedeemableCardValuesEuro: List = None):
        if relevantRedeemableCardValuesEuro is None or len(relevantRedeemableCardValuesEuro) == 0:
            relevantRedeemableCardValuesEuro = [10, 15, 20, 25, 50, 100]
        self.relevantRedeemableCardValues = relevantRedeemableCardValuesEuro
        self.allow_update_shops = self.args.allow_update_shops
        self.allow_update_shops = False
        self.csv_skip_inactive_shops = self.args.csv_skip_inactive_shops  #
        if wgAT:
            self.countrycode = 'AT'
            self.domain = 'wunschgutschein.at'
            self.additionalShopMapping = {
                2: 'normal'
            }
        else:
            self.countrycode = 'DE'
            self.domain = 'wunschgutschein.de'
            self.additionalShopMapping = {
                1: 'normal'
            }
            # self.typeMapping = {
            #     1: 'normal',
            #     4: 'fashion',
            #     29: 'tanken',
            #     30: 'mobilitaet'
            # }

    def getCountryCodeForURL(self) -> str:
        return self.countrycode.lower()

    def run(self):

        if debugmode:
            print("DEBUGMODE!!!")
        timestampStart = datetime.now().timestamp()
        filepathShopsCSV = f'{self.countrycode}_shops.csv'
        filepathShops = f'{self.countrycode}_shops.json'
        filepathShopsRaw = f'{self.countrycode}_shops_raw.json'
        canReUseExistingDatabase = os.path.exists(filepathShops) and self.allow_update_shops
        if canReUseExistingDatabase:
            print("Existierende " + filepathShops + " wird verwendet!")
        # Get list of possible variations
        variations = self.callAPI(f'/redeem/variation/{self.getCountryCodeForURL()}')
        if len(variations) == 0:
            # This should never happen
            print("WTF no variations available")
            return

        wgVoucherTypeIdToMoreMapping = {}
        for variation in variations:
            voucherCategory = variation.get('voucherCategory')
            if self.additionalShopMapping is not None and voucherCategory in self.additionalShopMapping:
                wgVoucherTypeIdToMoreMapping[voucherCategory] = {
                    'path': '',
                    'urlName': self.additionalShopMapping[voucherCategory]
                }
            else:
                urlName = variation.get('urlName')
                wgVoucherTypeIdToMoreMapping[voucherCategory] = {
                    'path': urlName,
                    'urlName': variation.get('urlName')
                }
        if len(wgVoucherTypeIdToMoreMapping) == 0:
            # TODO: Add whitelist implementation
            print("Keine crawlbaren Kategorien gefunden -> Möglicherweise zu strikte Whitelist!")
            return

        # Crawl all shopping categories and make a mapping
        categoriesList = self.callAPI('/shop/categories/1')
        categoriesIdToNameMapping = {}
        for category in categoriesList:
            categoriesIdToNameMapping.setdefault(category['id'], category)
        # Save categories mapping as json file
        saveJson(categoriesIdToNameMapping, 'categories.json')

        index_wgVoucherTypeIdToUrlNameMapping = 0
        crawledShopsRawNowFromAPI = []
        for wgVoucherTypeId, wgVoucherTypeMap in wgVoucherTypeIdToMoreMapping.items():
            # Get list of basic shop information
            """ TODO: Umbauen, sodass alle Infos mit einem einzelnen Request von hier geholt werden:
            https://app.wunschgutschein.de/api/shop/wall/1?extraFields=voucherValues
            Ergebnis variiert je nach Parameter z.B.
            https://app.wunschgutschein.de/api/shop/wall/1?extraFields=voucherValues&onlyWithLogo=1&position=T
            """
            # thisCrawledShopsRawNowFromAPI = callAPI(f'/shop/wall/{wgVoucherTypeId}?extraFields=voucherValues&onlyWithLogo=1&position=T')
            thisCrawledShopsRawNowFromAPI = self.callAPI(f'/shop/wall/{wgVoucherTypeId}?extraFields=voucherValues')
            wgVoucherTypeMap['shops'] = thisCrawledShopsRawNowFromAPI

            for shop in thisCrawledShopsRawNowFromAPI:
                if shop not in crawledShopsRawNowFromAPI:
                    crawledShopsRawNowFromAPI.append(shop)
            index_wgVoucherTypeIdToUrlNameMapping += 1
            print(
                f'WG Typ Crawler Fortschritt: {index_wgVoucherTypeIdToUrlNameMapping}/{len(wgVoucherTypeIdToMoreMapping)} | Anzahl Shops bisher: {len(crawledShopsRawNowFromAPI)} | ID: {wgVoucherTypeId} | {wgVoucherTypeMap.get("urlName")}')
        print(f'Gesamtanzahl möglicher Shops: {len(crawledShopsRawNowFromAPI)}')
        # Save as json for later offline examination
        saveJson(crawledShopsRawNowFromAPI, filepathShopsRaw)

        shopIDsToUpdate = []
        shopIDsNew = []
        storedShops = []
        if canReUseExistingDatabase:
            # Load last state so we can crawl faster
            print("Vorherige " + filepathShops + " gefunden. Es werden nur neue Shops gecrawlt, Informationen bestehender werden nicht aktualisiert!!")
            with open(os.path.join(os.getcwd(), filepathShops), encoding='utf-8') as infile:
                storedShops = json.load(infile)
            newShops = []
            for currentShop in crawledShopsRawNowFromAPI:
                currentShopID = currentShop['id']
                foundShop = False
                for storedShop in storedShops:
                    if storedShop['id'] == currentShopID:
                        foundShop = True
                        break
                if not foundShop:
                    # New shopID found: Store so we can crawl the details of that shop later
                    # print("SHOP_NEW: " + currentShop['name'] + " | ID: " + str(currentShopID))
                    shopIDsToUpdate.append(currentShopID)
                    newShops.append(currentShop)
                    shopIDsNew.append(currentShopID)
            print("Number of new shops: " + str(len(newShops)))
            # Continue with old dataset now that we know which shops need re-crawl
            crawledShopsRawToUse = storedShops + newShops
        else:
            # Add all shopIDs to list so we will update data of all shops
            crawledShopsRawToUse = crawledShopsRawNowFromAPI.copy()
            for shopRaw in crawledShopsRawToUse:
                shopIDsToUpdate.append(shopRaw['id'])

        # Collect detailed info for all shops - will may take some time
        print(f'Crawle Details von {len(shopIDsToUpdate)} Shops')
        numberofProcessedRequestsToCrawlShopDetails = 1
        debugStopFlag = False
        for shop in crawledShopsRawToUse:
            shopID = shop['id']
            if shopID in shopIDsToUpdate:
                print(f"Working on shop {numberofProcessedRequestsToCrawlShopDetails}/{len(shopIDsToUpdate)}: {shopID}")
                extendedShopInfo = self.callAPI('/shop/' + str(shopID))
                # Merge both dicts so we got all shop information in one dict
                shop.update(extendedShopInfo)
                if numberofProcessedRequestsToCrawlShopDetails >= 10 and debugmode:
                    print("Stopping because: debugmode is enabled")
                    debugStopFlag = True
                numberofProcessedRequestsToCrawlShopDetails += 1
            # Beautify some data so in the end we got one json that contains everything
            categoriesHumanReadable = []
            for categoryID in shop['categories']:
                categoriesHumanReadable.append(categoriesIdToNameMapping[categoryID]['name'])
            shop['WGCrawler_categories_human_readable'] = categoriesHumanReadable
            voucherValuesCent = shop.get('voucherValues', [])
            otherCardValuesEuro = []
            for voucherValue in voucherValuesCent:
                valueInCent = voucherValue['valueInCent']
                valueInEuro = valueInCent / 100
                if valueInEuro not in self.relevantRedeemableCardValues:
                    otherCardValuesEuro.append(valueInEuro)
            shop['WGCrawler_voucherValuesMisc'] = otherCardValuesEuro
            thisShopWgTypes = []
            for wgVoucherTypeMap in wgVoucherTypeIdToMoreMapping.values():
                thisWgTypeShops = wgVoucherTypeMap['shops']
                for thisWgTypeShop in thisWgTypeShops:
                    thisWgTypeShopID = thisWgTypeShop['id']
                    if thisWgTypeShopID == shop['id']:
                        thisShopWgTypes.append(wgVoucherTypeMap.get('urlName'))
                        break
            shop['WGCrawlerWGTypes'] = thisShopWgTypes
            # Check for stop flag
            if debugStopFlag:
                break
        shops = crawledShopsRawToUse

        # Save shop information as json file
        saveJson(shops, filepathShops)

        # Look for deleted shops and print info - Only possible if we got data from previous crawl process
        for oldShop in storedShops:
            foundShop = False
            oldShopID = oldShop['id']
            for shop in crawledShopsRawNowFromAPI:
                if shop['id'] == oldShopID:
                    foundShop = True
                    break
            if not foundShop:
                print('SHOP_DELETED: ' + str(oldShopID) + ' | ' + oldShop['name'] + ' | Link:' + oldShop.get('link', 'N/A'))
        # Print info about new shops
        if len(shopIDsNew) > 0:
            for newShopID in shopIDsNew:
                for shop in shops:
                    shopID = shop['id']
                    if shopID == newShopID:
                        print(f'SHOP_NEW: {newShopID} | {shop["name"]} | {shop.get("link")}')

        # Create csv file with most relevant human readable results
        skippedInactiveShops = []
        with open(filepathShopsCSV, 'w', newline='', encoding="utf-8") as csvfile:
            # TODO: Add column "Beschreibung" but atm this will fuck up our CSV formatting, maybe we need to escape that String before
            fieldnames = ['Shop', 'Beschreibung', 'Einlösebedingungen', 'URL', 'Einlöseurl', 'Kategorien', 'Online', 'OfflineFiliale']
            # Add one column for each possible card value
            for possibleCardValueEuros in self.relevantRedeemableCardValues:
                fieldnames.append("Kartenwert " + str(possibleCardValueEuros) + "€")
            key_MiscCardValues = "Sonstige Kartenwerte"
            key_WGTypes = "Verfuegbar in WG Typ"
            fieldnames.append(key_MiscCardValues)
            fieldnames.append(key_WGTypes)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for shop in shops:
                if self.csv_skip_inactive_shops and not shop['active']:
                    skippedInactiveShops.append(shop)
                    continue
                redeemWarningsPlain = ''
                redeemWarnings = shop.get('redeemWarnings', [])
                for redeemWarning in redeemWarnings:
                    redeemWarningText = redeemWarning['text']
                    redeemWarningTextSoup = BeautifulSoup(redeemWarningText)
                    # HTML to text
                    redeemWarningsPlain += redeemWarningTextSoup.get_text() + '\n'
                redeemWarningsPlain = redeemWarningsPlain.strip()
                redeemable = shop['redeemable']
                columnsDict = {'Shop': shop['name'], 'URL': shop.get('link', 'N/A'),
                               'Einlöseurl': 'https://app.wunschgutschein.de/shops/' + str(shop['id']) + '/' + str(shop['slug']),
                               "Kategorien": str(shop.get("WGCrawler_categories_human_readable", "DEBUG_MODUS_ODER_FEHLER")),
                               "Einlösebedingungen": redeemWarningsPlain,
                               'Online': booleanToExcel('REDEEMABLE_ONLINE' in redeemable), 'OfflineFiliale': booleanToExcel('REDEEMABLE_BRANCH' in redeemable),
                               'Beschreibung': shop.get('description', '')
                               # TODO: Using "booleanToExcel" for "OfflineFiliale" will break our CSVs column headers? -.-
                               }
                # Polish some data for our CSV
                # Column "Sonstige Kartenwerte"
                for possibleCardValue in self.relevantRedeemableCardValues:
                    if isCardValuePossible(shop, possibleCardValue):
                        # columnsDict["Kartenwert " + str(possibleCardValue)] = True
                        columnsDict["Kartenwert " + str(possibleCardValue) + "€"] = booleanToExcel(True)
                    else:
                        # columnsDict["Kartenwert " + str(possibleCardValue)] = False
                        columnsDict["Kartenwert " + str(possibleCardValue) + "€"] = booleanToExcel(False)
                otherCardValuesEuro = shop.get('WGCrawler_voucherValuesMisc', [])
                if len(otherCardValuesEuro) > 0:
                    columnsDict[key_MiscCardValues] = str(otherCardValuesEuro)
                else:
                    columnsDict[key_MiscCardValues] = 'KEINE'
                # Column "WG Typen"
                thisShopWgTypes = shop.get('WGCrawlerWGTypes', [])
                if len(thisShopWgTypes) > 0:
                    columnsDict[key_WGTypes] = str(thisShopWgTypes)
                else:
                    columnsDict[key_WGTypes] = 'KEINE ODER ALLE'

                """ TODO: Check:
                 UnicodeEncodeError: 'charmap' codec can't encode character '\u0308' in position 109: character maps to <undefined>
                 """
                writer.writerow(columnsDict)
        if self.csv_skip_inactive_shops:
            print("Number of skipped inactive shops: " + str(len(skippedInactiveShops)))
            print("Skipped inactive shops:")
            print(str(skippedInactiveShops))
        print("Total time required: " + getFormattedPassedTime(timestampStart))
        print(f'DONE, results are were saved in files: {filepathShopsCSV}, {filepathShops} and {filepathShopsRaw}')

    def callAPI(self, path: str, returnJson: bool = True) -> Any:
        """ Performs API request. """
        resp = httpx.get(url=f"https://app.{self.domain}/api{path}", headers=basicHeaders, timeout=120)
        if returnJson:
            return resp.json()
        else:
            return resp.text


def main():
    crawler = WGCrawler(wgAT=False)
    crawler.run()


if __name__ == '__main__':
    main()
