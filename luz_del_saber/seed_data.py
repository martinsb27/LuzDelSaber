# seed_data.py
"""
Inserta datos de ejemplo para pruebas rápidas.
Úsalo solo en entornos de desarrollo.
"""

from models.book import BookRepository
from database.connection import get_connection

sample_books = [
    ("Matemáticas para todos", "Ana Perez", "978-0001", "Matemáticas", 12, 25.50),
    ("Física esencial", "Carlos Ruiz", "978-0002", "Ciencias", 8, 30.00),
    ("Gramática española", "María López", "978-0003", "Lengua", 5, 18.75),
    ("Programación en Python", "Luis Gómez", "978-0004", "Programación", 10, 42.00),
    ("Historia universal", "Rosa Díaz", "978-0005", "Historia", 3, 22.00),
]

def seed():
    conn = get_connection()
    try:
        cur = conn.cursor()
        for titulo, autor, isbn, categoria, stock, precio in sample_books:
            # Comprobar existencia por ISBN para no duplicar
            cur.execute("SELECT COUNT(1) FROM libros WHERE isbn = ?", (isbn,))
            if cur.fetchval() == 0:
                cur.execute(
                    "INSERT INTO libros (titulo, autor, isbn, categoria, stock, precio) VALUES (?, ?, ?, ?, ?, ?)",
                    (titulo, autor, isbn, categoria, stock, precio)
                )
        conn.commit()
        print("Datos semilla insertados (o ya existían).")
    except Exception as e:
        conn.rollback()
        print("Error al insertar datos de prueba:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
