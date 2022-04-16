# WGs

Wunschgutscheine auf shoppingkonto.de automatisiert einlösen und vollständige Liste von Wunschgutschein Einlösepartnern automatisch crawlen

# **VERALTET!** Vollständige Liste aller Einlösepartner crawlen
1. Einlösesession bei wunschgutschein.de starten:  
   [Hier](https://www.wunschgutschein.de/einloesen/) einen gültigen Gutschein eingeben und den Wert des "PHPSESSID" Cookies kopieren.
2. ShopCrawler.py starten und den Wert des Cookies eingeben.
3. Nach dem Crawlvorgang finden sich die Daten in den Dateien ``shops.csv`` und ``shops.json``.  
Möchte man nur den bestehenden Datenbestand aktualisieren, kann man einfach die letzte ``shops.json`` im Ordner liegen lassen und das Script erneut durchlaufen lassen.  
   Neue Shops werden ggf. ergänzt, bestehende werden nicht aktualisiert und alte nicht gelöscht!

# TODOs
* Shopliste Crawler aktualisieren

# Notizen
* Mögliche Kartenwerte: 10, 15, 20, 25, 50, 100 (100 ist nur mit Zuzahlung möglich)
* Manche Shops haben auch komische Wertstufen z.B. Gymondo: 60, 80
* Manche Shops sind nur in Kategorien auffindbar, aber nicht in der quasi-Kategorie "keine Kategorie"

# WGs Limits
* Shoppingkonto: Max. 300€ pro 24H, **Limit wird immer um 0 Uhr zurückgesetzt!!**
* Shoppingkonto: Max. 24 GS pro Tag und/oder ca. 500€ Aufladung (unbestätigt)
* Shoppingkonto: Accountsperrung bei zu vielen Einlöse-Fehlversuchen??
* Shoppingkonto: Sofortige Accountsperre, wenn man versucht, GS mit Fehler "RDXm3" (ganz am Ende) einzulösen