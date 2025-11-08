# models/book.py
"""
BookRepository: funciones CRUD para la tabla libros.
Usa consultas parametrizadas para evitar inyección SQL.
"""

from database.connection import get_connection
from typing import List, Dict, Optional

class BookRepository:
    @staticmethod
    def add_book(titulo: str, autor: str, isbn: str, categoria: Optional[str], stock: int, precio: float) -> int:
        sql = """
        INSERT INTO libros (titulo, autor, isbn, categoria, stock, precio)
        VALUES (?, ?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (titulo, autor, isbn, categoria, stock, precio))
            # Obtener ID insertado (SCOPE_IDENTITY devuelve decimal, convertir a int)
            new_id = cur.fetchval()
            conn.commit()
            return int(new_id)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update_book_by_isbn(isbn: str, fields: Dict) -> bool:
        """
        fields: diccionario con columnas a actualizar y sus valores.
        Ej: {"titulo": "Nuevo", "precio": 45.0}
        """
        if not fields:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        sql = f"UPDATE libros SET {set_clause} WHERE isbn = ?"
        params = list(fields.values()) + [isbn]

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            affected = cur.rowcount
            conn.commit()
            return affected > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def delete_by_isbn(isbn: str) -> bool:
        sql = "DELETE FROM libros WHERE isbn = ?"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (isbn,))
            affected = cur.rowcount
            conn.commit()
            return affected > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def get_by_isbn(isbn: str) -> Optional[Dict]:
        sql = "SELECT id, titulo, autor, isbn, categoria, stock, precio, creado_en FROM libros WHERE isbn = ?"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (isbn,))
            row = cur.fetchone()
            if row:
                return dict(zip([c[0] for c in cur.description], row))
            return None
        finally:
            conn.close()

    @staticmethod
    def search(term: str) -> List[Dict]:
        """
        Busca por título, autor, ISBN o categoría (LIKE %term%).
        """
        like = f"%{term}%"
        sql = """
        SELECT id, titulo, autor, isbn, categoria, stock, precio, creado_en
        FROM libros
        WHERE titulo LIKE ? OR autor LIKE ? OR isbn LIKE ? OR categoria LIKE ?
        ORDER BY titulo
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (like, like, like, like))
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def list_low_stock(threshold: int = 5) -> List[Dict]:
        sql = "SELECT id, titulo, autor, isbn, categoria, stock, precio FROM libros WHERE stock <= ? ORDER BY stock ASC"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (threshold,))
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]
        finally:
            conn.close()
