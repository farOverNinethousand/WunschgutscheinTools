# Wunschgutschein.de und Shoppingkonto.de Tools

Wunschgutschein und shoppingkonto.de Guthaben teil-automatisiert einlösen und vollständige Liste von Wunschgutschein Einlösepartnern automatisch crawlen

# Wunschgutschein Codes und Shoppingkonto.de Guthaben (teil-)automatisiert einlösen
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
``https://einloesen.wunschgutschein.de/shops/10837/amazon``  
Wenn du nur wenige Profile hast und/oder den Einlösepartner ausschließlich über das Redirector Addon steuern möchtest solltest du dafür sorgen, dass alle Autofill Profile für alle Shops gelten.  
Schreibe dafür folgenden Wert in das Site Feld:  
``https://einloesen.wunschgutschein.de/shops/*``  
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

# ShopCrawler - Vollständige Liste aller Einlösepartner crawlen  
Mit dem ShopCrawler kannst du eine aktuelle Liste aller WG Einlösepartner, einlösbare Wertstufen usw. erstellen lassen.  
Dieser Vorgang kann bis zu 45 Minuten dauern.
1. ShopCrawler.py starten.
2. Nach dem Crawlvorgang finden sich die Daten in den Dateien ``shops.csv`` und ``shops.json``.  
3. Optional:  
Möchte man nur den bestehenden Datenbestand **um neue Shops** aktualisieren, kann man einfach die zuletzt erstellte ``shops.json`` im Ordner liegen lassen und das Script mit dem Parameter ``allow_update_shops`` erneut durchlaufen lassen.  
Mehr zu diesem Parameter siehe Liste der Parameter unten.

### Mögliche Parameter
| Parameter        | Erklärung    
| :-------------: |:-------------:|
| skip_vpn_warning      | VPN Warnung am Anfang des Scripts überspringen z.B. nützlich, wenn das Script alle X Zeit automatisch aufgerufen wird.
| allow_update_shops      | Alte shops.json wiederverwenden und nur **neue Shops** crawlen/hinzufügen. Alte Shop-Daten werden nicht aktualisiert und nicht mehr existente Shops bleiben in der Liste!
| csv_skip_inactive_shops      | Als 'inaktiv' markierte Shops nicht mit in die Liste aufnehmen. Was 'inaktiv' bedeutet ist noch unklar daher sollte man diesen Parameter nicht verwenden.
| skip_vpn_warning_ip_check      | Abfrage und Anzeige der IP Adresse in der VPN Warnung deaktivieren.

# TODOs
* Shoplisten-Crawler verbessern (Spalte "Beschreibung" zerschießt die csv, vermutlich wegen nicht escapter Zeichen)
* VoucherHelper aktualisieren (Gutscheincodeformat ohne Bindestrich unterstützen und Erfassung verbessern)

# Relevante WG API Calls
```
https://einloesen.wunschgutschein.de/api/shop/11334

https://einloesen.wunschgutschein.de/api/shop/categories/1
https://einloesen.wunschgutschein.de/api/shop/categories/2
https://einloesen.wunschgutschein.de/api/shop/categories/3

https://einloesen.wunschgutschein.de/api/redeem/maintenance-status

https://einloesen.wunschgutschein.de/api/shop/wall/1?onlyWithLogo=1
https://einloesen.wunschgutschein.de/api/shop/wall/1?distribution=ONLINE_DE_PDF&voucherValue=2500&currency=EUR

https://einloesen.wunschgutschein.de/api/redeem/link/<redeemLinkToken>

https://einloesen.wunschgutschein.de/api/redeem/merchantcode
POST {"redeemLinkToken":"<redeemLinkToken>"}

```

# Bekannte Fehlercodes und deren Bedeutung (direkt nach Gutscheineingabe)
| Fehlercode        | Text           | Bedeutung  |
| :-------------: |:-------------:| -----:|
| VCRx8      | Ihr Gutscheincode wurde vom Schenker noch nicht aktiviert. Mit dieser Aktivierung möchten wir sichergehen, dass der Gutschein nicht unerlaubt durch Dritte entwendet wird. Wir haben in diesem Moment an den Schenker eine E-Mail versendet, die ihn an die Aktivierung erinnert. | Selbsterklärend |
| RDMx3     | Es ist ein Fehler aufgetreten (RDMx3)      |   Der GS wurde nach dem Kauf noch nicht aktiviert (Sicherheitssperre 24h oder so). Abwarten und am nächsten Werktag erneut probieren. |
| STDx11     | wgs.std.err.occurred (STDx11) |   Unbekannt |
| VCRx15     |  Es ist ein Fehler aufgetreten. Bitte wenden Sie sich an unseren Kundenservice. (VCRx15)      |   Der Code ist noch nicht aktiv (Sicherheitssperre nach Kauf) -> Am nächsten Tag erneut versuchen |
| VCRx10     | Text zu lang      |   GS wegen Verlust ersetzt oder wg. Diebstahlschutz gesperrt. |
| VCRx1     | Bitte achten Sie auf Groß- u. Kleinschreibung...      |   GS ungültig |
| DUMMY     | DUMMY      |   DUMMY |

# Bekannte Fehlercodes und deren Bedeutung (am Ende der 'anonymen' Einlösung)
Fehler, die erst ganz am Ende des Einlösevorgangs auftreten würden, würden bei einer versuchten Einlösung des GS auf einen Shoppingkonto Accounts meist sofort zu einer temporären Sperre führen!

| Fehlercode        | Text           | Bedeutung  |
| :-------------: |:-------------:| -----:|
| STDx23      | Es ist ein Fehler aufgetreten (STDx23) | Unbekannt
| RDMx3      | Es ist ein Fehler aufgetreten (RDMx3) | Verursacht instant Accountsperre
| RDMx12      | wgs.std.err.occurred (RDMx12) | Unbekannt
| RDMx5      | RDMx5 | Problem beim Einlösepartner

# FAQ
**Ich kann bestimmte Einlösepartner z.B. Kaufland nicht auswählen, woran liegt das und was kann ich tun?**  
Manchmal sind die Karten mancher Einlösepartner ausverkauft und deswegen temporär nicht verfügbar oder ein Einlösepartner ist plötzlich keiner mehr (schlimmster Fall), aber in den meisten Fällen greifen seltsame Einschränkungen für Gutscheine aus bestimmten Quellen z.B. kann man auf Amazon gekaufte WGs nicht in Kaufland umwandeln (Stand 21.04.2022).  
Das lässt sich prüfen/umgehen, indem man die Gutscheine auf [Shoppingkonto.de](http://shoppingkonto.de/) auflädt und schaut, ob die *fehlenden* Einlösepartner nun verfügbar sind.

# Notizen
* Mögliche Kartenwerte: 10, 15, 20, 25, 50, 100 (100 ist nur mit Zuzahlung möglich)
* Manche Shops haben auch komische Wertstufen z.B. Gymondo: 60, 80
* Manche Shops sind nur in Kategorien auffindbar, aber nicht in der *fake-Kategorie* "keine Kategorie"

# WGs Limits
* Shoppingkonto: Max. 300€ aufladen pro 24H, **Limit wird immer um 0 Uhr zurückgesetzt!!**
* Shoppingkonto: Max. 200€ pro 24H auszahlen (Steht in deren AGB unter §6)
* Shoppingkonto: Max. 24 GS pro Tag und/oder ca. 500€ Aufladung (unbestätigt)
* Shoppingkonto: Accountsperrung bei zu vielen Einlöse-Fehlversuchen??
* Shoppingkonto: Sofortige Accountsperre, wenn man versucht, GS mit Fehler "RDXm3" (ganz am Ende) einzulösen (was man ggf. nicht vorher wissen kann daher im Zweifel die "Anonyme Einlösung" verwenden)
