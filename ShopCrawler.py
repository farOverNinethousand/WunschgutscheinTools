import argparse
import csv
import logging
import os
import random
import time
from datetime import datetime, timedelta
from typing import Any, List

import httpx
import simplejson as json
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_BASE = "https://app.wunschgutschein.de/api"
"""
2022-01-09: The Accept-Language header is really important as the returned json response can vary based on that.
For example "en-EN,en;q=0.5" will return a different list of supported shops on GET "/shop/categories/1".
"""
basicHeaders = {
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "de-DE,de;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
debugmode = False

SPECIAL_SHOPPINGKONTO_DISTRIBUTION = "MEINSHOPPINGKONTO"


def booleanToExcel(mybool: bool) -> str:
    return "X" if mybool else ""


def getFormattedPassedTime(pastTimestamp: float) -> str:
    """Returns human readable duration until given future timestamp is reached."""
    secondsPassed = datetime.now().timestamp() - pastTimestamp
    return str(timedelta(seconds=secondsPassed))


def isCardValuePossible(thisShop: dict, checkValueEuros: int) -> bool:
    """Checks if given shop supports redeeming vouchers for given card value in EUR."""
    thisVoucherValues = thisShop.get('voucherValues', [])
    for thisVoucherValue in thisVoucherValues:
        thisValueInCent = thisVoucherValue['valueInCent']
        if thisValueInCent == checkValueEuros * 100:
            return True
    return False


def saveJson(obj, path):
    """Saves given object as json to desired path."""
    with open(path, 'w', encoding='utf-8') as ofile:
        json.dump(obj, ofile, ensure_ascii=False, indent=2)


class WGCrawler:
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        '-a', '--allow_update_shops',
        help='Alte shops.json wiederverwenden und nur neue Shops crawlen/hinzufügen. Alte Shop-Daten werden nicht aktualisiert und nicht mehr existente Shops bleiben in der Liste!',
        action='store_true'
    )
    args = my_parser.parse_args()

    def __init__(self, wgAT: bool = False, shopTypeWhitelist: List = None, relevantRedeemableCardValuesEuro: List = None):
        if relevantRedeemableCardValuesEuro is None or len(relevantRedeemableCardValuesEuro) == 0:
            relevantRedeemableCardValuesEuro = [10, 15, 20, 25, 50, 100]

        self.relevantRedeemableCardValues = relevantRedeemableCardValuesEuro
        self.allow_update_shops = self.args.allow_update_shops
        self.client = httpx.Client()

        """Use additionalVariations to add variations which this script cannot auto-detect."""
        self.additionalVariations = []

        if wgAT:
            self.countrycode = 'AT'
            self.domain = 'wunschgutschein.at'
            self.additionalVariations = [
                dict(name="Normal", voucherCategory=2)
            ]
        else:
            self.countrycode = 'DE'
            self.domain = 'wunschgutschein.de'
            self.additionalVariations = [
                dict(name="Shoppingkonto", voucherCategory=1, distribution=SPECIAL_SHOPPINGKONTO_DISTRIBUTION),
                dict(name="LIDL_OHNE_AMAZON", voucherCategory=1, distribution="LIDL_OHNE_AMAZON", name_for_table="FILIALE_LI_DL_OHNE_AMA_ZON"),
                dict(name="Penny ohne Kaufland", voucherCategory=1, distribution="PENNY_PROMO", name_for_table="FILIALE_P_E_N_N_Y_PROMO"),
                dict(name="ALDI_SUED", voucherCategory=1, distribution="ALDI_SUED", name_for_table="FILIALE_AL_DI_SUED"),
                dict(name="Rewe", voucherCategory=1, distribution="Rewe", name_for_table="RE_WE"),
                dict(name="Rossmann", voucherCategory=1, distribution="Rossmann", name_for_table="FILIALE_ROSS_MANN"),
                dict(name="Kaufland", voucherCategory=1, distribution="Kaufland", name_for_table="FILIALE_KAUF_LAND"),
                dict(name="EDEKA", voucherCategory=1, distribution="EDEKA", name_for_table="FILIALE_EDE_KA"),
                dict(name="LEKKERLAND", voucherCategory=1, distribution="LEKKERLAND"),
                dict(name="WG_Amazon", voucherCategory=1, distribution="WGSAMAZON POR", name_for_table="WGS_AMA_ZON_POR"),
                # dict(name="EPAY", voucherCategory=1, distribution="EPAY"),
                # dict(name="WG Tanken Test mit Distribution", voucherCategory=29, distribution="ONLINE_GG_TANKSTELLEN_PDF"),
            ]

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

        variations = self.callAPI(f'/redeem/variation/{self.getCountryCodeForURL()}')
        if len(variations) == 0:
            print("WTF no variations available")
            return

        variationsForCrawler = []

        # Blacklist für ungewollte distribution Strings
        distributionsToSkip = [
            "TEST_Distribution_Eintrag_der_uebersprungen_werden_soll",
            # "B2B_Postcode_Lotterie",
        ]

        for variation in variations:
            urlName = variation['urlName']
            distribution = variation.get("distribution")
            if distribution is not None and distribution in distributionsToSkip:
                print(f"Ueberspringe {urlName} basierend auf blacklisted distribution {distribution}")
                continue
            variationsForCrawler.append(variation)

        for variation in self.additionalVariations:
            if variation not in variationsForCrawler:
                variationsForCrawler.append(variation)

        categoriesList = self.callAPI('/shop/categories/1')
        categoriesIdToNameMapping = {}
        for category in categoriesList:
            categoriesIdToNameMapping.setdefault(category['id'], category)

        saveJson(categoriesIdToNameMapping, 'categories.json')

        variationIndex = 0
        allShopsRawNowFromAPI = []
        variationsUnique = []
        variationsDuplicated = []
        shops_voucher_type_and_distribution = {}
        skippedSpecialShoppingkontoDistribution = None

        for variation in variationsForCrawler:
            variationIndex += 1
            variationName = variation['name']
            variationVoucherCategoryID = variation['voucherCategory']
            variationDistribution = variation.get('distribution')

            if variationDistribution is not None and variationDistribution == SPECIAL_SHOPPINGKONTO_DISTRIBUTION:
                print("Skipping Shoppingkonto in order to process it later")
                skippedSpecialShoppingkontoDistribution = variation
                continue

            type_and_distribution_key = f"{variationVoucherCategoryID}_{variationDistribution}"
            print(
                f"Crawle WG Variation Shops: {variationIndex}/{len(variationsForCrawler)} | "
                f"Anzahl Shops bisher: {len(allShopsRawNowFromAPI)} | "
                f"variationName='{variationName}' | variationDistribution='{variationDistribution}'"
            )

            thisShopIDs = shops_voucher_type_and_distribution.get(type_and_distribution_key)
            if thisShopIDs is None:
                params = dict(extraFields="voucherValues", currency="EUR")
                if variationDistribution is not None:
                    params['distribution'] = variationDistribution

                thisShopsRawNowFromAPI = self.callAPI(f'/shop/wall/{variationVoucherCategoryID}', params=params)

                if len(thisShopsRawNowFromAPI) == 0:
                    logging.warning(
                        "Variation ohne Shops übersprungen: name=%s, distribution=%s, voucherCategory=%s",
                        variationName, variationDistribution, variationVoucherCategoryID
                    )
                    shops_voucher_type_and_distribution[type_and_distribution_key] = []
                    variationsDuplicated.append(variation)
                    print('**************************************************')
                    continue

                thisShopIDs = []
                for shop in thisShopsRawNowFromAPI:
                    shopID = shop['id']
                    thisShopIDs.append(shopID)

                    foundShop = False
                    for shopTmp in allShopsRawNowFromAPI:
                        if shopTmp['id'] == shopID:
                            foundShop = True
                            break
                    if not foundShop:
                        allShopsRawNowFromAPI.append(shop)

                listOfVariationShopLists = list(shops_voucher_type_and_distribution.values())
                if thisShopIDs in listOfVariationShopLists:
                    variationsDuplicated.append(variation)
                else:
                    variationsUnique.append(variation)

                shops_voucher_type_and_distribution[type_and_distribution_key] = thisShopIDs
            else:
                variationsDuplicated.append(variation)

            print(f"{variationName} -> {len(thisShopIDs)} Shops | Shops gefunden bisher: {len(allShopsRawNowFromAPI)}")
            print('**************************************************')

        print(f'Gesamtanzahl möglicher Shops (ohne Shoppingkonto Shops): {len(allShopsRawNowFromAPI)}')

        if skippedSpecialShoppingkontoDistribution is not None:
            """
            Herzlicher Undank an WG geht raus, die Shoppingkonto Shops so zu verstecken lol
            Um an die Shops des Shoppingkontos zu kommen, muss eine Wertstufe angegeben werden,
            aber dann bekommt man natürlich nur die Shops, die diese Wertstufe bieten.
            Wir wollen alle Shops, die per Shoppingkonto möglich sind und müssen daher
            einmal alle Wertstufen durchgehen.
            """
            print("Crawle Shoppingkonto Shops")
            possibleShoppingkontoValuesCentLIST = [1000, 2000, 2500, 5000, 10000]
            index = 0
            variationName = skippedSpecialShoppingkontoDistribution['name']
            variationVoucherCategoryID = skippedSpecialShoppingkontoDistribution['voucherCategory']
            shoppingkontoShopIDs = []

            for possibleShoppingkontoValueCent in possibleShoppingkontoValuesCentLIST:
                index += 1
                print(
                    f"Crawle Shoppingkonto Shops von Wertstufe {index}/{len(possibleShoppingkontoValuesCentLIST)} | "
                    f"{possibleShoppingkontoValueCent=}"
                )
                params = dict(
                    extraFields="voucherValues",
                    currency="EUR",
                    voucherValue=possibleShoppingkontoValueCent,
                    distribution=SPECIAL_SHOPPINGKONTO_DISTRIBUTION
                )
                thisShopsRawNowFromAPI = self.callAPI(f'/shop/wall/{variationVoucherCategoryID}', params=params)

                for shop in thisShopsRawNowFromAPI:
                    shopID = shop['id']
                    if shopID not in shoppingkontoShopIDs:
                        shoppingkontoShopIDs.append(shopID)

                    foundShop = False
                    for shopTmp in allShopsRawNowFromAPI:
                        if shopTmp['id'] == shopID:
                            foundShop = True
                            break
                    if not foundShop:
                        print(f"Special nur Shoppingkonto Shop: {shopID}")
                        allShopsRawNowFromAPI.append(shop)

            type_and_distribution_key = f"{variationVoucherCategoryID}_{SPECIAL_SHOPPINGKONTO_DISTRIBUTION}"
            shops_voucher_type_and_distribution[type_and_distribution_key] = shoppingkontoShopIDs
            print(f"{variationName} -> {len(shoppingkontoShopIDs)} Shoppingkonto Shops gefunden")

        print(f'Gesamtanzahl möglicher Shops (mit Shoppingkonto Shops): {len(allShopsRawNowFromAPI)}')
        saveJson(allShopsRawNowFromAPI, filepathShopsRaw)

        shopIDsToUpdate = []
        shopIDsNew = []
        storedShops = []

        if canReUseExistingDatabase:
            print("Vorherige " + filepathShops + " gefunden. Es werden nur neue Shops gecrawlt, Informationen bestehender werden nicht aktualisiert!!")
            with open(os.path.join(os.getcwd(), filepathShops), encoding='utf-8') as infile:
                storedShops = json.load(infile)

            newShops = []
            for currentShop in allShopsRawNowFromAPI:
                currentShopID = currentShop['id']
                foundShop = False
                for storedShop in storedShops:
                    if storedShop['id'] == currentShopID:
                        foundShop = True
                        break
                if not foundShop:
                    shopIDsToUpdate.append(currentShopID)
                    newShops.append(currentShop)
                    shopIDsNew.append(currentShopID)

            print(f"Number of new shops: {len(newShops)}")
            crawledShopsRawToUse = storedShops + newShops
        else:
            crawledShopsRawToUse = allShopsRawNowFromAPI.copy()
            for shopRaw in crawledShopsRawToUse:
                shopIDsToUpdate.append(shopRaw['id'])

        print(f'Crawle Details von {len(shopIDsToUpdate)} Shops')
        numberofProcessedRequestsToCrawlShopDetails = 1
        debugStopFlag = False

        for shop in crawledShopsRawToUse:
            shopID = shop['id']
            if shopID in shopIDsToUpdate:
                print(f"Working on shop {numberofProcessedRequestsToCrawlShopDetails}/{len(shopIDsToUpdate)}: {shopID}")

                time.sleep(0.4 + random.uniform(0, 0.6))
                extendedShopInfo = self.callAPI('/shop/' + str(shopID))

                shop.update(extendedShopInfo)

                if numberofProcessedRequestsToCrawlShopDetails >= 10 and debugmode:
                    print("Stopping because: debugmode is enabled")
                    debugStopFlag = True

                numberofProcessedRequestsToCrawlShopDetails += 1

            categoriesHumanReadable = []
            for categoryID in shop.get('categories', []):
                if categoryID in categoriesIdToNameMapping:
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

            thisShopWGVariations = []
            for variation in variationsForCrawler:
                variationName = variation['name']
                variationVoucherCategoryID = variation['voucherCategory']
                variationDistribution = variation.get('distribution')
                type_and_distribution_key = f"{variationVoucherCategoryID}_{variationDistribution}"
                variationShopIDList = shops_voucher_type_and_distribution.get(type_and_distribution_key, [])
                if shopID in variationShopIDList:
                    thisShopWGVariations.append(variationName)
            shop['WG_Variations'] = thisShopWGVariations

            thisShopWGVariationsForTable = []
            for variation in variationsUnique:
                variationName = variation['name']
                variationVoucherCategoryID = variation['voucherCategory']
                variationDistribution = variation.get('distribution')
                type_and_distribution_key = f"{variationVoucherCategoryID}_{variationDistribution}"
                variationShopIDList = shops_voucher_type_and_distribution.get(type_and_distribution_key, [])
                if shopID in variationShopIDList:
                    variationNameForTable = variation.get('name_for_table', variationName)
                    thisShopWGVariationsForTable.append(variationNameForTable)
            shop['WG_Variations_table'] = thisShopWGVariationsForTable

            if debugStopFlag:
                break

        saveJson(crawledShopsRawToUse, filepathShops)

        for oldShop in storedShops:
            foundShop = False
            oldShopID = oldShop['id']
            for shop in allShopsRawNowFromAPI:
                if shop['id'] == oldShopID:
                    foundShop = True
                    break
            if not foundShop:
                print('SHOP_DELETED: ' + str(oldShopID) + ' | ' + oldShop['name'] + ' | Link:' + oldShop.get('link', 'N/A'))

        if len(shopIDsNew) > 0:
            for newShopID in shopIDsNew:
                for shop in crawledShopsRawToUse:
                    shopID = shop['id']
                    if shopID == newShopID:
                        print(f'SHOP_NEW: {newShopID} | {shop["name"]} | {shop.get("link")}')

        with open(filepathShopsCSV, 'w', newline='', encoding="utf-8") as csvfile:
            fieldnames = [
                'Shop',
                'Beschreibung',
                'Einlösebedingungen',
                'URL',
                'Einlöseurl',
                'Kategorien',
                'Online',
                'OfflineFiliale'
            ]

            for possibleCardValueEuros in self.relevantRedeemableCardValues:
                fieldnames.append("Wertstufe " + str(possibleCardValueEuros) + "€")

            key_MiscCardValues = "Sonstige Wertstufen"
            key_WGTypes = "Verfügbar in unique WG Variationen"
            fieldnames.append(key_MiscCardValues)
            fieldnames.append(key_WGTypes)

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for shop in crawledShopsRawToUse:
                redeemWarningsPlain = ''
                redeemWarnings = shop.get('redeemWarnings', [])
                for redeemWarning in redeemWarnings:
                    redeemWarningText = redeemWarning['text']
                    redeemWarningTextSoup = BeautifulSoup(redeemWarningText, features="html.parser")
                    redeemWarningsPlain += redeemWarningTextSoup.get_text() + '\n'
                redeemWarningsPlain = redeemWarningsPlain.strip()

                redeemable = shop.get('redeemable', [])
                columnsDict = {
                    'Shop': shop.get('name', ''),
                    'URL': shop.get('link', 'N/A'),
                    'Einlöseurl': 'https://app.wunschgutschein.de/shops/' + str(shop['id']) + '/' + str(shop.get('slug', '')),
                    'Kategorien': str(shop.get("WGCrawler_categories_human_readable", "DEBUG_MODUS_ODER_FEHLER")),
                    'Einlösebedingungen': redeemWarningsPlain,
                    'Online': booleanToExcel('REDEEMABLE_ONLINE' in redeemable),
                    'OfflineFiliale': booleanToExcel('REDEEMABLE_BRANCH' in redeemable),
                    'Beschreibung': shop.get('description', '')
                }

                for possibleCardValue in self.relevantRedeemableCardValues:
                    columnsDict["Wertstufe " + str(possibleCardValue) + "€"] = booleanToExcel(
                        isCardValuePossible(shop, possibleCardValue)
                    )

                otherCardValuesEuro = shop.get('WGCrawler_voucherValuesMisc', [])
                if len(otherCardValuesEuro) > 0:
                    columnsDict[key_MiscCardValues] = str(otherCardValuesEuro)
                else:
                    columnsDict[key_MiscCardValues] = 'KEINE'

                thisShopWGVariations = shop.get('WG_Variations_table', [])
                if len(thisShopWGVariations) > 0:
                    columnsDict[key_WGTypes] = str(thisShopWGVariations)
                else:
                    columnsDict[key_WGTypes] = 'KEINE ODER ALLE'

                writer.writerow(columnsDict)

        print("Total time required: " + getFormattedPassedTime(timestampStart))
        print(f'DONE, results are were saved in files: {filepathShopsCSV}, {filepathShops} and {filepathShopsRaw}')

    def callAPI(self, path: str, params=None, returnJson: bool = True) -> Any:
        """Performs API request with retry/backoff for rate limits."""
        url = f"https://app.{self.domain}/api/v2{path}"
        max_retries = 6

        for attempt in range(1, max_retries + 1):
            resp = self.client.get(
                url=url,
                params=params,
                headers=basicHeaders,
                timeout=120
            )

            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                if retry_after is not None:
                    try:
                        wait_seconds = int(retry_after)
                    except ValueError:
                        wait_seconds = 5
                else:
                    wait_seconds = min(60, 2 ** attempt) + random.uniform(0, 1)

                logging.warning(
                    "Rate limit bei %s (Attempt %s/%s), warte %.1fs",
                    path, attempt, max_retries, wait_seconds
                )
                time.sleep(wait_seconds)
                continue

            resp.raise_for_status()

            if returnJson:
                try:
                    return resp.json()
                except Exception as e:
                    raise Exception(
                        f"Antwort war kein gültiges JSON für {path}. "
                        f"Status={resp.status_code}, Body={resp.text[:300]!r}"
                    ) from e

            return resp.text

        raise Exception(f"API Rate Limit dauerhaft erreicht für {path} nach {max_retries} Versuchen")


def main():
    crawler = WGCrawler(wgAT=False)
    crawler.run()


if __name__ == '__main__':
    main()