import re
import sys
from typing import Tuple

import pyclip

PATTERN_VOUCHER = "(?:[A-Za-z0-9]{3}-[A-Za-z0-9]{3}-[A-Za-z0-9]{3}|[A-Za-z0-9]{9})"


class Voucher:
    code = None
    valueCents = 0
    errorMsg = None

    def setValue(self, valueCents: int):
        self.valueCents = valueCents

    def setErrorMsg(self, errorMsg: str):
        self.errorMsg = errorMsg

    def getCode(self):
        return self.code

    def getCodeCleaned(self):
        return self.code.replace('-', '')

    def getValueCents(self) -> int:
        return self.valueCents

    def getValueEuros(self):
        return self.valueCents / 100

    def getValueFormatted(self) -> str:
        return "%0.2f" % (self.valueCents / 100)

    def getErrorMsg(self):
        return self.errorMsg

    def getStatus(self):
        if self.errorMsg is not None:
            return self.errorMsg
        else:
            return self.getValueFormatted()

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code + '\t' + self.getStatus()

    @staticmethod
    def parseVouchers(text: str, filterDuplicates: bool) -> list:
        """ Parses vouchers from within given text. """
        ret = []
        results = re.compile("(" + PATTERN_VOUCHER + "[ \t]+.+)").findall(text)
        dupes = []
        for result in results:
            result = result.strip()
            voucherInfoRegEx = re.compile(r'(' + PATTERN_VOUCHER + r')' + r'([ \t]+(.+)?)?').search(result)
            voucherCode = voucherInfoRegEx.group(1)
            moneyValueOrErrormessage = voucherInfoRegEx.group(3)
            voucher = Voucher(voucherCode)
            if moneyValueOrErrormessage is not None:
                if moneyValueOrErrormessage.replace(',', '').isdecimal():
                    if ',' in moneyValueOrErrormessage:
                        voucher.setValue(int(float(moneyValueOrErrormessage.replace(',', '.')) * 100))
                    else:
                        voucher.setValue(int(moneyValueOrErrormessage) * 100)
                else:
                    voucher.setErrorMsg(moneyValueOrErrormessage)
            # Skip dupes if needed
            voucherCodeCleaned = voucher.getCodeCleaned()
            if filterDuplicates and voucherCodeCleaned in dupes:
                continue
            else:
                ret.append(voucher)
                dupes.append(voucherCodeCleaned)
        return ret


def getVoucherCodes() -> list:
    results = []
    counter_lines_of_input = 0
    while len(results) == 0:
        # Multi line input: https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-user
        voucherSource = ''
        counter_lines_of_input = 0
        currInput = ' '
        while currInput != '' and counter_lines_of_input <= 500:
            currInput = input()
            voucherSource += currInput + '\n'
            if currInput == '':
                break
            elif counter_lines_of_input >= 500:
                break
            else:
                counter_lines_of_input += 1
        results = Voucher.parseVouchers(voucherSource, filterDuplicates=False)
        if len(results) == 0:
            print("Ungueltige Eingabe!")

    dupeCheckList = []
    dupes = []
    resultWithoutDuplicates = []
    for voucher in results:
        if voucher.getCodeCleaned() in dupeCheckList:
            dupeCheckList.append(voucher.getCodeCleaned())
            dupes.append(voucher.getCode())
        else:
            resultWithoutDuplicates.append(voucher)
            dupeCheckList.append(voucher.getCodeCleaned())
    if len(dupes) > 0:
        print("Achtung! " + str(len(dupes)) + " Duplikate wurden entfernt:")
        for dupe in dupes:
            print(dupe)
        input("Bestätige mit ENTER, um ohne Duplikate mit " + str(len(resultWithoutDuplicates)) + "/" + str(len(results)) + " Codes fortzufahren")
    if counter_lines_of_input != len(resultWithoutDuplicates):
        print("Warnung! " + str(counter_lines_of_input) + " Zeilen aber nur " + str(len(resultWithoutDuplicates)) + " Codes!!")
        input("Fortfahren?")
    return resultWithoutDuplicates


def getVoucherResultText(vouchers: list) -> str:
    """ Combines the initially added list with the list containing the results in order to return that list in original order. """
    totalAmount = 0
    text = ''
    for voucher in vouchers:
        if len(text) > 0:
            text += '\n'
        text += voucher.__str__()
        totalAmount += voucher.getValueEuros()
    text += "\n---"
    text += "\n" + str(totalAmount)
    return text


class VoucherHelper:

    def getSortedVoucherListWithResults(self, initialVoucherList: list, voucherListWithResults: list) -> Tuple[list, str]:
        """ Combines the initially added list with the list containing the results in order to return that list in original order. """
        result = []
        notfoundCodes = []
        totalAmount = 0
        for voucherCode in initialVoucherList:
            voucherWithResult = None
            for voucherWithResultTmp in voucherListWithResults:
                if voucherWithResultTmp.startswith(voucherCode):
                    voucherWithResult = voucherWithResultTmp
                    break
            if voucherWithResult is not None:
                moneyRegex = re.compile(PATTERN_VOUCHER + r'[ \t]+(\d+(,\d{1,2})?)').search(voucherWithResult)
                if moneyRegex:
                    amount = moneyRegex.group(1).replace(",", ".")
                    totalAmount += float(amount)
                result.append(voucherWithResult)
            else:
                notfoundCodes.append(voucherCode)
        if len(notfoundCodes) > 0:
            print("Achtung! Einige Codes der ursprünglichen Codes konnten nicht gefunden werden:")
            print(str(notfoundCodes))
        thisAmountText = "---"
        thisAmountText += "\n" + str(totalAmount)
        return result, thisAmountText

    if __name__ == '__main__':
        print("Gib alle WGs zeilengetrennt ein:")
        useOldURLHandling = False
        if useOldURLHandling:
            voucherCodes = getVoucherCodes()
            allVouchersAsURLsText = ""
            for voucher in voucherCodes:
                allVouchersAsURLsText += "\nhttps://www.meinshoppingkonto.de/transaction/employeevoucherdeposit/?vouchercode=" + voucher
            print(allVouchersAsURLsText)
            pyclip.copy(allVouchersAsURLsText)
            print(str(len(voucherCodes)) + " GS gefunden und alle Links in die Zwischenablage kopiert!")
            while True:
                print("Gib dieselbe Liste von Codes mit Ergebnis am Ende ein z.B.: 'aaa-b5f-cgh Fehler: bla' oder 'aaa-b5f-cgh 25,00':")
                voucherCodes = getVoucherCodes()
                voucherCodesWithResultsSorted, amountText = getSortedVoucherListWithResults(voucherCodes, voucherCodes)
                sortedVouchersWithResultsAsText = ""
                for voucherCodeWithResult in voucherCodesWithResultsSorted:
                    sortedVouchersWithResultsAsText += "\n" + voucherCodeWithResult
                sortedVouchersWithResultsAsText += "\n" + amountText
                print("********************************************************************************")
                print(sortedVouchersWithResultsAsText)
                pyclip.copy(sortedVouchersWithResultsAsText)
                print("********************************************************************************")
                if len(voucherCodesWithResultsSorted) == len(voucherCodes):
                    print("Es wurden alle " + str(len(voucherCodes)) + " Codes gefunden/sortiert :)")
                    print("Das sortierte Ergebnis wurde in die Zwischenablage kopiert!")
                    break
                else:
                    print("ACHTUNG: Es wurden nur " + str(len(voucherCodesWithResultsSorted)) + " von " + str(
                        len(voucherCodes)) + " anfangs eingefügten Codes zugeordnet/sortiert werden!")
                    print("Das sortierte Ergebnis wurde in die Zwischenablage kopiert!")
                    input("Drücke ENTER um nochmals Codes mit Ergebnis zum Sortieren einzugeben oder beende das Script.")
        else:
            print("Gib die Liste von Codes mit Ergebnis am Ende ein z.B.: 'aaa-b5f-cgh Fehler: bla' oder 'aaa-b5f-cgh 25,00':")
            voucherCodes = getVoucherCodes()
            text = getVoucherResultText(voucherCodes)
            print("********************************************************************************")
            print(text)
            pyclip.copy(text)
            print("********************************************************************************")
            print("Es wurden " + str(len(voucherCodes)) + " Codes gefunden :)")
            print("Das Ergebnis wurde in die Zwischenablage kopiert!")

        # input("Drücke ENTER zum Beenden")
        print("Ende")
        sys.exit()
