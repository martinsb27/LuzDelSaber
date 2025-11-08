# utils/helpers.py
"""
Funciones auxiliares: validación básica, formateo para consola, etc.
"""

from typing import Any
from tabulate import tabulate

def format_table(rows: list, headers: list):
    """
    Usa tabulate para imprimir listas de diccionarios o listas de tuplas.
    """
    if not rows:
        return "No hay resultados."
    return tabulate(rows, headers=headers, tablefmt="grid", showindex=False)

def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default

def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default
