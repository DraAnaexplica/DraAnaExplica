import sqlite3

def init_db():
    conn = sqlite3.connect("consultas.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            numero TEXT PRIMARY KEY,
            plano INT,
            perguntas_restantes INT,
            treplicas_restantes INT
        )
    """)
    conn.close()
