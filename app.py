import os
import random
import string
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Dictionnaire pour stocker les URL raccourcies
short_urls = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    try:
        long_url = request.form['long_url']
        # Logique pour raccourcir l'URL (exemple simple : utiliser une clé aléatoire)
        short_url = generate_short_url(long_url)
        short_urls[short_url] = long_url
        return render_template('result.html', short_url=short_url)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    if short_url in short_urls:
        original_url = short_urls[short_url]
        return redirect(original_url)
    else:
        return render_template('error.html', error='URL raccourcie non trouvée')

# Exemple de gestion d'erreur
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page non trouvée'), 404

def generate_short_url(long_url):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

if __name__ == "__main__":
    # Désactiver le mode de débogage
    # Utiliser Gunicorn pour servir l'application Flask
    # Configurer l'hôte et le port pour l'écoute de l'application
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
