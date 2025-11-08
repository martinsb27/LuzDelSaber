# main.py
"""
Interfaz de consola principal para Luz del Saber.
Menú simple que usa los repositorios y reportes.
"""

import sys
from models.book import BookRepository
from models.sale import SaleRepository
from reports.reports import top_selling_books, income_by_day, low_stock_books
from utils.helpers import format_table, parse_int, parse_float
from tabulate import tabulate

def menu_libros():
    while True:
        print("\n--- Gestionar libros ---")
        print("1. Agregar libro")
        print("2. Editar libro por ISBN")
        print("3. Eliminar libro por ISBN")
        print("4. Buscar libros")
        print("5. Listar libros con stock bajo")
        print("0. Volver")
        opt = input("> ").strip()
        if opt == "1":
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            isbn = input("ISBN: ").strip()
            categoria = input("Categoría: ").strip() or None
            stock = parse_int(input("Stock inicial: ").strip(), 0)
            precio = parse_float(input("Precio: ").strip(), 0.0)
            try:
                new_id = BookRepository.add_book(titulo, autor, isbn, categoria, stock, precio)
                print(f"Libro agregado con id {new_id}")
            except Exception as e:
                print("Error al agregar libro:", e)
        elif opt == "2":
            isbn = input("ISBN del libro a editar: ").strip()
            book = BookRepository.get_by_isbn(isbn)
            if not book:
                print("Libro no encontrado.")
                continue
            print("Dejar vacío para no cambiar campo.")
            titulo = input(f"Título [{book['titulo']}]: ").strip()
            autor = input(f"Autor [{book['autor']}]: ").strip()
            categoria = input(f"Categoría [{book.get('categoria')}]: ").strip()
            stock_text = input(f"Stock [{book['stock']}]: ").strip()
            precio_text = input(f"Precio [{book['precio']}]: ").strip()
            fields = {}
            if titulo: fields['titulo'] = titulo
            if autor: fields['autor'] = autor
            if categoria: fields['categoria'] = categoria
            if stock_text != "": fields['stock'] = parse_int(stock_text, book['stock'])
            if precio_text != "": fields['precio'] = parse_float(precio_text, book['precio'])
            try:
                ok = BookRepository.update_book_by_isbn(isbn, fields)
                print("Actualizado." if ok else "No se realizaron cambios.")
            except Exception as e:
                print("Error al actualizar:", e)
        elif opt == "3":
            isbn = input("ISBN a eliminar: ").strip()
            confirm = input("¿Seguro? (s/n): ").lower()
            if confirm != "s":
                continue
            try:
                ok = BookRepository.delete_by_isbn(isbn)
                print("Eliminado." if ok else "No se encontró el libro.")
            except Exception as e:
                print("Error al eliminar:", e)
        elif opt == "4":
            term = input("Término de búsqueda (título/autor/ISBN/categoría): ").strip()
            try:
                rows = BookRepository.search(term)
                if not rows:
                    print("No hay resultados.")
                else:
                    headers = list(rows[0].keys())
                    print(format_table([list(r.values()) for r in rows], headers))
            except Exception as e:
                print("Error en búsqueda:", e)
        elif opt == "5":
            threshold = parse_int(input("Umbral stock (por defecto 5): ").strip() or 5, 5)
            try:
                rows = BookRepository.list_low_stock(threshold)
                if not rows:
                    print("No hay libros con stock bajo.")
                else:
                    headers = list(rows[0].keys())
                    print(format_table([list(r.values()) for r in rows], headers))
            except Exception as e:
                print("Error al listar stock bajo:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida.")

def menu_ventas():
    while True:
        print("\n--- Registrar venta ---")
        print("1. Registrar venta por ISBN")
        print("2. Ver ventas por rango de fechas")
        print("0. Volver")
        opt = input("> ").strip()
        if opt == "1":
            isbn = input("ISBN: ").strip()
            cantidad = parse_int(input("Cantidad: ").strip(), 0)
            try:
                venta_id = SaleRepository.register_sale(isbn, cantidad)
                print(f"Venta registrada con id {venta_id}")
            except Exception as e:
                print("Error al registrar venta:", e)
        elif opt == "2":
            inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
            fin = input("Fecha fin (YYYY-MM-DD): ").strip()
            try:
                rows = SaleRepository.get_sales_by_date_range(inicio, fin)
                if not rows:
                    print("No hay ventas en ese rango.")
                else:
                    headers = list(rows[0].keys())
                    print(format_table([list(r.values()) for r in rows], headers))
            except Exception as e:
                print("Error al consultar ventas:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida.")

def menu_reportes():
    while True:
        print("\n--- Reportes ---")
        print("1. Libros más vendidos")
        print("2. Ingresos por día (rango)")
        print("3. Libros con stock bajo")
        print("0. Volver")
        opt = input("> ").strip()
        if opt == "1":
            try:
                limit = int(input("Cuántos (por defecto 10): ").strip() or 10)
            except:
                limit = 10
            try:
                rows = top_selling_books(limit)
                if not rows:
                    print("No hay datos de ventas.")
                else:
                    headers = list(rows[0].keys())
                    print(format_table([list(r.values()) for r in rows], headers))
            except Exception as e:
                print("Error al generar reporte:", e)
        elif opt == "2":
            inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
            fin = input("Fecha fin (YYYY-MM-DD): ").strip()
            try:
                rows = income_by_day(inicio, fin)
                if not rows:
                    print("No hay ingresos en ese rango.")
                else:
                    headers = list(rows[0].keys())
                    print(format_table([list(r.values()) for r in rows], headers))
            except Exception as e:
                print("Error al generar reporte:", e)
        elif opt == "3":
            threshold = parse_int(input("Umbral stock (por defecto 5): ").strip() or 5, 5)
            try:
                rows = low_stock_books(threshold)
                if not rows:
                    print("No hay libros con stock bajo.")
                else:
                    headers = list(rows[0].keys())
                    print(format_table([list(r.values()) for r in rows], headers))
            except Exception as e:
                print("Error al generar reporte:", e)
        elif opt == "0":
            break
        else:
            print("Opción inválida.")

def main():
    print("=== Luz del Saber — Gestión de Inventario ===")
    while True:
        print("\nMenú principal:")
        print("1. Gestionar libros")
        print("2. Registrar venta")
        print("3. Reportes")
        print("0. Salir")
        opt = input("> ").strip()
        if opt == "1":
            menu_libros()
        elif opt == "2":
            menu_ventas()
        elif opt == "3":
            menu_reportes()
        elif opt == "0":
            print("Saliendo. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
