import os
import sys
import time

# =====================================================================
# CORE IDLE PROJEKT - REVENUE ENGINE & AD-STAGING v8.0
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

def get_b2b_monetization_banner(target_group):
    """
    Generiert hochrelevante Platzhalter für B2B-Werbung und Affiliate-Links,
    die exakt auf die jeweilige Zielgruppe zugeschnitten sind.
    """
    if target_group == "aemter":
        return """
        <div class="ad-banner input-ready">
            <span class="ad-badge">ANZEIGE / EMPFEHLUNG</span>
            <h4>Fachliteratur & Kommentare zum Arbeitszeitgesetz (ArbZG)</h4>
            <p>Rechtssichere Kommentare für Dienststellenleiter und Schichtführer zur rechtssicheren Dienstplanung.</p>
            <a href="#" class="ad-button">Jetzt im Fachhandel ansehen</a>
        </div>
        """
    elif target_group == "betreiber":
        return """
        <div class="ad-banner input-ready">
            <span class="ad-badge">ANZEIGE / EMPFEHLUNG</span>
            <h4>Gesetzlich vorgeschriebene Aushänge für Gewerbebetriebe</h4>
            <p>Erfüllen Sie die Aushangpflicht nach § 16 ArbZG vollständig und schützen Sie Ihr Studio vor Bußgeldern des Gewerbeamtes.</p>
            <a href="#" class="ad-button">Aushang-Paket anfordern</a>
        </div>
        """
    else:
        return """
        <div class="ad-banner input-ready">
            <span class="ad-badge">ANZEIGE / EMPFEHLUNG</span>
            <h4>Vorbereitungsbuch: Die Laufbahnprüfung im Fokus</h4>
            <p>Das Standardwerk für Beamtenanwärter – Didaktik, Prüfungsrelevante Musterklausuren und Gutachtenstil.</p>
            <a href="#" class="ad-button">Lernmaterial sichern</a>
        </div>
        """

def generate_network_with_faqs():
    raw_content = load_index_data()
    if not raw_content:
        print("[FEHLER] Keine 'Zentralregister_Zielgruppen_Index.txt' gefunden!")
        return

    print("\n[AGENT] Schalte Revenue-Engine auf... Injektiere B2B-Werbezonen...")
    data = split_content_by_target(raw_content)

    # Erweitertes CSS für die optische Trennung der Monetarisierungs-Zonen
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
        
        /* REVENUE INTERFACE DESIGN */
        .ad-banner { background: #fffcf4; border: 2px dashed #f39c12; padding: 20px; border-radius: 6px; margin: 25px 0; position: relative; }
        .ad-badge { position: absolute; top: -10px; left: 15px; background: #f39c12; color: white; font-size: 0.7rem; font-weight: bold; padding: 2px 8px; border-radius: 10px; letter-spacing: 0.5px; }
        .ad-banner h4 { color: #d35400; margin-bottom: 5px; font-size: 1.1rem; }
        .ad-banner p { color: #6e7c8c; font-size: 0.9rem; margin-bottom: 12px; }
        .ad-button { display: inline-block; background: #e67e22; color: white; text-decoration: none; padding: 6px 15px; font-size: 0.85rem; font-weight: bold; border-radius: 4px; transition: background 0.2s; }
        .ad-button:hover { background: #d35400; }
        
        footer { text-align: center; padding: 25px; background: #222; color: #888; margin-top: 50px; font-size: 0.85rem; }
    </style>
    <!-- GOOGLE_ADSENSE_STAGING_ZONE -->
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
        f.write(f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
        <title>Zentralregister für Arbeitsschutz & Hygiene | Core Idle Portal</title>
        <meta name="description" content="Offizielles Informationsregister für Arbeitsschutzvorschriften, Ruhezeiten im Schichtdienst und gesetzliche Sicherheitsunterweisungen nach ArbSchG und ArbZG.">
        {shared_style}</head><body>
        <header><h1>Zentralregister für Arbeitsschutz & Hygiene</h1><p>Core Idle Informations-System v8.0</p></header>{nav_bar}
        <div class="container"><div class="hero-box"><h2>Willkommen beim Zentralregister</h2><p>Unser System analysiert fortlaufend die Gesetzestexte des Bundes und bereitet sie in verständlichen Praxis-Leitfäden auf.</p></div>
        {get_b2b_monetization_banner('betreiber')}
        <div class="hero-box" style="border-left-color: #2ecc71; background: #fdfdfd;">
            <h3>📊 Aktueller Datenbank-Status:</h3>
            <p style="margin-top: 10px;">• <strong>Behörden-Terminal:</strong> {len(data['aemter'])} aktive Kontroll-Segmente analysiert.</p>
            <p>• <strong>Betreiber-Kompass:</strong> {len(data['betreiber'])} Sicherheits-Unterweisungen generiert.</p>
            <p>• <strong>Anwärter-Akademie:</strong> {len(data['anwaerter'])} Prüfungsrelevante Normen katalogisiert.</p>
        </div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    # 2. AEMTER.HTML
    faqs_aemter = "".join([generate_faq_logic(b, "aemter") for b in data["aemter"]])
    with open("aemter.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
        <title>Behörden-Terminal | Vorschriften für Schichtdienst & Dienststellenleiter</title>
        <meta name="description" content="Rechtssichere Leitfäden für Schichtdienstleiter und Dienststellen zur Umsetzung von Arbeitszeitverordnungen, Ruhezeiten und behördlichen Auflagen.">
        {shared_style}</head><body>
        <header style="background: linear-gradient(135deg, #1e3c72, #162a4e);"><h1>🏛️ Behörden- & Ämter-Terminal</h1><p>Rechtssicherheit für Dienststellen und Schichtleiter</p></header>{nav_bar}
        <div class="container"><div class="hero-box" style="border-left-color: #1e3c72;"><h2>Praxiswissen für den Dienstbetrieb</h2></div>
        {get_b2b_monetization_banner('aemter')}
        <h3>📌 Häufige Fragen aus der Verwaltungspraxis</h3><div class="faq-container">{faqs_aemter}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    # 3. BETREIBER.HTML
    faqs_betreiber = "".join([generate_faq_logic(b, "betreiber") for b in data["betreiber"]])
    with open("betreiber.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
        <title>Betreiber-Kompass | Sicherheitsunterweisung & Gewerbeamt-Leitfaden</title>
        <meta name="description" content="Praxisnahe Umsetzung der gesetzlichen Sicherheitsunterweisung für Betreiber und Studios nach § 12 ArbSchG zur Vermeidung von Bußgeldern des Gewerbeamtes.">
        {shared_style}</head><body>
        <header style="background: linear-gradient(135deg, #e67e22, #d35400);"><h1>🏢 Betreiber- & Studio-Kompass</h1><p>Vorschriften verständlich erklärt für die Praxis</p></header>{nav_bar}
        <div class="container"><div class="hero-box" style="border-left-color: #e67e22;"><h2>Sicher durch die Betriebsprüfung</h2></div>
        {get_b2b_monetization_banner('betreiber')}
        <h3>📌 Wichtige Betreiber-Fragen im Überblick</h3><div class="faq-container">{faqs_betreiber}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    # 4. ANWAERTER.HTML
    faqs_anwaerter = "".join([generate_faq_logic(b, "anwaerter") for b in data["anwaerter"]])
    with open("anwaerter.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
        <title>Anwärter-Akademie | Klausurenstoff & Aufsichtspflicht für Laufbahnprüfungen</title>
        <meta name="description" content="Gutachterliche Prüfungsschemata und Erläuterungen zu Verordnungen und Arbeitsschutzgesetzen für Beamtenanwärter der Justiz und Verwaltung.">
        {shared_style}</head><body>
        <header style="background: linear-gradient(135deg, #2ecc71, #27ae60);"><h1>🎓 Die Anwärter-Akademie</h1><p>Prüfungserfolg und Didaktik für die Laufbahnprüfung</p></header>{nav_bar}
        <div class="container"><div class="hero-box" style="border-left-color: #2ecc71;"><h2>Lernstoff für die Laufbahnprüfungen</h2></div>
        {get_b2b_monetization_banner('anwaerter')}
        <h3>📌 Klausurrelevante Frage-Muster</h3><div class="faq-container">{faqs_anwaerter}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>""")

    print("[SUCCESS] Revenue-Staging v8.0 abgeschlossen!")

if __name__ == "__main__":
    generate_network_with_faqs()