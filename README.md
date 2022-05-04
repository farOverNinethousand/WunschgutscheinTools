# Wunschgutschein.de und Shoppingkonto.de Tools

Wunschgutschein und shoppingkonto.de Guthaben teil-automatisiert einlösen und vollständige Liste von Wunschgutschein Einlösepartnern automatisch crawlen

# Wunschgutschein Codes (teil-)automatisiert einlösen
### Benötigte Browser Addons
* [Redirector](https://chrome.google.com/webstore/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd)
* [Autofill](https://chrome.google.com/webstore/detail/autofill/nlmmgnhgdeffjkdckmikfpnddkbbfkkk)
1. Die benötigten Addons installieren.
2. Die Datei ``Redirector.json`` herunterladen, in den Optionen des Redirector Addons importieren (Optionen -> Import) und beliebig anpassen bzw. so einstellen, dass es automatisch zum bevorzugten Einlösepartner weiterleitet.
3. Die Datei ``Autofill.txt`` herunterladen.
Dann wie folgt importieren:  
Optionen -> Import/Export -> In das große Textfeld den kompletten Inhalt der Datei einfügen -> Import --> Wechseln ins Tab "Form Fields" -> Links unten auf "Save" klicken.
4. Jetzt in Autofill das Beispielprofil beliebig oft duplizieren und mit eigenen Daten befüllen.  
Mit ALT + G gelangst du zur Übersicht der Profile und kannst bestehende duplizieren/ändern.
Wichtig: Unten bei "Site:" den Link zum Shop angeben für den das Profil gelten soll.  

**Was nun passieren sollte:**  
Du öffnest die Einlöseseite, gibst deinen Gutscheincode ein und bestätigst das Captcha.  
Danach wirst du automatisch zur Shopseite weitergeleitet , musst nur noch 1x auf "Weiter" klicken, deine Daten werden automatisch eingetragen und mit einem weiteren Klick wird der Gutschein eingelöst.
Nach erfolgreicher Einlösung wirst du automatisch zur Einlöseseite weitergeleitet und kannst den nächsten Gutscheincode einlösen.

# **VERALTET!** Vollständige Liste aller Einlösepartner crawlen
1. Einlösesession bei wunschgutschein.de starten:  
   [Hier](https://www.wunschgutschein.de/einloesen/) einen gültigen Gutschein eingeben und den Wert des "PHPSESSID" Cookies kopieren.
2. ShopCrawler.py starten und den Wert des Cookies eingeben.
3. Nach dem Crawlvorgang finden sich die Daten in den Dateien ``shops.csv`` und ``shops.json``.  
Möchte man nur den bestehenden Datenbestand aktualisieren, kann man einfach die letzte ``shops.json`` im Ordner liegen lassen und das Script erneut durchlaufen lassen.  
   Neue Shops werden ggf. ergänzt, bestehende werden nicht aktualisiert und alte nicht gelöscht!

# TODOs
* Shoplisten-Crawler aktualisieren

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
