# reports/reports.py
"""
Funciones para generar reportes:
- top_selling_books
- income_by_period (day/month)
- low_stock_books
"""

from database.connection import get_connection
from typing import List, Dict

def top_selling_books(limit: int = 10) -> List[Dict]:
    sql = """
    SELECT TOP (?) b.id, b.titulo, b.autor, b.isbn, SUM(v.cantidad) AS total_vendido
    FROM ventas v
    JOIN libros b ON v.libro_id = b.id
    GROUP BY b.id, b.titulo, b.autor, b.isbn
    ORDER BY total_vendido DESC
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, (limit,))
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()

def income_by_day(start_date: str, end_date: str) -> List[Dict]:
    """
    Retorna total de ingresos por día en el rango.
    start_date y end_date en formato 'YYYY-MM-DD'
    """
    sql = """
    SELECT CAST(fecha AS DATE) AS dia, SUM(total) AS ingresos
    FROM ventas
    WHERE CAST(fecha AS DATE) BETWEEN ? AND ?
    GROUP BY CAST(fecha AS DATE)
    ORDER BY dia
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, (start_date, end_date))
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()

def low_stock_books(threshold: int = 5) -> List[Dict]:
    sql = """
    SELECT id, titulo, autor, isbn, stock, precio
    FROM libros
    WHERE stock <= ?
    ORDER BY stock ASC
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, (threshold,))
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()
