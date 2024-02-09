# Wunschgutschein.de, Wunschgutschein.at und Shoppingkonto.de Tools

Wunschgutschein und shoppingkonto.de/.at Guthaben teil-automatisiert einlösen und vollständige Liste von Wunschgutschein Einlösepartnern mitsamt verfügbarer Wertstufen automatisch crawlen

# Fertige Shoplisten
Wer zu faul ist, die Shopliste selbst zu crawlen, findet unter folgendem Link eine Sammlung von Shoplisten, die in unregelmäßigen Abständen aktualisiert wird:  
https://mega.nz/folder/HehC1JyK#v5R3VoyOGnoIU6dHKU1vIg  
**Wichtig:**  
Diese shopliste kann Shops enthalten, die nicht bei allen Wunschgutschein-Varianten verfügbar sind. Dies ist kein Fehler!  
Die Shops für alle existierenden WG Varianten separat herauszufinden wäre ein sehr hoher Aufwand und man bräuchte aktive Sessions also gültige Gutscheine für jeden WG Typ.  
Beispiel: Aral/Shell/Esso also Tankstellengutscheine werden zwar gelistet, aber sind eigentlich nur wirklich auswählbar, wenn man einen WG Tankgutschein z.B. von hier kauft:  
https://geschenkgutscheine.de/products/tankgutschein  
und:  
https://app.wunschgutschein.de/mobilitaet  
Mehr Infos:  
https://www.mydealz.de/diskussion/wunschgutschein-in-shell-geht-nicht-1707965**

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

|       Distribution        | voucherCategory |             Typisch verwendet für WG Typ             |                                                          Details/Besonderheiten |
|:-------------------------:|-----------------|:----------------------------------------------------:|--------------------------------------------------------------------------------:|
|     MEINSHOPPINGKONTO     | 1               |           Alle; Einlösung in Shoppingkonto           | Enthält einige Einträge, die es bei WG normal nicht gibt z.B. REWE, Aral, Shell |
|       WGSCADOOZ_POR       | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|         ONLINE_DE         | 1               |                    WG Normal Post                    |                                                                     Platzhalter |
|       ONLINE_DE_PDF       | 1               |                   WG Normal online                   |                                                                     Platzhalter |
|           Rewe            | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|         Rossmann          | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|         Kaufland          | 1               |                     Platzhalter                      |                                                                     Platzhalter |
| ONLINE_GG_TANKSTELLEN_PDF | 29              | https://geschenkgutscheine.de/products/tankgutschein |                                                                     Platzhalter |
|         ALDI_SUED         | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|     LIDL_OHNE_AMAZON      | 1               |                    WG Normal Lidl                    |                                                                     Ohne Amazon |
|          ONLINE           | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|           EDEKA           | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|       WGSAMAZON POR       | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|         REWE_POR          | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|        LEKKERLAND         | 1               |             WG normal an Tankstellen(?)              |                                                                     Platzhalter |
|           EPAY            | 1               |        ?? Evtl WG online von REWE, Penny usw         |                                                                     Platzhalter |
|        Platzhalter        | 1               |                     Platzhalter                      |                                                                     Platzhalter |
|        Platzhalter        | 1               |                     Platzhalter                      |                                                                     Platzhalter |

## WG Variationen Österreich

| Distribution | voucherCategory |             Typisch verwendet für WG Typ             |                                                          Details/Besonderheiten |
|:------------:|-----------------|:----------------------------------------------------:|--------------------------------------------------------------------------------:|
|    Normal    | 2               |                     Platzhalter                      |                                                                     Platzhalter |
| Platzhalter  | 1               |                     Platzhalter                      |                                                                     Platzhalter |


# TODOs
* Irgendwas ist immer ;)

# Bekannte Fehlercodes und deren Bedeutung (direkt nach Gutscheineingabe)
| Fehlercode        | Text           | Bedeutung  |
| :-------------: |:-------------:| -----:|
| VCRx8      | Ihr Gutscheincode wurde vom Schenker noch nicht aktiviert. Mit dieser Aktivierung möchten wir sichergehen, dass der Gutschein nicht unerlaubt durch Dritte entwendet wird. Wir haben in diesem Moment an den Schenker eine E-Mail versendet, die ihn an die Aktivierung erinnert. | Selbsterklärend |
| RDMx3     | Es ist ein Fehler aufgetreten (RDMx3)      |   Der GS wurde nach dem Kauf noch nicht aktiviert (Sicherheitssperre 24h oder so). Abwarten und am nächsten Werktag erneut probieren. |
| STDx11     | wgs.std.err.occurred (STDx11) |   Unbekannt |
| VCRx15     |  Es ist ein Fehler aufgetreten. Bitte wenden Sie sich an unseren Kundenservice. (VCRx15)      |   Der Code ist noch nicht aktiv (Sicherheitssperre nach Kauf) -> Am nächsten Tag erneut versuchen |
| VCRx10     | Text zu lang      |   GS wegen Verlust ersetzt oder wg. Diebstahlschutz gesperrt. |
| VCRx1     | Bitte achten Sie auf Groß- u. Kleinschreibung...      |   GS ungültig |

# Bekannte Fehlercodes und deren Bedeutung (am Ende der 'anonymen' Einlösung nach Eingabe der persönlichen Daten)
Fehler, die erst ganz am Ende des Einlösevorgangs auftreten würden, würden bei einer versuchten Einlösung des GS auf einen Shoppingkonto Accounts meist sofort zu einer temporären Sperre führen!

| Fehlercode | Text           | Bedeutung  |
|:----------:|:-------------:| -----:|
|   STDx23   | Es ist ein Fehler aufgetreten (STDx23) | Unbekannt
|   RDMx3    | Es ist ein Fehler aufgetreten (RDMx3) | Verursacht instant Accountsperre, würde man diesen GS versuchen auf ein Shoppingkonto aufzuladen
|   RDMx5    | RDMx5 | Problem beim Einlösepartner
|   RDMx12   | wgs.std.err.occurred (RDMx12) | Unbekannt. Später erneut versuchen.


# Bekannte Fehlercodes und deren Bedeutung (ganz am Ende wenn man den Link zum GS bereits per Mail erhalten hat und diesen öffnen will)
Fehler, die erst ganz am Ende des Einlösevorgangs auftreten würden, würden bei einer versuchten Einlösung des GS auf einen Shoppingkonto Accounts meist sofort zu einer temporären Sperre führen!

| Fehlercode        | Text           | Bedeutung  |
| :-------------: |:-------------:| -----:|
| RDMx3      | Es ist ein Fehler aufgetreten (RDMx3) | Zu viele GS in kurzer Zeit eingelöst -> Abwarten und es einige Tage später erneut versuchen oder den Support kontaktieren. Kann auch als Vorstufe von RDMx19 erscheinen.
|   RDMx19   | Rdmx19 | Geldwäscheprüfung von WG im Gange. Entweder eine Woche abwarten oder den Support am nächsten Tag kontaktieren.

# FAQ
**Ich kann bestimmte Einlösepartner z.B. Kaufland nicht auswählen, woran liegt das und was kann ich tun?**  
Manchmal sind die Karten mancher Einlösepartner ausverkauft und deswegen temporär nicht verfügbar oder ein Einlösepartner ist plötzlich keiner mehr (schlimmster Fall), aber in den meisten Fällen greifen seltsame Einschränkungen für Gutscheine aus bestimmten Quellen z.B. kann man auf Amazon gekaufte WGs nicht in Kaufland umwandeln (Stand 21.04.2022).  
Das lässt sich prüfen/umgehen, indem man die Gutscheine auf [Shoppingkonto.de](http://shoppingkonto.de/) auflädt und schaut, ob die *fehlenden* Einlösepartner nun verfügbar sind.

# Notizen
* Manche Shops haben auch komische Wertstufen z.B. Gymondo: 60, 80
* Manche Shops sind nur in Kategorien auffindbar, aber nicht in der *fake-Kategorie* "keine Kategorie"

# WGs Limits Shoppingkonto
* Max. 300€ pro 24H auszahlen (Steht in [deren AGB](https://www.shoppingkonto.de/agb.html) unter §1.3),  **dieses Limit wird immer um 0 Uhr zurückgesetzt!**
* Accountsperrung bei zu vielen Einlöse-Fehlversuchen??
* Sofortige Accountsperre, wenn man versucht, GS mit Fehler "RDXm3" (ganz am Ende) einzulösen (was man ggf. nicht vorher wissen kann daher im Zweifel die E-Mail Einlösung verwenden)

# WGs Limits E-Mail Einlösung
* Max 200 oder 300€ pro Mail pro 24H