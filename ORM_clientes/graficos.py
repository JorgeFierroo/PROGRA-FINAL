import matplotlib.pyplot as plt
from sqlalchemy import func
from database import get_session
from models import Pedido, Menu, Ingrediente
from datetime import datetime, timedelta

def graficar_ventas_por_fecha():
    """Genera un gráfico de barras para las ventas agrupadas por fecha."""
    db = next(get_session())
    try:
        # Consultar datos de ventas agrupados por fecha (últimos 30 días)
        rango_inicio = datetime.now() - timedelta(days=1)
        resultados = db.query(
            Pedido.fecha_creacion,
            func.sum(Pedido.total).label("total_vendido")
        ).filter(Pedido.fecha_creacion >= rango_inicio).group_by(Pedido.fecha_creacion).order_by(Pedido.fecha_creacion).all()

        # Validar si hay datos
        if not resultados:
            print("No hay datos de ventas disponibles para el rango seleccionado.")
            return

        # Procesar resultados
        fechas = [pedido[0].strftime('%Y-%m-%d') for pedido in resultados]
        totales = [pedido[1] for pedido in resultados]

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(fechas, totales, color='blue')
        plt.title("Ventas por Fecha (Últimos 30 días)")
        plt.xlabel("Fecha")
        plt.ylabel("Total Vendido")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    finally:
        db.close()

def graficar_menus_mas_comprados():
    """Genera un gráfico de torta para los menús más vendidos."""
    db = next(get_session())
    try:
        # Consultar los menús más vendidos, sumando la cantidad de menús comprados
        resultados = db.query(
            Menu.nombre,
            func.sum(Pedido.cantidad_menus).label("cantidad_vendida")
        ).join(Pedido, Pedido.descripcion == Menu.nombre).group_by(Menu.nombre).order_by(func.sum(Pedido.cantidad_menus).desc()).all()

        # Validar si hay datos
        if not resultados:
            print("No hay datos disponibles para los menús más vendidos.")
            return

        # Extraer nombres y cantidades
        menus = [resultado[0] for resultado in resultados]
        cantidades = [resultado[1] for resultado in resultados]

        # Crear el gráfico
        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=menus, autopct='%1.1f%%', startangle=140)
        plt.title("Distribución de Menús Más Comprados")
        plt.show()
    finally:
        db.close()

def graficar_uso_ingredientes():
    """Genera un gráfico de barras para los ingredientes utilizados."""
    db = next(get_session())
    try:
        # Consultar datos de uso de ingredientes
        resultados = db.query(Ingrediente.nombre, Ingrediente.cantidad).all()
        ingredientes = [resultado[0] for resultado in resultados]
        cantidades = [resultado[1] for resultado in resultados]

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(ingredientes, cantidades, color='green')
        plt.title("Uso de Ingredientes en Pedidos")
        plt.xlabel("Ingrediente")
        plt.ylabel("Cantidad Utilizada")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    finally:
        db.close()