import os
import sys
import time

# =====================================================================
# CORE IDLE PROJEKT - FAQ ENGINE & DEPLOYMENT PREPARATION v7.0
# =====================================================================

def load_index_data():
    index_file = "Zentralregister_Zielgruppen_Index.txt"
    if not os.path.exists(index_file):
        return None
    with open(index_file, "r", encoding="utf-8") as f:
        return f.read()

def split_content_by_target(raw_content):
    blocks = raw_content.split("-" * 50)
    categorized = {"aemter": [], "betreiber": [], "anwaerter": []}
    
    for block in blocks:
        if "INHALT:" not in block:
            continue
        block_lower = block.lower()
        if "schichtdienst" in block_lower or "ruhezeit" in block_lower:
            categorized["aemter"].append(block)
        if "unterweisung" in block_lower or "gefahr" in block_lower:
            categorized["betreiber"].append(block)
        if "aufsicht" in block_lower or "verordnung" in block_lower or "arbeitszeit" in block_lower:
            categorized["anwaerter"].append(block)
            
    return categorized

def generate_faq_logic(block, target_group):
    lines = block.strip().split("\n")
    quelle, schlagwort, inhalt = "Quelle", "ALLGEMEIN", ""
    for line in lines:
        if line.startswith("QUELLE:"): quelle = line.replace("QUELLE:", "").strip()
        if line.startswith("SCHLAGWORT:"): schlagwort = line.replace("SCHLAGWORT:", "").strip()
        if line.startswith("INHALT:"): inhalt = line.replace("INHALT:", "").strip()
    
    sw_lower = schlagwort.lower()
    
    if target_group == "aemter":
        frage = f"Welche Vorgaben gelten laut Gesetz für {sw_lower} im Dienstbetrieb?"
        antwort = f"Gemäß den Vorschriften (siehe {quelle}) müssen Dienststellenleiter und Schichtführer zwingend darauf achten, dass die gesetzlichen Rahmenbedingungen strikt eingehalten werden. Konkret besagt der Text: {inhalt}"
    elif target_group == "betreiber":
        frage = f"Was müssen Betriebsinhaber beim Thema '{sw_lower}' zwingend beachten?"
        antwort = f"Für Betreiber und Studioleiter besteht hier eine gesetzliche Pflicht zur Umsetzung, um Bußgelder des Gewerbeamtes zu vermeiden. Der Gesetzgeber schreibt vor: {inhalt}"
    else:
        frage = f"Wie wird das Thema '{schlagwort.upper()}' in der Laufbahnprüfung abgefragt?"
        antwort = f"In Klausuren der Verwaltungs- und Justizlaufbahn ist an dieser Stelle sauber gutachterlich zu prüfen, ob die gesetzlichen Tatbestandsmerkmale erfüllt sind. Die maßgebliche Norm definiert hierzu: {inhalt}"

    return f"""
    <div class="faq-item">
        <div class="faq-question">❓ {frage}</div>
        <div class="faq-answer">
            <p><strong>Offizielle Basis ({quelle}):</strong></p>
            <p>{antwort}</p>
        </div>
    </div>
    """

def prepare_deployment_metadata():
    """
    Erstellt die notwendigen Metadaten und Konfigurationen,
    damit das Projekt direkt plattformunabhängig ins Netz geladen werden kann.
    """
    print("\n[AGENT] Starte Phase 4: Online-Staging-Vorbereitung...")
    print("[SYSTEM] Generiere Webserver-Konfiguration und Projekt-Dokumentation...")
    
    # 1. Erstellung einer professionellen README für das Hosting-Repository
    readme_content = """# Zentralregister für Arbeitsschutz & Hygiene
Vollautomatisch generiertes und indexiertes Informationsportal des Core Idle Projekts.

## Struktur
- `index.html` - Hauptportal & Datenbankstatus
- `aemter.html` - Terminal für Behörden & Dienststellenleiter
- `betreiber.html` - Kompass für Gewerbebetreibende & Studios
- `anwaerter.html` - Akademie für den Verwaltungsnachwuchs

## Technologie
- Pure HTML5 / CSS3 (Maximale Pagespeed-Performance für Google Ads)
- Lokale Python-Parsing-Pipeline v7.0
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("[SPEICHERN] Dokumentation erstellt -> README.md")

    # 2. .gitignore hinzufügen, damit deine geheimen .env-Dateien NIEMALS im Internet landen!
    gitignore_content = ".env\n*.pyc\n__pycache__/\n"
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("[SICHERHEIT] Sicherheitsfilter hinterlegt -> .gitignore (.env geschützt)")
    print("[SUCCESS] Staging abgeschlossen. Bereit für den finalen Push ins Web.")

def generate_network_with_faqs():
    raw_content = load_index_data()
    if not raw_content:
        print("[FEHLER] Keine 'Zentralregister_Zielgruppen_Index.txt' gefunden!")
        return

    print("\n[AGENT] Schalte FAQ-Schmiede auf... Generiere Deep-Content-Netzwerk...")
    data = split_content_by_target(raw_content)

    shared_style = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f4f6f9; color: #333; line-height: 1.6; }
        header { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 30px 20px; text-align: center; }
        nav { background: #162a4e; text-align: center; padding: 12px; }
        nav a { color: white; text-decoration: none; margin: 0 20px; font-weight: bold; font-size: 0.95rem; transition: color 0.2s; }
        nav a:hover { color: #2ecc71; }
        .container { max-width: 1000px; margin: 40px auto; padding: 0 20px; }
        .hero-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 30px; border-left: 6px solid #1e3c72; }
        .faq-container { margin-top: 25px; }
        .faq-item { background: white; margin-bottom: 15px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #e9ecef; }
        .faq-question { background: #f8f9fa; padding: 18px 20px; font-weight: bold; color: #1e3c72; border-bottom: 1px solid #edf2f7; font-size: 1.05rem; }
        .faq-answer { padding: 20px; background: white; color: #4a5568; font-size: 0.98rem; }
        footer { text-align: center; padding: 25px; background: #222; color: #888; margin-top: 50px; font-size: 0.85rem; }
    </style>
    """

    nav_bar = """
    <nav>
        <a href="index.html">🏠 Startseite</a>
        <a href="aemter.html">🏛️ Ämter & Behörden</a>
        <a href="betreiber.html">🏢 Betreiber & Studios</a>
        <a href="anwaerter.html">🎓 Beamtenanwärter</a>
    </nav>
    """

    # 1. INDEX.HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Zentralregister | Start</title>{shared_style}</head><body>
        <header><h1>Zentralregister für Arbeitsschutz & Hygiene</h1><p>Core Idle Informations-System v7.0</p></header>{nav_bar}
        <div class="container"><div class="hero-box"><h2>Willkommen beim Zentralregister</h2><p>Unser System analysiert fortlaufend die Gesetzestexte des Bundes und bereitet sie in verständlichen Praxis-Leitfäden auf.</p></div>
        <div class="hero-box" style="border-left-color: #2ecc71; background: #fdfdfd;">
            <h3>📊 Aktueller Datenbank-Status:</h3>
            <p style="margin-top: 10px;">• <strong>Behörden-Terminal:</strong> {len(data['aemter'])} aktive Kontroll-Segmente analysiert.</p>
            <p>• <strong>Betreiber-Kompass:</strong> {len(data['betreiber'])} Sicherheits-Unterweisungen generiert.</p>
            <p>• <strong>Anwärter-Akademie:</strong> {len(data['anwaerter'])} Prüfungsrelevante Normen katalogisiert.</p>
        </div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    # 2. AEMTER.HTML
    faqs_aemter = "".join([generate_faq_logic(b, "aemter") for b in data["aemter"]])
    with open("aemter.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Ämter & Behörden</title>{shared_style}</head><body>
        <header style="background: linear-gradient(135deg, #1e3c72, #162a4e);"><h1>🏛️ Behörden- & Ämter-Terminal</h1><p>Rechtssicherheit für Dienststellen und Schichtleiter</p></header>{nav_bar}
        <div class="container"><div class="hero-box" style="border-left-color: #1e3c72;"><h2>Praxiswissen für den Dienstbetrieb</h2></div>
        <h3>📌 Häufige Fragen aus der Verwaltungspraxis</h3><div class="faq-container">{faqs_aemter}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    # 3. BETREIBER.HTML
    faqs_betreiber = "".join([generate_faq_logic(b, "betreiber") for b in data["betreiber"]])
    with open("betreiber.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Betreiber & Studios</title>{shared_style}</head><body>
        <header style="background: linear-gradient(135deg, #e67e22, #d35400);"><h1>🏢 Betreiber- & Studio-Kompass</h1><p>Vorschriften verständlich erklärt für die Praxis</p></header>{nav_bar}
        <div class="container"><div class="hero-box" style="border-left-color: #e67e22;"><h2>Sicher durch die Betriebsprüfung</h2></div>
        <h3>📌 Wichtige Betreiber-Fragen im Überblick</h3><div class="faq-container">{faqs_betreiber}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    # 4. ANWAERTER.HTML
    faqs_anwaerter = "".join([generate_faq_logic(b, "anwaerter") for b in data["anwaerter"]])
    with open("anwaerter.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Beamtenanwärter</title>{shared_style}</head><body>
        <header style="background: linear-gradient(135deg, #2ecc71, #27ae60);"><h1>🎓 Die Anwärter-Akademie</h1><p>Prüfungserfolg und Didaktik für die Laufbahnprüfung</p></header>{nav_bar}
        <div class="container"><div class="hero-box" style="border-left-color: #2ecc71;"><h2>Lernstoff für die Laufbahnprüfungen</h2></div>
        <h3>📌 Klausurrelevante Frage-Muster</h3><div class="faq-container">{faqs_anwaerter}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    print("[SUCCESS] Content-Schmiede abgeschlossen!")
    
    # Nach der Content-Generierung werfen wir direkt die Online-Schnittstelle an
    prepare_deployment_metadata()

if __name__ == "__main__":
    generate_network_with_faqs()