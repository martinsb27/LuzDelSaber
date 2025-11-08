# models/sale.py
"""
SaleRepository: registra ventas y actualiza stock de forma transaccional.
Verifica disponibilidad de stock antes de insertar.
"""

from database.connection import get_connection
from typing import Optional, List, Dict

class SaleRepository:
    @staticmethod
    def register_sale(isbn: str, cantidad: int) -> int:
        """
        Registra una venta: busca libro por ISBN, valida stock, actualiza stock e inserta en ventas.
        Retorna id de la venta insertada.
        Lanza excepciones en caso de error.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()

            # Obtener libro
            cur.execute("SELECT id, stock, precio FROM libros WHERE isbn = ?", (isbn,))
            row = cur.fetchone()
            if not row:
                raise ValueError("Libro no encontrado con ese ISBN.")
            libro_id, stock_actual, precio_unitario = row

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            if stock_actual < cantidad:
                raise ValueError(f"Stock insuficiente. Disponible: {stock_actual}")

            total = round(precio_unitario * cantidad, 2)

            # Actualizar stock
            new_stock = stock_actual - cantidad
            cur.execute("UPDATE libros SET stock = ? WHERE id = ?", (new_stock, libro_id))

            # Insertar venta
            cur.execute(
                """
                INSERT INTO ventas (libro_id, cantidad, precio_unitario, total)
                VALUES (?, ?, ?, ?);
                SELECT SCOPE_IDENTITY();
                """,
                (libro_id, cantidad, float(precio_unitario), total)
            )
            venta_id = cur.fetchval()
            conn.commit()
            return int(venta_id)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def get_sales_by_date_range(start_date: str, end_date: str) -> List[Dict]:
        """
        start_date and end_date as 'YYYY-MM-DD' (inclusive)
        """
        sql = """
        SELECT v.id, v.libro_id, b.titulo, v.cantidad, v.precio_unitario, v.total, v.fecha
        FROM ventas v
        JOIN libros b ON v.libro_id = b.id
        WHERE CAST(v.fecha AS DATE) BETWEEN ? AND ?
        ORDER BY v.fecha
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
