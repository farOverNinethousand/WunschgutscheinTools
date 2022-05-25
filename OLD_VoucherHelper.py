import re
from typing import Tuple

import pyclip

PATTERN_VOUCHER = "[A-Za-z0-9]{3}-[A-Za-z0-9]{3}-[A-Za-z0-9]{3}"


def getVoucherCodes() -> list:
    result = []
    while len(result) == 0:
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
        result = re.compile("(" + PATTERN_VOUCHER + ")").findall(voucherSource)
        if len(result) == 0:
            print("Ungueltige Eingabe!")
    duplicates = []
    resultWithoutDuplicates = []
    for voucherTmp in result:
        if voucherTmp in resultWithoutDuplicates:
            duplicates.append(voucherTmp)
        else:
            resultWithoutDuplicates.append(voucherTmp)
    if len(duplicates) > 0:
        print(str(len(duplicates)) + " Duplikate wurden entfernt:")
        for dupe in duplicates:
            print(dupe)
        input("Bestätige mit ENTER, um ohne Duplikate fortzufahren")
    return resultWithoutDuplicates


def getVoucherCodesWithResults() -> list:
    result = []
    while len(result) == 0:
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
        result = re.compile("(" + PATTERN_VOUCHER + "[ \t]+.+)").findall(voucherSource)
        if len(result) == 0:
            print("Ungueltige Eingabe!")
    return result


def getSortedVoucherListWithResults(initialVoucherList: list, voucherListWithResults: list) -> Tuple[list, str]:
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
    voucherCodes = getVoucherCodes()
    allVouchersAsURLsText = ""
    for voucher in voucherCodes:
        allVouchersAsURLsText += "\nhttps://www.meinshoppingkonto.de/transaction/employeevoucherdeposit/?vouchercode=" + voucher
    print(allVouchersAsURLsText)
    pyclip.copy(allVouchersAsURLsText)
    print(str(len(voucherCodes)) + " GS gefunden und alle Links in die Zwischenablage kopiert!")

    while True:
        print("Gib dieselbe Liste von Codes mit Ergebnis am Ende ein z.B.: 'aaa-b5f-cgh Fehler: bla' oder 'aaa-b5f-cgh 25,00':")
        voucherCodesWithResults = getVoucherCodesWithResults()
        voucherCodesWithResultsSorted, amountText = getSortedVoucherListWithResults(voucherCodes, voucherCodesWithResults)
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
            print("ACHTUNG: Es wurden nur " + str(len(voucherCodesWithResultsSorted)) + " von " + str(len(voucherCodes)) + " anfangs eingefügten Codes zugeordnet/sortiert werden!")
            print("Das sortierte Ergebnis wurde in die Zwischenablage kopiert!")
            input("Drücke ENTER um nochmals Codes mit Ergebnis zum Sortieren einzugeben oder beende das Script.")

    input("Drücke ENTER zum Beenden")
