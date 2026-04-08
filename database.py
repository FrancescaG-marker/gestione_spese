import sqlite3

def inizializza_database():
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spese (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        descrizione TEXT,
        importo REAL NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mese TEXT NOT NULL,
        categoria_id INTEGER,
        importo REAL NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
    )
    """)

    conn.commit()
    conn.close()


def aggiungi_categoria(nome):
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    nome = nome.strip()

    if nome == "":
        conn.close()
        return "Il nome della categoria non può essere vuoto."

    cursor.execute("SELECT * FROM categorie WHERE nome = ?", (nome,))
    if cursor.fetchone():
        conn.close()
        return "La categoria esiste già."

    cursor.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

    return "Categoria inserita correttamente."


def aggiungi_spesa(data, importo, nome_categoria, descrizione):
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    if importo <= 0:
        conn.close()
        return "Errore: l'importo deve essere maggiore di zero."

    nome_categoria = nome_categoria.strip()

    cursor.execute("SELECT id FROM categorie WHERE nome = ?", (nome_categoria,))
    categoria = cursor.fetchone()

    if not categoria:
        conn.close()
        return "Errore: la categoria non esiste."

    categoria_id = categoria[0]

    cursor.execute("""
    INSERT INTO spese (data, descrizione, importo, categoria_id)
    VALUES (?, ?, ?, ?)
    """, (data, descrizione, importo, categoria_id))

    conn.commit()
    conn.close()

    return "Spesa inserita correttamente."


def salva_budget(mese, nome_categoria, importo_budget):
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    if importo_budget <= 0:
        conn.close()
        return "Errore: il budget deve essere maggiore di zero."

    nome_categoria = nome_categoria.strip()

    cursor.execute("SELECT id FROM categorie WHERE nome = ?", (nome_categoria,))
    categoria = cursor.fetchone()

    if not categoria:
        conn.close()
        return "Errore: la categoria non esiste."

    categoria_id = categoria[0]

    cursor.execute("""
    SELECT id FROM budget
    WHERE mese = ? AND categoria_id = ?
    """, (mese, categoria_id))

    if cursor.fetchone():
        cursor.execute("""
        UPDATE budget
        SET importo = ?
        WHERE mese = ? AND categoria_id = ?
        """, (importo_budget, mese, categoria_id))
    else:
        cursor.execute("""
        INSERT INTO budget (mese, categoria_id, importo)
        VALUES (?, ?, ?)
        """, (mese, categoria_id, importo_budget))

    conn.commit()
    conn.close()

    return "Budget mensile salvato correttamente."


def report_totale_per_categoria():
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.nome, IFNULL(SUM(s.importo), 0)
    FROM categorie c
    LEFT JOIN spese s ON c.id = s.categoria_id
    GROUP BY c.id, c.nome
    ORDER BY c.nome
    """)

    risultati = cursor.fetchall()
    conn.close()

    return risultati


def report_spese_vs_budget(mese):
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        c.nome,
        IFNULL(b.importo, 0),
        IFNULL(SUM(s.importo), 0)
    FROM categorie c
    LEFT JOIN budget b
        ON c.id = b.categoria_id AND b.mese = ?
    LEFT JOIN spese s
        ON c.id = s.categoria_id AND substr(s.data, 1, 7) = ?
    GROUP BY c.id, c.nome, b.importo
    ORDER BY c.nome
    """, (mese, mese))

    risultati = cursor.fetchall()
    conn.close()

    return risultati


def report_elenco_spese():
    conn = sqlite3.connect("spese.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT s.data, c.nome, s.importo, s.descrizione
    FROM spese s
    JOIN categorie c ON s.categoria_id = c.id
    ORDER BY s.data
    """)

    risultati = cursor.fetchall()
    conn.close()

    return risultati