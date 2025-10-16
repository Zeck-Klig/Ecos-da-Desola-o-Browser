from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Cria o banco e insere dados iniciais
def init_db():
    conn = sqlite3.connect('ecos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            content TEXT,
            keywords TEXT,
            secret_keywords TEXT,
            url TEXT
        )
    ''')
    c.execute("SELECT COUNT(*) FROM sites")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO sites (title, description, content, keywords, secret_keywords, url) VALUES (?, ?, ?, ?, ?, ?)",
                  ("Mapa Interativo", "Explore a Cidade Desolada.", "Mapa com marcadores.", "mapa,cidade", "", "paginas/mapa.html"))
        c.execute("INSERT INTO sites (title, description, content, keywords, secret_keywords, url) VALUES (?, ?, ?, ?, ?, ?)",
                  ("Diário do Errante", "Segredos da Floresta.", "Textos ocultos.", "diario,floresta", "sussurro", "paginas/diario.html"))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

@app.route('/indice')
def indice():
    return render_template('indice.html')

@app.route('/buscar')
def buscar():
    q = request.args.get('q', '').lower()
    conn = sqlite3.connect('ecos.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM sites WHERE lower(title) LIKE ? OR lower(keywords) LIKE ? OR lower(description) LIKE ?", (f'%{q}%', f'%{q}%', f'%{q}%'))
    results = c.fetchall()
    c.execute("SELECT * FROM sites WHERE secret_keywords LIKE ?", (f'%{q}%',))
    secrets = c.fetchall()
    conn.close()
    all_results = [dict(r) for r in results + secrets]
    return jsonify(all_results)

@app.route('/sites')
def todos_os_sites():
    conn = sqlite3.connect('ecos.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM sites")
    sites = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(sites)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
