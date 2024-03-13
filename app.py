import os
import random
import string
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Dictionnaire pour stocker les URL raccourcies et les statistiques
short_urls = {}
url_clicks = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    try:
        long_url = request.form['long_url']
        custom_alias = request.form.get('custom_alias')
        # Validation de l'URL
        if not long_url.startswith(('http://', 'https://')):
            raise ValueError('URL invalide. Assurez-vous d\'inclure http:// ou https://')
        # Vérification de l'alias personnalisé
        if custom_alias:
            if custom_alias in short_urls:
                raise ValueError('Cet alias personnalisé est déjà utilisé')
            short_url = custom_alias
        else:
            # Logique pour raccourcir l'URL
            short_url = generate_short_url()
        short_urls[short_url] = long_url
        url_clicks.setdefault(short_url, 0)
        return render_template('result.html', short_url=short_url)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    if short_url in short_urls:
        original_url = short_urls[short_url]
        # Incrémenter le compteur de clics
        url_clicks[short_url] += 1
        return redirect(original_url)
    else:
        return render_template('error.html', error='URL raccourcie non trouvée')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page non trouvée'), 404

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
