#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
French Bar Scrapers Platform - RAILWAY Edition
===============================================
Version cloud-adaptée pour Railway avec scrapers intégrés
"""

import os
import json
import subprocess
import threading
import tempfile
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'french-bar-scrapers-railway-2025'

# Configuration pour Railway (utilise le PORT fourni par l'environnement)
PORT = int(os.environ.get('PORT', 8082))

# Configuration des scrapers - URLs vers vos scrapers GitHub
RAILWAY_SCRAPERS_CONFIG = {
    "agen": {"name": "Agen", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/agen_scraper_production.py"},
    "ain": {"name": "Ain (Bourg-en-Bresse)", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/ain_scraper_production.py"},
    "angers": {"name": "Angers", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/angers_production_scraper.py"},
    "annecy": {"name": "Annecy", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/annecy_scraper_final.py"},
    "argentan": {"name": "Argentan", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/argentan_scraper_production.py"},
    "arras": {"name": "Arras", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/arras_scraper_production.py"},
    "belfort": {"name": "Belfort", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/belfort_scraper_production.py"},
    "bethune": {"name": "Béthune", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/bethune_scraper_final_propre.py"},
    "blois": {"name": "Blois", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/blois_scraper_production.py"},
    "bonneville": {"name": "Bonneville et les Pays du Mont-Blanc", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/bonneville_final_scraper.py"},
    "bordeaux": {"name": "Bordeaux", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/bordeaux_production_final.py"},
    "boulogne": {"name": "Boulogne-sur-Mer", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/boulogne_scraper_production.py"},
    "bourges": {"name": "Bourges", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/bourges_scraper_FINAL_COMPLETE.py"},
    "bourgoin": {"name": "Bourgoin-Jallieu", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/bourgoin_scraper_production.py"},
    "brest": {"name": "Brest", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/brest_scraper_final.py"},
    "caen": {"name": "Caen", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/scraper_caen_corrected.py"},
    "cambrai": {"name": "Cambrai", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/cambrai_scraper_production.py"},
    "carpentras": {"name": "Carpentras", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/carpentras_scraper_production.py"},
    "castres": {"name": "Castres", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/castres_scraper_final.py"},
    "chalon": {"name": "Chalon-sur-Saône", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/chalon_scraper_production.py"},
    "charente": {"name": "Charente", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/charente_scraper_production.py"},
    "creuse": {"name": "Creuse", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/creuse_scraper_production.py"},
    "dunkerque": {"name": "Dunkerque", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/dunkerque_complete_final_scraper.py"},
    "essonne": {"name": "Essonne", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/essonne_scraper_final.py"},
    "fontainebleau": {"name": "Fontainebleau", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/fontainebleau_scraper_production.py"},
    "martinique": {"name": "Fort-de-France (Martinique)", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/martinique_scraper_final.py"},
    "grasse": {"name": "Grasse", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/grasse_scraper_production.py"},
    "laval": {"name": "Laval", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/laval_scraper_production.py"},
    "havre": {"name": "Le Havre", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/havre_scraper_final.py"},
    "sables": {"name": "Les Sables-d'Olonne", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/sables_olonne_scraper_final_corrected.py"},
    "libourne": {"name": "Libourne", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/libourne_scraper_final_definitif.py"},
    "lille": {"name": "Lille", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/lille_scraper_final.py"},
    "limoges": {"name": "Limoges", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/limoges_scraper_production.py"},
    "lisieux": {"name": "Lisieux", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/lisieux_scraper_final.py"},
    "lorient": {"name": "Lorient", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/lorient_scraper_final_consolidated.py"},
    "lozere": {"name": "Lozère", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/lozere_scraper_final.py"},
    "lyon": {"name": "Lyon", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/lyon_scraper_final.py"},
    "macon": {"name": "Mâcon", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/macon_scraper_final_with_specialties.py"},
    "mayotte": {"name": "Mayotte", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/mayotte_scraper_final.py"},
    "melun": {"name": "Melun", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/melun_scraper_fixed_complete.py"},
    "meuse": {"name": "Meuse", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/meuse_scraper_final.py"},
    "montdemarsan": {"name": "Mont-de-Marsan", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/montdemarsan_scraper_production.py"},
    "montlucon": {"name": "Montluçon", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/montlucon_final_scraper.py"},
    "nancy": {"name": "Nancy", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/nancy_scraper_273_FINAL.py"},
    "nantes": {"name": "Nantes", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/nantes_scraper_final.py"},
    "nevers": {"name": "Nevers", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/nevers_scraper_complet.py"},
    "papeete": {"name": "Papeete - Tahiti (Nouvelle-Calédonie)", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/papeete_scraper_production.py"},
    "pau": {"name": "Pau", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/pau_scraper_production_fixed.py"},
    "perigueux": {"name": "Périgueux", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/perigueux_scraper_final_avec_serment.py"},
    "rennes": {"name": "Rennes", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/rennes_scraper_production_fixed.py"},
    "rouen": {"name": "Rouen", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/rouen_scraper_production.py"},
    "saintdenis": {"name": "Saint-Denis de la Réunion", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/saint_denis_scraper_final.py"},
    "saintnazaire": {"name": "Saint-Nazaire", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/saintnazaire_production_scraper.py"},
    "saintpierre": {"name": "Saint-Pierre de la Réunion", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/saint_pierre_reunion_scraper_final.py"},
    "saintquentin": {"name": "Saint-Quentin", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/saint_quentin_scraper_complet.py"},
    "saintes": {"name": "Saintes", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/saintes_complete_scraper.py"},
    "sarreguemines": {"name": "Sarreguemines", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/sarreguemines_final_scraper.py"},
    "saverne": {"name": "Saverne", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/saverne_scraper_final.py"},
    "senlis": {"name": "Senlis", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/senlis_complete_scraper.py"},
    "tarbes": {"name": "Tarbes", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/tarbes_scraper_final.py"},
    "thionville": {"name": "Thionville", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/thionville_scraper_final_correct.py"},
    "thonon": {"name": "Thonon-les-Bains, Léman et Genevois", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/thonon_scraper_final.py"},
    "valdemarne": {"name": "Val-de-Marne", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/valdemarne_scraper_final.py"},
    "valenciennes": {"name": "Valenciennes", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/valenciennes_scraper_production.py"},
    "vannes": {"name": "Vannes", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/vannes_scraper_final.py"},
    "vienne": {"name": "Vienne", "github_url": "https://raw.githubusercontent.com/paularnd875/french-bar-scrapers/main/vienne_scraper_production_final.py"}
}

# Global variables for tracking running processes
running_processes = {}
scraping_stats = {"total": 0, "completed": 0, "failed": 0}

def download_scraper(github_url, scraper_id):
    """Télécharge un scraper depuis GitHub."""
    try:
        response = requests.get(github_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Erreur téléchargement {scraper_id}: {str(e)}")
        return None

def execute_scraper_cloud(scraper_id, scraper_config):
    """Execute un scraper en mode cloud."""
    global running_processes, scraping_stats
    
    try:
        print(f"☁️ Démarrage cloud scraper: {scraper_config['name']}")
        
        # Télécharger le code du scraper
        scraper_code = download_scraper(scraper_config["github_url"], scraper_id)
        if not scraper_code:
            raise Exception("Impossible de télécharger le scraper")
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(scraper_code)
            temp_script_path = temp_file.name
        
        # Exécuter le scraper
        process = subprocess.Popen(
            ["python3", temp_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        running_processes[scraper_id] = process
        
        # Monitor process output
        stdout, stderr = process.communicate()
        
        # Nettoyer le fichier temporaire
        os.unlink(temp_script_path)
        
        # Check process result
        if process.returncode == 0:
            scraping_stats["completed"] += 1
            print(f"✅ Terminé: {scraper_config['name']}")
        else:
            scraping_stats["failed"] += 1
            print(f"❌ Échec: {scraper_config['name']} - {stderr[:200]}")
            
    except Exception as e:
        scraping_stats["failed"] += 1
        print(f"💥 Erreur: {scraper_config['name']} - {str(e)}")
    
    finally:
        if scraper_id in running_processes:
            del running_processes[scraper_id]

@app.route('/')
def index():
    """Main dashboard."""
    return render_template('railway_index.html', scrapers=RAILWAY_SCRAPERS_CONFIG)

@app.route('/api/scrape/<scraper_id>', methods=['POST'])
def scrape_single(scraper_id):
    """Start scraping for a single barreau."""
    if scraper_id not in RAILWAY_SCRAPERS_CONFIG:
        return jsonify({'error': 'Scraper not found'}), 404
    
    if scraper_id in running_processes:
        return jsonify({'error': 'Scraper already running'}), 400
    
    scraper_config = RAILWAY_SCRAPERS_CONFIG[scraper_id]
    
    # Start scraper in background thread
    thread = threading.Thread(
        target=execute_scraper_cloud,
        args=(scraper_id, scraper_config)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Started scraping ' + scraper_config["name"]}), 200

@app.route('/api/scrape/all', methods=['POST'])
def scrape_all():
    """Start scraping all barreaux."""
    global scraping_stats
    scraping_stats = {"total": len(RAILWAY_SCRAPERS_CONFIG), "completed": 0, "failed": 0}
    
    # Start all scrapers in parallel
    for scraper_id, scraper_config in RAILWAY_SCRAPERS_CONFIG.items():
        if scraper_id not in running_processes:
            thread = threading.Thread(
                target=execute_scraper_cloud,
                args=(scraper_id, scraper_config)
            )
            thread.daemon = True
            thread.start()
    
    return jsonify({'message': 'Started scraping all ' + str(len(RAILWAY_SCRAPERS_CONFIG)) + ' official barreaux'}), 200

@app.route('/api/status')
def get_status():
    """Get current scraping status."""
    return jsonify({
        'running': list(running_processes.keys()),
        'stats': scraping_stats
    })

if __name__ == '__main__':
    print("🚂 French Bar Scrapers Platform - RAILWAY Edition starting...")
    print(f"☁️ Managing {len(RAILWAY_SCRAPERS_CONFIG)} barreaux in the cloud")
    print("✅ Scrapers downloaded from GitHub on-demand")
    print(f"🌐 Railway deployment ready on port {PORT}")
    
    app.run(debug=False, host='0.0.0.0', port=PORT)