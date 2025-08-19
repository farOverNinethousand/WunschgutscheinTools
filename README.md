# Wunschgutschein.de, Wunschgutschein.at und Shoppingkonto.de Tools

Wunschgutschein und shoppingkonto.de/.at Guthaben teil-automatisiert einlösen und vollständige Liste von Wunschgutschein Einlösepartnern mitsamt verfügbarer Wertstufen automatisch crawlen

# Fertige Shoplisten
Wer zu faul ist, die Shopliste selbst zu crawlen, findet unter folgendem Link eine Sammlung von Shoplisten, die in unregelmäßigen Abständen aktualisiert wird:  
https://mega.nz/folder/HehC1JyK#v5R3VoyOGnoIU6dHKU1vIg  
**Wichtig:**  
Diese Shopliste enthält auch Shops, die nicht bei allen Wunschgutschein-Varianten verfügbar sind also nur weil irgendwo *Aral* oder *ESSO* steht bedeutet dies nicht, dass man mit normalen Wunschgutscheinen direkt an Tankgutscheine kommt!  
Beachtet die Spalte "*Verfügbar in unique WG Variationen*"!!  
Die klassischen WG Tankgutscheine gibt es nur unter [geschenkgutscheine.de/products/tankgutschein](https://geschenkgutscheine.de/products/tankgutschein).

# 18.12.2023: Wunschgutschein speichert die Daten mittlerweile selbst und füllt das Formular automatisch aus, wenn man mehrere Codes einlöst somit kann man statt der unten beschriebenen Methoden auch einfach mehrere Browserprofile (eines pro E-Mail Adresse) verwenden.


# [Veraltet] Wunschgutschein Codes und Shoppingkonto.de Guthaben (teil-)automatisiert einlösen
### Benötigte Browser Addons
* [Redirector](https://chrome.google.com/webstore/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd)
* [Autofill](https://chrome.google.com/webstore/detail/autofill/nlmmgnhgdeffjkdckmikfpnddkbbfkkk)
1. Die benötigten Addons installieren.
2. Die Datei ``Redirector.json`` herunterladen, in den Optionen des Redirector Addons importieren (Optionen -> Import) und beliebig anpassen bzw. so einstellen, dass es automatisch zum bevorzugten Einlösepartner weiterleitet.
3. Die Datei ``Autofill.txt`` herunterladen.
Dann wie folgt importieren:  
Optionen -> Import/Export -> In das große Textfeld den kompletten Inhalt der Datei einfügen -> Import --> Wechseln ins Tab "Form Fields" -> Links unten auf "Save" klicken.  
Optional:  
Wenn du Profile hast, die nur für bestimmte Einlösepartner angewendet werden sollen, kannst du im jeweiligen Profil unten bei ``site`` die URL zum Shop angeben z.B.  
``https://app.wunschgutschein.de/shops/10837/amazon``  
Wenn du nur wenige Profile hast und/oder den Einlösepartner ausschließlich über das Redirector Addon steuern möchtest solltest du dafür sorgen, dass alle Autofill Profile für alle Shops gelten.  
Schreibe dafür folgenden Wert in das Site Feld:  
``https://app.wunschgutschein.de/shops/*``  
(= Standard, wenn du das Beispielprofil aus dieser Repository verwendest.)
4. Jetzt in Autofill das Beispielprofil beliebig oft duplizieren und mit eigenen Daten befüllen.  
Mit ALT + G gelangst du zur Übersicht der Profile und kannst bestehende duplizieren/ändern.  
Wichtig:  
Falls beim Shop deiner Wahl bestimmte Felder für ein bestimmtes Profil anders sein sollen:  
Unten bei "Site:" den Link zum Shop angeben für den das Profil gelten soll.  

**Was nun passieren sollte:**  
Du öffnest die Einlöseseite, gibst deinen Gutscheincode ein und bestätigst das Captcha.  
Danach wirst du automatisch zur Shopseite weitergeleitet , musst nur noch 1x auf "Weiter" klicken, deine Daten werden automatisch eingetragen und mit einem weiteren Klick wird der Gutschein eingelöst.
Nach erfolgreicher Einlösung wirst du automatisch zur Einlöseseite weitergeleitet und kannst den nächsten Gutscheincode einlösen.

## WG Einlösen mit den obigen Hilfsmiteln: Bekannte Probleme seit 01-2023
Durch Änderungen der WG Webseite gibt es derzeit folgende Probleme mit den unten aufgelisteten Addons:  
Redirector:  
Der automatische Redirect zum voreingestellten Wunsch-Shop kann dazu führen, dass keine Wertstufe vorausgewählt ist und sich keine auswählen lässt oder eine falsche Wertstufe vorausgewählt ist.  
Es gibt noch keine Lösung dafür daher empfehle ich derzeit, die automatischen Redirects abzuschalten.
Autofill:  
Wenn man Redirector nicht verwendet kann es sein, dass das Autofill Addon ebenfalls nicht (immer) funktioniert.  
Workaround: Shop-Übersicht nach Eingabe des Gutscheins 1x manuell neuladen und sich zum Ende durchklicken dann sollte Autofill greifen.  
**WG scheint hier außerdem nachgerüstet zu haben und speichert die eingegebenen Daten selbst in den Cookies oder im Local Storage daher ist ein möglicher Workaround, mehrere Browser-Profile zu verwenden statt die hier aufgeführten Addons zu nutzen.  
Das bedeutet für die meisten User dürfte es reichen, sich mehrere Browserprofile anzulegen und die GS ohne das 'Autofill' Addon einzulösen.**  
Ein besserer Ansatz wäre ein Greasemonkey Script.

# ShopCrawler - Vollständige Liste aller Einlösepartner crawlen  
Mit dem ShopCrawler kannst du eine aktuelle Liste aller WG Einlösepartner, einlösbare Wertstufen usw. erstellen lassen.  
Dieser Vorgang kann mehrere Minuten dauern.
1. ShopCrawler.py starten.
2. Nach dem Crawlvorgang finden sich die Daten in den Dateien ``XY_shops.csv`` und ``XY_shops.json``.  
3. Optional:  
Möchte man nur den bestehenden Datenbestand **um neue Shops** aktualisieren, kann man einfach die zuletzt erstellte ``XY_shops.json`` im Ordner liegen lassen und das Script mit dem Parameter ``allow_update_shops`` erneut durchlaufen lassen.

### Mögliche Parameter
```
usage: ShopCrawler.py [-h] [-a ALLOW_UPDATE_SHOPS]
```

# Anleitung Shopliste für Wunschgutschein.at (Österreich) erstellen
Hierfür den Parameter ```wgAT``` in der ```ShopCrawler.py``` auf ```True``` setzen.
                                                                                          
# Liste interner WG Variationen
Diese Variationen definieren mitunter, welche Shops bei welchem Gutschein angezeigt werden.  
09.02.2024: Ich habe die Variation "normal" entfernt, da das Wording so nicht stimmt. Es gibt die nennen wir sie mal "mainstream" WG Typen, die allesamt dieselben Shops bieten.  
Dies sind bei WG Deutschland z.B. alle WG Typen der Variationen ONLINE_DE, REWE, ALDI_SUED und einige mehr.

## WG Variationen Deutschland

|       Distribution        | voucherCategory |                     Typisch verwendet für WG Typ                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Details/Besonderheiten |
|:-------------------------:|-----------------|:--------------------------------------------------------------------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|     MEINSHOPPINGKONTO     | 1               |                   Alle; Einlösung in Shoppingkonto                   | Kann Einträge enthalten, die es bei 'WG normal' nicht gibt. Wichtig für den API Aufruf: Neben dem Distribution Parameter wird der 'voucherValues' Parameter serverseitig erwungen, da auch bei der Einlösung per Webseite der vorher ausgewählte Wert u.B. 50€ immer vollständig eingelöst werden muss. Möchte man alle Shops finden, die übers Shoppingkonto verfügbar sind, muss man die API Anfrage also einmal mit jedem im Shoppingkonto auswählbarem Wert ausführen also 10€,20€, 25€, 50€, 100€ und die Daten dann zusammenführen. |
|       WGSCADOOZ_POR       | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|         ONLINE_DE         | 1               |                            WG Normal Post                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|       ONLINE_DE_PDF       | 1               |                           WG Normal online                           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|           Rewe            | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|         Rossmann          | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|         Kaufland          | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
| ONLINE_GG_TANKSTELLEN_PDF | 29              |         https://geschenkgutscheine.de/products/tankgutschein         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|         ALDI_SUED         | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|     LIDL_OHNE_AMAZON      | 1               |                            WG Normal Lidl                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Ohne Amazon |
|          ONLINE           | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|           EDEKA           | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|       WGSAMAZON POR       | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|         REWE_POR          | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|        LEKKERLAND         | 1               |                     WG normal an Tankstellen(?)                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|           EPAY            | 1               |                ?? Evtl WG online von REWE, Penny usw                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|    REWEPENNYBONUS_POR     | 1               | Bonusguthaben aus den neuen WG Aktionen bei REWE/Penny ohne Payback  |                                                                                                                                                                                                                                                                                                                                                               Beispiel:         https://www.mydealz.de/deals/penny-8-auf-wunschgutschein-via-bonus-wunschgutscheincode-nur-gultig-von-mo-1908-bis-so-25082024-wgs-2408319?page=4#comments |
|        PENNY_PROMO        | 1               | GS, die während neueren Penny Aktionen ~Oktober 2024 verkauft wurden |                                                                                                 
|         EDEKA_ICP         | 1               |                                Edeka                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|        Platzhalter        | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|        Platzhalter        | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|        Platzhalter        | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |


## Weitere WG Distribution Werte als lazy Tabelle
```
ONLINE_DE_PDF
REWE
ONLINE_DE
EDEKA
WGSAMAZON POR
ALDI_SUED
LEKKERLAND
Rossmann
LIDL_OHNE_AMAZON
ONLINE_GG_TANKSTELLEN_PDF
Kaufland
WGSCADOOZ_POR
LIDL
REWE_POR
EPAY
Toom
ONLINE_GG_TANKSTELLEN
ONLINE_LIGHT_DE_PDF
NORMA POR
Eni/Mpreis
ONLINE_AT_PDF
PDF_OHNE_AMAZON
TIBIDONO AT
PENNY_PROMO
Valora DE
HOFER_AT
WGSAMAZON POSA
B2B
ONLINE_LIGHT_DE
MSH
AUFLADEGUTSCHEINESTARTGUTHABENABLAUFDATUM
ONLINE
NKD_DE
ONLINE_PREMIUM_DE_PDF
EDEKA_ICP
KIOSK
Lidl AT
KULANZ_POR_DE
REWEPENNYBONUS_POR
TRINKGUT
PDF
EURONICS
DM
ONLINE_B2B_DE_PDF
RESERVE
```

## WG Variationen Österreich

| Distribution | voucherCategory |             Typisch verwendet für WG Typ             |                                                          Details/Besonderheiten |
|:------------:|-----------------|:----------------------------------------------------:|--------------------------------------------------------------------------------:|
|    Normal    | 2               |                     Platzhalter                      |                                                                     Platzhalter |
| Platzhalter  | 1               |                     Platzhalter                      |                                                                     Platzhalter |


# TODOs
* Shoppingkonto Standardwertstufen im Crawler prüfen und ggf. aktualisieren
* Irgendwas ist immer ;)

# Bekannte Fehlercodes und deren Bedeutung (direkt nach Gutscheineingabe oder Shoppingkonto Einlöseversuch)
|  Fehlercode   |                                                                                                                                       Text                                                                                                                                        |                                                                                                                                                                                                                                                                                          Bedeutung |
|:-------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|     RDMx3     |                                                                                                                       Es ist ein Fehler aufgetreten (RDMx3)                                                                                                                       |                                                                                                                                                                Der GS wurde nach dem Kauf noch nicht aktiviert (Sicherheitssperre 24h oder so). Abwarten und am nächsten Werktag erneut probieren. |
|    RDMx10     |                                                                                                                       Es ist ein Fehler aufgetreten (RDMx10)                                                                                                                       |                                                                                                                                                                      Noch unklar. Passiert eventuell, wenn man kurz nach Start des Wartungsmodus versucht, etwas aus dem Shoppingkonto einzulösen. |
|     STDx5     |                                                                                                                                        ??                                                                                                                                         |                                                                                                                                                    Unbekannt. Passiert vermutlich, wenn sich der GS in diesem Moment aufgrund eines Fehlers nicht beim Einlösepartner erstellen bzw abholen lässt. |
|    STDx11     |                                                                                                                           wgs.std.err.occurred (STDx11)                                                                                                                           |                                                                                                                                                                                       Unbekannt, Passiert eventuell bei Einlöseversuch wenn WG gerade in dem Moment in den Wartungsmodus wechselt. |
|     VCRx1     |                                                                                                                 Bitte achten Sie auf Groß- u. Kleinschreibung...                                                                                                                  |                                                                                                                                                                                                                                                                                        GS ungültig |
|     VCRx8     | Ihr Gutscheincode wurde vom Schenker noch nicht aktiviert. Mit dieser Aktivierung möchten wir sichergehen, dass der Gutschein nicht unerlaubt durch Dritte entwendet wird. Wir haben in diesem Moment an den Schenker eine E-Mail versendet, die ihn an die Aktivierung erinnert. |                                                                                                                                                                                                                                                                                    Selbsterklärend |
|    VCRx9, VCRx54    |                                                                                                                             Voucher has been expired,Dieser WUNSCHGUTSCHEIN-Code kann nicht auf unserer Seite verwendet werden. Mögliche Gründe hierfür könnten sein:Die gesetzliche Verjährungsfrist ist überschritten und Ihr Gutscheincode ist älter als 3 JahreSie haben den Gutscheincode über einen externen Partner erworben                                                                                                                              |                                                                                                                                                                                                                                                        Gutschein abgelaufen (nicht mehr einlösbar) |
|    VCRx10     |                                                                                                                                   Text zu lang                                                                                                                                    |                                                                                                                                                                                                                                        GS wegen Verlust ersetzt oder wg. Diebstahlschutz gesperrt. |
|    VCRx13     |                                                                                                                             Voucher status is unknown                                                                                                                             | Veraltetes Codeformat, Code muss hier re-aktiviert werden: https://app.wunschgutschein.de/reactivate Er ist dann 24 Stunden später einlösbar. Dieser Fehler kann auch bei bereits eingelösten GS kommen. Das Auftauchen dieses Fehlercodes bedeutet also nicht, dass er gültig und einlösbar ist!! |
|    VCRx15     |                                                                                              Es ist ein Fehler aufgetreten. Bitte wenden Sie sich an unseren Kundenservice. (VCRx15)                                                                                              |                                                                                                                                                                                                    Der Code ist noch nicht aktiv (Sicherheitssperre nach Kauf) -> Am nächsten Tag erneut versuchen |
|    VCRx20     |                                                                                                                                      VCRx20                                                                                                                                       |                                                                           Code wurde versucht für eine falsche Kategorie einzulösen (z.B. wenn man versucht, WG Tanken auf der normalen WG Einlöseseite einzulösen). Dieser Fehler sagt noch nichts darüber aus, ob der WG wirklich einlösbar ist! |
|    VCRx25     |                                                                                                                          'Voucher has unexpected status'                                                                                                                          |                                                                                                                                                                                                                                                                                       Keine Ahnung |
|    VCRx49     |                                                                                                                              'Voucher not yet ready'                                                                                                                              |                                                                                                                                                                                                                                                                    Abwarten bis GS aktiviert wird. |
| VCRx51/VCRx52 |                                                                                                                           'User identification needed'                                                                                                                            |                                                    GS lässt sich derzeit nicht einlösen. WG verlangt direkt nach dem Captcha Vorname, Nachname und E-Mail. Wartet man 24-48h ab, ist er 'normal' einlösbar. Einlösung von solchen GS wird mit hoher Wahrscheinlichkeit Geldwäscheprüfung triggern. |


# Bekannte Fehlercodes und deren Bedeutung am Ende der 'anonymen' Einlösung nach Eingabe der persönlichen Daten
Fehler, die erst ganz am Ende des Einlösevorgangs auftreten würden, würden bei einer versuchten Einlösung des GS auf einen Shoppingkonto Accounts meist sofort zu einer temporären Sperre führen!

| Fehlercode | Text           | Bedeutung  |
|:----------:|:-------------:| -----:|
|   STDx6   | Invalid token passed | Session Fehler; erneut versuchen
|   STDx23   | Es ist ein Fehler aufgetreten (STDx23) | Unbekannt/temporärer Fehler
|   RDMx3    | Es ist ein Fehler aufgetreten (RDMx3) | Verursacht instant Accountsperre, würde man diesen GS versuchen auf ein Shoppingkonto aufzuladen. Am nächsten Werktag erneut versuchen.
|   RDMx5    | RDMx5 | Problem beim Einlösepartner
|   RDMx12   | wgs.std.err.occurred (RDMx12) | Unbekannt. Später erneut versuchen.


# Bekannte Fehlercodes und deren Bedeutung ganz am Ende wenn man den Link zum GS bereits per Mail erhalten hat und diesen öffnen will
Fehler, die erst ganz am Ende des Einlösevorgangs auftreten würden, würden bei einer versuchten Einlösung des GS auf einen Shoppingkonto Accounts meist sofort zu einer temporären Sperre führen!

| Fehlercode        | Text           | Bedeutung  |
| :-------------: |:-------------:| -----:|
| RDMx3      | Es ist ein Fehler aufgetreten (RDMx3) | Zu viele GS in kurzer Zeit eingelöst, ggf Geldwäscheprüfung -> Abwarten und es einige Tage später erneut versuchen oder den Support kontaktieren. Kann auch als Vorstufe von RDMx19 erscheinen.
|   RDMx19   | Rdmx19 | Geldwäscheprüfung von WG im Gange. Entweder eine Woche abwarten oder den Support am nächsten Tag kontaktieren.

# Bekannte Fehlercodes und deren Bedeutung nach erfolgreicher Einlösung, wenn die E-Mail mit dem GS nicht kommt und man versucht, sich den GS erneut zuschicken zu lassen
| Fehlercode        | Text           | Bedeutung  |
| :-------------: |:-------------:| -----:|
|   STDx2   | STDx2 | Geldwäscheprüfung von WG im Gange. Entweder eine Woche abwarten oder den Support am nächsten Tag kontaktieren. Solche GS lassen sich bis zur Freischaltung vom Support nicht erneut zuschicken.


# FAQ
**Ich kann bestimmte Einlösepartner z.B. Kaufland nicht auswählen, woran liegt das und was kann ich tun?**  
Manchmal sind die Karten mancher Einlösepartner ausverkauft und deswegen temporär nicht verfügbar oder ein Einlösepartner ist plötzlich keiner mehr (schlimmster Fall), aber in den meisten Fällen greifen seltsame Einschränkungen für Gutscheine aus bestimmten Quellen z.B. kann man auf Amazon gekaufte WGs nicht in Kaufland umwandeln (Stand 21.04.2022).  
Das lässt sich prüfen/umgehen, indem man die Gutscheine auf [Shoppingkonto.de](http://shoppingkonto.de/) auflädt und schaut, ob die *fehlenden* Einlösepartner nun verfügbar sind.

**Die E-Mail mit dem Gutschein kommt nicht an, was kann ich tun?**  
Dafür gibt es zwei mögliche Hauptgründe:  
* Die Einlösung ist gesperrt / Geldwäscheprüfung
* Ein Bug seitens Wunschgutschein, der bei ca 8% aller Einlösungen auftritt -> Hier kann nur der Support helfen
* Probleme mit deiner E-Mail Adresse: Das kannst du ausschließen, indem du dir von einer anderen E-Mail Adresse selbst eine E-Mail schickst.  

Das Problem tritt laut MyDealz Community immer wieder auf ([Beispiel](https://www.mydealz.de/deals/rewe-kartenwelt-5-extra-zum-wunschgutschein-online-offline-2614175#reply-53940569)).

Herausfinden, woran es liegt:  
1. Code neu zusenden lassen.
2. Falls der Code nicht kommt: [Support kontaktieren](https://wunschgutschein.de/kontakt).  
Einige Minuten nachdem du dem WG Support geschrieben hast, solltest du eine automatisierte E-Mail Antwort mit einer Ticketnummer bekommen.  
Falls die nicht kommt, gibt es eventuell Probleme mit deiner E-Mail Adresse.
3. Falls du weitere WG hast und wissen möchtest, ob es sich um eine Sperre oder einen WG Bug handelt, löse einen weiteren Gutschein auf dieselbe E-Mail Adresse ein.  
Wenn der GS ankommt: WG Bug  
Wenn der GS nicht ankommt: Sperre/Geldwäscheprüfung

# Notizen
* Manche Shops haben auch komische Wertstufen z.B. Gymondo: 60, 80
* Manche Shops sind nur in Kategorien auffindbar, aber nicht in der *fake-Kategorie* "keine Kategorie"

# WGs Limits Shoppingkonto
* Max. 300€ pro 24H auszahlen (Steht in [deren AGB](https://www.shoppingkonto.de/agb.html) unter §1.3),  **dieses Limit wird immer um 0 Uhr zurückgesetzt!**
* Accountsperrung bei zu vielen Einlöse-Fehlversuchen??
* Sofortige Accountsperre, wenn man versucht, GS mit Fehler "RDXm3" (ganz am Ende) einzulösen (was man ggf. nicht vorher wissen kann daher im Zweifel die E-Mail Einlösung verwenden)

# WGs Limits E-Mail Einlösung
* Max 200 oder 300€ pro Mail pro 24H

# Bugs/Fehler auf der Wunschgutschein Webseite und im Einlösesystem

| Bekannt seit | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10.04.2025   | **Kaputte Verlinkung von Fehlerseiten** – Klick auf „zur Startseite“ auf einer Fehlerseite (z. B. https://app.wunschgutschein.de/abc) verweist auf falschen Link, sodass man nicht zurück zur Startseite gelangt.                                                                                                                                                                                                                                                         |
| 10.04.2025   | **Weitere kaputte Verlinkungen** – Auf https://geschenkgutscheine.de/products/tankgutschein/ führt der „hier klicken“-Link zu einer ungültigen Adresse (https://b2b.wunschgutschein.de/tankgutschein/). Screenshot des Fehlers im html Code: [Klick](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/52433015_2025_04_10_Bug_Verlinkung_html_Screenshot.jpg)                                                            |
| 10.04.2025   | **Veraltete Werbung für Mobilitätsgutscheine mit D-Ticket** – Auf https://b2b.wunschgutschein.de/pages/mobilitaetsgutschein sowie bei Partnern wie https://kartenwelt.penny.de/wunschgutschein-mobilitat.html wird das D-Ticket noch beworben, obwohl es nicht mehr als Einlösepartner verfügbar ist. [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/52433015_2025_04_10_Bug_Deutschlandcard_beworben.jpg) |
| 01.06.2022   | **Replace-Tag/Platzhalter beim Fehler VCRx10** - Beim Fehler VCRx10 wird **{help_email}** verlinkt, ohne Angabe der E-Mail. [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2022_06_01_Bug_in_Fehlermeldung_VCRx10.jpg)                                                                                                                                                                                    |
| 01.04.2025   | **Manche Gutscheine werden einfach nicht versendet** Mögliche Lösungen/Troubleshooting siehe FAQ über dieser Tabelle.                                                                                                                                                                                                                                                                                                                                                     |
| 01.07.2025   | **Es gibt ein neues Kontaktformular, welches kaputt ist** - https://app.wunschgutschein.de/help/support-request-code -> Egal welchen Code man hier eingibt, man bekommt immer den Fehlercode 422.                                                                                                                                                                                                                                                                         |
| 14.08.2025   | **Shoppingkonto Einlösungen triggern Emails zu Gutscheinen, die sich nicht öffnen lassen.** Wenn man das Shoppingkonto mit einem GS auflädt, wird trotzdem die E-Mail ausgelöst, die man normalerweise beim GS Versand erhält. In diesem Fall leitet der Einlöselink auf eine kaputte Einlöseseite weiter. [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/52433015_2025_08_14_Shoppingkonto_Bug.png)                                                                                                                                                 |
| 08.08.2025   | *Platzhalter*                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
