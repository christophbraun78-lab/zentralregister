import os
import sys

# =====================================================================
# CORE IDLE PROJEKT - REVENUE ENGINE & BRANDING v11.5
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

    return f'<div class="faq-item"><div class="faq-question">❓ {frage}</div><div class="faq-answer"><p><strong>Offizielle Basis ({quelle}):</strong></p><p>{antwort}</p></div></div>'

def get_b2b_monetization_banner(target_group):
    if target_group == "aemter":
        return '<div class="ad-banner"><span class="ad-badge">ANZEIGE / EMPFEHLUNG</span><h4>Fachliteratur & Kommentare zum Arbeitszeitgesetz (ArbZG)</h4><p>Rechtssichere Kommentare für Dienststellenleiter und Schichtführer zur rechtssicheren Dienstplanung.</p><a href="#" class="ad-button">Jetzt im Fachhandel ansehen</a></div>'
    elif target_group == "betreiber":
        return '<div class="ad-banner"><span class="ad-badge">ANZEIGE / EMPFEHLUNG</span><h4>Gesetzlich vorgeschriebene Aushänge für Gewerbebetriebe</h4><p>Erfüllen Sie die Aushangpflicht nach § 16 ArbZG vollständig und schützen Sie Ihr Studio vor Bußgeldern des Gewerbeamtes.</p><a href="#" class="ad-button">Aushang-Paket anfordern</a></div>'
    else:
        return '<div class="ad-banner"><span class="ad-badge">ANZEIGE / EMPFEHLUNG</span><h4>Vorbereitungsbuch: Die Laufbahnprüfung im Fokus</h4><p>Das Standardwerk für Beamtenanwärter – Didaktik, Prüfungsrelevante Musterklausuren und Gutachtenstil.</p><a href="#" class="ad-button">Lernmaterial sichern</a></div>'

def generate_sitemap_xml():
    print("[SYSTEM] Generiere digitale Landkarte für Google -> sitemap.xml...")
    base_url = "https://christophbraun78-lab.github.io/zentralregister/"
    pages = ["index.html", "aemter.html", "betreiber.html", "anwaerter.html"]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml_content += f'  <url>\n    <loc>{base_url}{page}</loc>\n    <priority>{"1.0" if page == "index.html" else "0.8"}</priority>\n  </url>\n'
    xml_content += '</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("[SUCCESS] sitemap.xml wurde fehlerfrei geschrieben!")

def prepare_deployment_metadata():
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Praxis-Kompass Arbeitsschutz\nCore Idle Projekt Informationsnetzwerk.\n")
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(".env\n*.pyc\n__pycache__/\n")

def generate_network_with_faqs():
    raw_content = load_index_data()
    if not raw_content:
        print("[FEHLER] Keine 'Zentralregister_Zielgruppen_Index.txt' gefunden!")
        return

    if os.path.exists("style.css"):
        with open("style.css", "r", encoding="utf-8") as css_f:
            clean_style = '<style>' + css_f.read() + '</style>'
    else:
        clean_style = '<style>body { font-family: sans-serif; }</style>'

    print("\n[AGENT] Schalte Revenue-Engine auf... Injektiere Praxis-Kompass Branding...")
    data = split_content_by_target(raw_content)

    nav_bar = '<nav><a href="index.html">🏠 Startseite</a><a href="aemter.html">🏛️ Ämter & Behörden</a><a href="betreiber.html">🏢 Betreiber & Studios</a><a href="anwaerter.html">🎓 Beamtenanwärter</a></nav>'

    google_tag = '<meta name="google-site-verification" content="HJYQ9n7LlloJpf-macnCXQR1E38ckMVlT3czmLz-RBs" />'

    # 1. INDEX.HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">{google_tag}<title>Praxis-Kompass Arbeitsschutz | Start</title><meta name="description" content="Ihr privates Praxisportal für Arbeitsschutzvorschriften, Ruhezeiten im Schichtdienst und gesetzliche Sicherheitsunterweisungen.">{clean_style}</head><body><header><h1>Praxis-Kompass Arbeitsschutz</h1><p>Unabhängiges Informations-System v11.5</p></header>{nav_bar}<div class="container"><div class="hero-box"><h2>Willkommen beim Praxis-Kompass</h2><p>Unser unabhängiges System analysiert fortlaufend gesetzliche Rahmenbedingungen und bereitet sie in leicht verständlichen Praxis-Leitfäden für den Alltag auf.</p></div>{get_b2b_monetization_banner("betreiber")}<div class="hero-box" style="border-left-color: #2ecc71; background: #fdfdfd;"><h3>📊 Aktueller Datenbank-Status:</h3><p style="margin-top: 10px;">• <strong>Behörden-Terminal:</strong> {len(data["aemter"])} Segmente.</p><p>• <strong>Betreiber-Kompass:</strong> {len(data["betreiber"])} Unterweisungen.</p><p>• <strong>Anwärter-Akademie:</strong> {len(data["anwaerter"])} Normen.</p></div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>')

    # 2. AEMTER.HTML
    faqs_aemter = "".join([generate_faq_logic(b, "aemter") for b in data["aemter"]])
    with open("aemter.html", "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><title>Behörden-Terminal | Infos für Schichtdienst & Dienststellenleiter</title><meta name="description" content="Praxisnahe Leitfäden für Schichtdienstleiter und Dienststellen zur Umsetzung von Arbeitszeitverordnungen und Ruhezeiten.">{clean_style}</head><body><header style="background: linear-gradient(135deg, #1e3c72, #162a4e);"><h1>🏛️ Behörden- & Ämter-Terminal</h1><p>Rechtssicherheit für Dienststellen und Schichtleiter</p></header>{nav_bar}<div class="container"><div class="hero-box" style="border-left-color: #1e3c72;"><h2>Praxiswissen für den Dienstbetrieb</h2></div>{get_b2b_monetization_banner("aemter")}<h3>📌 Häufige Fragen aus der Verwaltungspraxis</h3><div class="faq-container">{faqs_aemter}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>')

    # 3. BETREIBER.HTML
    faqs_betreiber = "".join([generate_faq_logic(b, "betreiber") for b in data["betreiber"]])
    with open("betreiber.html", "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><title>Betreiber-Kompass | Unabhängiger Leitfaden</title><meta name="description" content="Praxisnahe Umsetzung der gesetzlichen Sicherheitsunterweisung für Betreiber und Studios nach § 12 ArbSchG.">{clean_style}</head><body><header style="background: linear-gradient(135deg, #e67e22, #d35400);"><h1>🏢 Betreiber- & Studio-Kompass</h1><p>Vorschriften verständlich erklärt für die Praxis</p></header>{nav_bar}<div class="container"><div class="hero-box" style="border-left-color: #e67e22;"><h2>Sicher durch die Betriebsprüfung</h2></div>{get_b2b_monetization_banner("betreiber")}<h3>📌 Wichtige Betreiber-Fragen im Überblick</h3><div class="faq-container">{faqs_betreiber}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>')

    # 4. ANWAERTER.HTML
    faqs_anwaerter = "".join([generate_faq_logic(b, "anwaerter") for b in data["anwaerter"]])
    with open("anwaerter.html", "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><title>Anwärter-Akademie | Klausurenstoff & Aufsichtspflicht</title><meta name="description" content="Gutachterliche Prüfungsschemata und Erläuterungen zu Verordnungen und Arbeitsschutzgesetzen für Beamtenanwärter.">{clean_style}</head><body><header style="background: linear-gradient(135deg, #2ecc71, #27ae60);"><h1>🎓 Die Anwärter-Akademie</h1><p>Prüfungserfolg und Didaktik für die Laufbahnprüfung</p></header>{nav_bar}<div class="container"><div class="hero-box" style="border-left-color: #2ecc71;"><h2>Lernstoff für die Laufbahnprüfungen</h2></div>{get_b2b_monetization_banner("anwaerter")}<h3>📌 Klausurrelevante Frage-Muster</h3><div class="faq-container">{faqs_anwaerter}</div></div><footer>&copy; 2026 Core Idle Projekt</footer></body></html>')

    print("[SUCCESS] Branding-Staging v11.5 abgeschlossen!")
    generate_sitemap_xml()
    prepare_deployment_metadata()

if __name__ == "__main__":
    generate_network_with_faqs()