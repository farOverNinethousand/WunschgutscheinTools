// ==UserScript==
// @name         Shoppingkonto Overlay & CSV Export
// @namespace    https://www.shoppingkonto.de/
// @version      1.2
// @description  Zeige Kundennummer, Einlösevolumen und exportiere Gutscheincodes als CSV
// @author       Dev
// @match        https://www.shoppingkonto.de/transaction/index/*
// @grant        none
// @updateURL    https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/tampermonkey_userscript_shoppingkonto.js
// @downloadURL  https://raw.githubusercontent.com/farOverNinethousand/WunschgutscheinTools/refs/heads/main/tampermonkey_userscript_shoppingkonto.js
// ==/UserScript==

(function() {
    'use strict';

    // ========== HILFSFUNKTIONEN ==========

    // Berechne Einlösesumme der letzten 24 Stunden
    function get24hRedemptionSum() {
        const transactions = extractAllTransactions();
        const now = new Date();
        const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

        let sum = 0;

        transactions.forEach(t => {
            // Nur "Gutschein Einlösung" zählen
            if (t.action.includes('Gutschein Einlösung')) {
                // Checke ob Transaktion innerhalb der letzten 24 Stunden liegt
                if (t.transactionDate >= oneDayAgo && t.transactionDate <= now) {
                    sum += Math.abs(t.amount); // Nimm Absolutwert (da negativ)
                }
            }
        });

        return sum.toFixed(2);
    }

    // Extrahiere aktuelles Guthaben
    function extractBalance() {
        // Suche nach dem Guthaben-Text im HTML
        // "auf Ihrem Shoppingkonto befindet sich Gutschein-Guthaben im Wert von  <br/><span style="font-size: 40px; font-weight: bold;">50,00 EUR!</span>"
        const jumbotron = document.querySelector('.jumbotron');
        if (jumbotron) {
            const text = jumbotron.textContent;
            const match = text.match(/([\d.,]+)\s*EUR/);
            if (match) {
                return match[1];
            }
        }
        return 'unbekannt';
    }

    // Extrahiere Kundennummer aus Profil-Link
    function extractCustomerNumber() {
        const profileLink = document.querySelector('a[href*="/user/edit/"]');
        if (profileLink) {
            const match = profileLink.href.match(/\/user\/edit\/(\d+)/);
            if (match) return match[1];
        }
        return 'unbekannt';
    }

    // Extrahiere Einlösesumme (nur "Wunschgutschein")
    function extractRedemptionSum() {
        // Checke erst, ob der Text "Sie können mit dem Einlösen beginnen, sobald Ihr Shoppingkonto Guthaben hat" vorhanden ist
        const panelBody = document.querySelector('.panel-body');
        if (panelBody && panelBody.textContent.includes('Sie können mit dem Einlösen beginnen')) {
            return '0.00';
        }

        const transactions = extractAllTransactions();
        let total = 0;
        let found = false;

        transactions.forEach(t => {
            // Nur "Wunschgutschein" zählen, NICHT "Gutschein Einlösung"
            if (t.action.includes('Wunschgutschein') && !t.action.includes('Einlösung')) {
                total += t.amount;
                found = true;
            }
        });

        return found ? total.toFixed(2) : 'unbekannt';
    }

    // Crawle alle Transaktionen (Gutscheincodes + Einlösungen) mit geparsten Daten
    function extractAllTransactions() {
        const transactions = [];
        const rows = document.querySelectorAll('table tbody tr');

        for (let row of rows) {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 3) {
                const dateCell = cells[0].textContent.trim();
                const actionCell = cells[1].textContent.trim();
                const amountCell = cells[2].textContent.trim();

                // Überspringe Summenzeile und leere Zeilen
                if (actionCell === '&nbsp;' || actionCell === '' || dateCell === 'Summe' || dateCell === '') {
                    continue;
                }

                // Parse Datum zu Date-Objekt (z.B. "2025-11-11 13:07:52")
                const transactionDate = new Date(dateCell);

                // Extrahiere nur die Zahl aus dem Betrag (z.B. "25,00 EUR" -> 25.00)
                const amountMatch = amountCell.match(/([-]?[\d.,]+)\s*EUR/);
                const amountRaw = amountMatch ? amountMatch[1] : '0';
                const amount = parseFloat(amountRaw.replace(',', '.'));

                transactions.push({
                    timestamp: dateCell,
                    transactionDate: transactionDate,
                    action: actionCell,
                    amountRaw: amountRaw,
                    amount: amount
                });
            }
        }

        return transactions;
    }

    // Erstelle CSV und lade herunter
    function exportToCSV(transactions, customerNumber) {
        let csv = 'Datum,Aktion,Betrag\n';

        transactions.forEach(t => {
            csv += `"${t.timestamp}","${t.action}","${t.amount}"\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);

        // Generiere Dateiname: YYYY_MM_dd_KDNR_shoppingkonto_transaktionen.csv
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const kdnr = customerNumber !== 'unbekannt' ? customerNumber : 'kdnr_unbekannt';
        const filename = `${year}_${month}_${day}_${kdnr}_shoppingkonto_transaktionen.csv`;

        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // ========== HAUPT-LOGIK ==========

    function createOverlay() {
        // Extrahiere Daten
        const customerNumber = extractCustomerNumber();
        const balance = extractBalance();
        const redemptionSum = extractRedemptionSum();
        const redemptionSum24h = get24hRedemptionSum();
        const transactions = extractAllTransactions();

        // Zähle nur Wunschgutschein Transaktionen
        const voucherCount = transactions.filter(t => t.action.includes('Wunschgutschein')).length;
        // Zähle nur Gutschein Einlösungen
        const redemptionCount = transactions.filter(t => t.action.includes('Gutschein Einlösung')).length;

        // Bestimme Hintergrundfarbe basierend auf 24h Einlösesumme
        const sum24hNum = parseFloat(redemptionSum24h);
        const isHighVolume = sum24hNum >= 300;
        const backgroundColor = isHighVolume ? 'rgba(255, 0, 0, 0.85)' : 'rgba(0, 0, 0, 0.85)';
        const borderColor = isHighVolume ? '#ff0000' : 'lime';
        const textColor = isHighVolume ? '#ff0000' : 'lime';

        // Erstelle Overlay
        const overlay = document.createElement('div');
        overlay.id = 'shoppingkonto-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${backgroundColor};
            border: 2px solid ${borderColor};
            border-radius: 8px;
            padding: 15px;
            font-family: monospace;
            font-size: 14px;
            color: ${textColor};
            z-index: 10000;
            box-shadow: 0 0 10px rgba(${isHighVolume ? '255, 0, 0' : '0, 255, 0'}, 0.5);
            max-width: 300px;
            transition: all 0.3s ease;
        `;

        overlay.innerHTML = `
            <div id="overlay-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="flex: 1;"></div>
                <button id="toggle-overlay-btn" style="
                    background: transparent;
                    border: none;
                    color: inherit;
                    font-size: 18px;
                    cursor: pointer;
                    padding: 0;
                    margin-left: 10px;
                ">✕</button>
            </div>
            <div id="overlay-content" style="display: block;">
                <div style="margin-bottom: 15px; text-align: center; border-bottom: 1px solid; padding-bottom: 10px;">
                    <strong style="font-size: 12px;">ShoppingkontoHelper V 1.2</strong>
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Kundennummer:</strong> ${customerNumber}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Guthaben:</strong> ${balance}${balance !== 'unbekannt' ? ' €' : ''}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Einlösesumme:</strong> ${redemptionSum}${redemptionSum !== 'unbekannt' ? ' €' : ''}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Einlösesumme 24h:</strong> ${redemptionSum24h}€/300.00€
                </div>
                <div style="margin-bottom: 15px; font-size: 11px; opacity: 0.8;">
                    Limit laut <a href="https://www.shoppingkonto.de/agb.html#:~:text=EUR%20300" target="_blank" style="color: inherit; text-decoration: underline;">AGB</a>
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Transaktionen:</strong> ${transactions.length}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Davon Gutscheincodes:</strong> ${voucherCount}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Davon Einlösungen:</strong> ${redemptionCount}
                </div>
                <button id="csv-export-btn" style="
                    background: ${isHighVolume ? '#ff0000' : 'lime'};
                    color: ${isHighVolume ? 'white' : 'black'};
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    width: 100%;
                    transition: all 0.2s;
                ">
                    CSV Export (${transactions.length} Einträge)
                </button>
            </div>
        `;

        document.body.appendChild(overlay);

        // Toggle Button Funktionalität
        let isVisible = true;
        const toggleBtn = document.getElementById('toggle-overlay-btn');
        const overlayContent = document.getElementById('overlay-content');

        toggleBtn.addEventListener('click', function() {
            isVisible = !isVisible;

            if (isVisible) {
                // Box maximieren
                overlayContent.style.display = 'block';
                overlay.style.background = isHighVolume ? 'rgba(255, 0, 0, 0.85)' : 'rgba(0, 0, 0, 0.85)';
                overlay.style.border = `2px solid ${borderColor}`;
                overlay.style.padding = '15px';
                toggleBtn.textContent = '✕';
            } else {
                // Box minimieren
                overlayContent.style.display = 'none';
                overlay.style.background = 'transparent';
                overlay.style.border = 'none';
                overlay.style.padding = '5px';
                toggleBtn.textContent = '→';
            }
        });

        // CSV Export Button Listener
        document.getElementById('csv-export-btn').addEventListener('click', function() {
            if (transactions.length > 0) {
                exportToCSV(transactions, customerNumber);
                this.textContent = '✓ Export erfolgreich!';
                this.style.background = isHighVolume ? '#ff0000' : 'lime';
                setTimeout(() => {
                    this.textContent = `CSV Export (${transactions.length} Einträge)`;
                }, 2000);
            } else {
                alert('Keine Transaktionen gefunden!');
            }
        });

        // Hover-Effekt für Button
        document.getElementById('csv-export-btn').addEventListener('mouseover', function() {
            this.style.background = isHighVolume ? '#ff3333' : '#00ff00';
            this.style.boxShadow = isHighVolume ? '0 0 5px red' : '0 0 5px lime';
        });

        document.getElementById('csv-export-btn').addEventListener('mouseout', function() {
            this.style.background = isHighVolume ? '#ff0000' : 'lime';
            this.style.boxShadow = 'none';
        });
    }

    // Starte Script nach Seitenladung
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createOverlay);
    } else {
        createOverlay();
    }
})();