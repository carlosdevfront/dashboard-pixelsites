# app/routes.py
from flask import Blueprint, render_template, request
from app.db import get_db_connection
from collections import defaultdict

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if fecha_inicio and fecha_fin:
        cursor.execute("""
            SELECT * FROM ventas
            WHERE fecha BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
    else:
        cursor.execute("SELECT * FROM ventas")

    ventas = cursor.fetchall()
    cursor.close()
    conn.close()

    for venta in ventas:
        venta['total'] = venta['cantidad'] * float(venta['precio'])

    total_general = sum(venta['total'] for venta in ventas)

    resumen_por_producto = defaultdict(float)
    for venta in ventas:
        resumen_por_producto[venta['producto']] += venta['total']

    labels = list(resumen_por_producto.keys())
    data = list(resumen_por_producto.values())

    return render_template(
        'index.html',
        ventas=ventas,
        total_general=total_general,
        labels=labels,
        data=data,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
