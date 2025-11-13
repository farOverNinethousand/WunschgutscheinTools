# Wunschgutschein.de, Wunschgutschein.at und Shoppingkonto.de Tools

wunschgutschein.de/wunschgutschein.at/restaurantgutschein.net Gutscheine und shoppingkonto.de Guthaben teil-automatisiert einlösen und vollständige Liste von Wunschgutschein Einlösepartnern mitsamt verfügbarer Wertstufen automatisch crawlen

# Fertige Shoplisten
Wer zu faul ist, die Shopliste selbst zu crawlen, findet unter folgendem Link eine Sammlung von Shoplisten, die in unregelmäßigen Abständen aktualisiert wird:  
https://mega.nz/folder/HehC1JyK#v5R3VoyOGnoIU6dHKU1vIg  
**Wichtig:**  
Diese Shopliste enthält auch Shops, die nicht bei allen Wunschgutschein-Varianten verfügbar sind also nur weil irgendwo *Aral* oder *ESSO* steht bedeutet dies nicht, dass man mit normalen Wunschgutscheinen direkt an Tankgutscheine kommt!  
Beachtet die Spalte "*Verfügbar in unique WG Variationen*"!!  
Die klassischen WG Tankgutscheine gibt es nur unter [geschenkgutscheine.de/products/tankgutschein](https://geschenkgutscheine.de/products/tankgutschein).


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

# Anleitung Shopliste für wunschgutschein.at (Österreich) erstellen
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
|    Egal, aber oft REWE    | 30              |     https://www.wunschgutschein.de/products/mobilitats-gutschein     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Gab es bis Oktober 2025 in vielen Kaufland Filialen. |
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
|           TODO            | 36              |       [Restaurantgutschein](https://restaurantgutschein.net/)        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Platzhalter |
|        Platzhalter        | 1               |                             Platzhalter                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Einlösung kaputt Stand 14.10.2025 |
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
|  Fehlercode   |                                                                                                                                                  Text                                                                                                                                                   |                                                                                                                                                                                                                                                                                          Bedeutung |
|:-------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|     RDMx3     |                                                                                                                                  Es ist ein Fehler aufgetreten (RDMx3)                                                                                                                                  |                                                                                                                                                                Der GS wurde nach dem Kauf noch nicht aktiviert (Sicherheitssperre 24h oder so). Abwarten und am nächsten Werktag erneut probieren. |
|    RDMx10     |                                                                                                                                 Es ist ein Fehler aufgetreten (RDMx10)                                                                                                                                  |                                                                                                                                                                      Noch unklar. Passiert eventuell, wenn man kurz nach Start des Wartungsmodus versucht, etwas aus dem Shoppingkonto einzulösen. |
|     STDx5     |                                                                                                                                                   ??                                                                                                                                                    |                                                                                                                                                    Unbekannt. Passiert vermutlich, wenn sich der GS in diesem Moment aufgrund eines Fehlers nicht beim Einlösepartner erstellen bzw abholen lässt. |
|    STDx11     |                                                                                                                                      wgs.std.err.occurred (STDx11)                                                                                                                                      |                                                                                                                                                                                       Unbekannt, Passiert eventuell bei Einlöseversuch wenn WG gerade in dem Moment in den Wartungsmodus wechselt. |
|     VCRx1     |                                                                                                                            Bitte achten Sie auf Groß- u. Kleinschreibung...                                                                                                                             |                                                                                                                                                                                                                                                                                        GS ungültig |
|     VCRx8     |            Ihr Gutscheincode wurde vom Schenker noch nicht aktiviert. Mit dieser Aktivierung möchten wir sichergehen, dass der Gutschein nicht unerlaubt durch Dritte entwendet wird. Wir haben in diesem Moment an den Schenker eine E-Mail versendet, die ihn an die Aktivierung erinnert.            |                                                                                                                                                                                                                                                                                    Selbsterklärend |
| VCRx9, VCRx54 | Voucher has been expired,Dieser WUNSCHGUTSCHEIN-Code kann nicht auf unserer Seite verwendet werden. Mögliche Gründe hierfür könnten sein:Die gesetzliche Verjährungsfrist ist überschritten und Ihr Gutscheincode ist älter als 3 JahreSie haben den Gutscheincode über einen externen Partner erworben |                                                                                                                                                                                                                                                        Gutschein abgelaufen (nicht mehr einlösbar) |
|    VCRx10     |                                                                                                                                              Text zu lang                                                                                                                                               |                                                                                                                                                                                                                                        GS wegen Verlust ersetzt oder wg. Diebstahlschutz gesperrt. |
|    VCRx13     |                                                                                                                                        Voucher status is unknown                                                                                                                                        | Veraltetes Codeformat, Code muss hier re-aktiviert werden: https://app.wunschgutschein.de/reactivate Er ist dann 24 Stunden später einlösbar. Dieser Fehler kann auch bei bereits eingelösten GS kommen. Das Auftauchen dieses Fehlercodes bedeutet also nicht, dass er gültig und einlösbar ist!! |
|    VCRx15     |                                                                                                         Es ist ein Fehler aufgetreten. Bitte wenden Sie sich an unseren Kundenservice. (VCRx15)                                                                                                         |                                                                                                                                                                                                    Der Code ist noch nicht aktiv (Sicherheitssperre nach Kauf) -> Am nächsten Tag erneut versuchen |
|    VCRx20     |                                                                                                                                                 VCRx20                                                                                                                                                  |                                                                           Code wurde versucht für eine falsche Kategorie einzulösen (z.B. wenn man versucht, WG Tanken auf der normalen WG Einlöseseite einzulösen). Dieser Fehler sagt noch nichts darüber aus, ob der WG wirklich einlösbar ist! |
|    VCRx25     |                                                                                                                                     'Voucher has unexpected status'                                                                                                                                     |                                                                                                                                                                                                                                                                                       Keine Ahnung |
|    VCRx49     |                                                                                                                                         'Voucher not yet ready'                                                                                                                                         |                                                                                                                                                                                                                                                                    Abwarten bis GS aktiviert wird. |
| VCRx51/VCRx52 |                                                                                                                                      'User identification needed'                                                                                                                                       |                                                    GS lässt sich derzeit nicht einlösen. WG verlangt direkt nach dem Captcha Vorname, Nachname und E-Mail. Wartet man 24-48h ab, ist er 'normal' einlösbar. Einlösung von solchen GS wird mit hoher Wahrscheinlichkeit Geldwäscheprüfung triggern. |
|    VCRx54     |                                                                                                                                       'Voucher has been expired.'                                                                                                                                       |                                                                                                                                                                                                                                                             GS abgelaufen. Nachfolger von VCRx9??! |


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

| Bekannt seit | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Behoben am |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| 10.04.2025   | **Kaputte Verlinkung von Fehlerseiten** – Klick auf „zur Startseite“ auf einer Fehlerseite (z. B. https://app.wunschgutschein.de/abc) verweist auf falschen Link, sodass man nicht zurück zur Startseite gelangt.                                                                                                                                                                                                                                                 |            |
| 10.04.2025   | **Weitere kaputte Verlinkungen** – Auf https://geschenkgutscheine.de/products/tankgutschein/ führt der „hier klicken“-Link zu einer ungültigen Adresse (https://b2b.wunschgutschein.de/tankgutschein/). Screenshot des Fehlers im html Code: [Klick](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2025_04_10_Bug_Verlinkung_html_Screenshot.jpg)                                                             |            |
| 10.04.2025   | **Veraltete Werbung für Mobilitätsgutscheine mit D-Ticket** – Auf https://b2b.wunschgutschein.de/pages/mobilitaetsgutschein sowie bei Partnern wie https://kartenwelt.penny.de/wunschgutschein-mobilitat.html wird das D-Ticket noch beworben, obwohl es nicht mehr als Einlösepartner verfügbar ist. [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2025_04_10_Bug_Deutschlandcard_beworben.jpg) |            |
| 01.06.2022   | **Replace-Tag/Platzhalter beim Fehler VCRx10** - Beim Fehler VCRx10 wird **{help_email}** verlinkt, ohne Angabe der E-Mail. [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2022_06_01_Bug_in_Fehlermeldung_VCRx10.jpg)                                                                                                                                                                            |            |
| 01.04.2025   | **Manche Gutscheine werden einfach nicht versendet** Mögliche Lösungen/Troubleshooting siehe FAQ über dieser Tabelle.                                                                                                                                                                                                                                                                                                                                             |            |
| 01.07.2025   | **Es gibt ein neues Kontaktformular, welches kaputt ist** - https://app.wunschgutschein.de/help/support-request-code -> Egal welchen Code man hier eingibt, man bekommt immer den Fehlercode 422.                                                                                                                                                                                                                                                                 |            |
| 14.08.2025   | **Shoppingkonto Einlösungen triggern Emails zu Gutscheinen, die sich nicht öffnen lassen.** Wenn man das Shoppingkonto mit einem GS auflädt, wird trotzdem die E-Mail ausgelöst, die man normalerweise beim GS Versand erhält. In diesem Fall leitet der Einlöselink auf eine kaputte Einlöseseite weiter. [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2025_08_14_Shoppingkonto_Bug.png)       |            |
| ~~14.10.2025~~   | Restaurantgutschein.net Einlösung funktioniert nicht: Fehler "Ungültige Domain für Webseitenschlüssel". [Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2025_10_14_restaurantgutschein_net_bug_1.png)                                                                                                                                                                                              | 06.11.2025 |
| 08.08.2025   | Wunschgutschein.de irreführende Fehlermeldung, wenn man als dummer User hier versucht, einen Restaurantgutschein einzulösen ([Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2025_10_14_restaurantgutschein_net_bug_2.png)). Korrekte Fehlermeldung wäre: "Der angegebene Gutscheincode ist nur unter https://restaurantgutschein.net einlösbar."                                                  |            |
| 06.11.2025   | Gutscheinversand an Freenet E-Mail Adressen funktioniert nicht mehr. Auch der Neuversand alter GS an Freenet E-Mail Adressen funktioniert nicht. Entweder Freenet blockiert die WG GS-Emails oder WG hat ein Problem. In ersterem Fall sollte WG sich darum kümmern, dass Freenet sie entsperrt, ist also als WG Bug anzusehen.                                                                                                                                   |            |
| 08.08.2025   | *Platzhalter*                                                                                                                                                                                                                                                                                                                                                                                                                                                     |            |

# Userscript ShoppingkontoHelper

![ShoppingkontoHelper Screenshot](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/Bilder/2025_11_13_Showcase_ShoppingkontoHelper.png)


## Schritt 1: Tampermonkey installieren

Wähle deinen Browser:

### Chrome/Edge
1. Gehe zu [Chrome Web Store - Tampermonkey](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
2. Klicke auf "Zu Chrome hinzufügen"
3. Bestätige die Installation
4. Rechtsklick auf das Tampermonkey Symbol -> Erweiterung verwalten -> Oben rechts den Entwicklermodus aktivieren und mittig "Nutzerscripts zulassen" aktivieren.

### Firefox
1. Gehe zu [Firefox Add-ons - Tampermonkey](https://addons.mozilla.org/de/firefox/addon/tampermonkey/)
2. Klicke auf "Zu Firefox hinzufügen"
3. Bestätige die Installation

### Safari
1. Gehe zu [App Store - Tampermonkey](https://apps.apple.com/de/app/tampermonkey/id1482490089)
2. Installiere die App
3. Aktiviere Tampermonkey in den Safari-Einstellungen

---

## Schritt 2: ShoppingkontoHelper installieren

Link zum Script:  
```
https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/tampermonkey_userscript_shoppingkonto.js
```

Installation mit einem Klick: [Ausprobieren](https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/tampermonkey_userscript_shoppingkonto.js)
Falls das nicht funktioniert:  

1. Tampermonkey öffnen (Browser-Icon oben rechts)
2. Auf "+" klicken (Neues Script)
3. Den obigen .js Link öffnen und den kompletten Code einfügen.
4. Mit `Ctrl+S` speichern

---

## Schritt 3: Script aktivieren

1. Gehe im eingeloggten Zustand zu https://www.shoppingkonto.de/transaction/index/
2. Das grüne Overlay sollte oben rechts erscheinen
3. Fertig! 🎉

---

## Features

- Kundennummer anzeigen
- Guthaben und Einlösesummen
- Anzeige des Einlöselimits
- CSV-Export aller Transaktionen
- Warnung bei Limit-Überschreitung

---

## Tipps

- Klick auf **✕** um die Box zu minimieren
- Klick auf **→** um die Box wiederherzustellen
- Der CSV-Export enthält alle Transaktionen
- Die Box aktualisiert sich beim Neuladen der Seite

# ShoppingkontoHelper FAQ

**Kann mein Shoppingkonto durch die Verwendung von ShoppingkontoHelper gesperrt werden?**  
Nein.

**Können die Betreiber von Shoppingkonto.de sehen, dass ich ShoppingkontoHelper verwende?**  
Nein.

Ich bin in einer Prüfung gelandet, obwohl ich keine Einlöselimits überschritten habe, wie kann das sein?  
Den Algo, der die Sperren auslöst kennen nur die Betreiber von Shoppingkonto.de