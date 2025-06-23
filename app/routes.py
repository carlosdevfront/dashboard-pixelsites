# app/routes.py
from flask import Blueprint, render_template, request, send_file
from collections import defaultdict
from .db import get_db_connection
import pandas as pd
from io import BytesIO

# ✅ define el blueprint primero
main = Blueprint('main', __name__)  

@main.route('/exportar')
def exportar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ventas")
    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    df = pd.DataFrame(datos)
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name="Ventas")

    output.seek(0)
    return send_file(
        output,
        download_name="reporte_ventas.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@main.route('/', methods=['GET', 'POST'])
def index():
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if fecha_inicio and fecha_fin:
        cursor.execute("""
            SELECT producto, cantidad, precio, fecha
            FROM ventas
            WHERE fecha BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
    else:
        cursor.execute("SELECT producto, cantidad, precio, fecha FROM ventas")

    ventas = cursor.fetchall()
    cursor.close()
    conn.close()

    for venta in ventas:
        venta["total"] = int(venta["cantidad"] or 0) * int(venta["precio"] or 0)

    total_general = sum(venta["total"] for venta in ventas)

    resumen_por_producto = defaultdict(float)
    for venta in ventas:
        resumen_por_producto[venta["producto"]] += float(venta["total"])

    labels = list(resumen_por_producto.keys())
    data = list(resumen_por_producto.values())

    total_registros = len(ventas)
    total_productos_vendidos = sum(venta["cantidad"] for venta in ventas)
    producto_mas_vendido = max(ventas, key=lambda v: v["cantidad"])["producto"] if ventas else "N/A"
    producto_mayores_ingresos = max(ventas, key=lambda v: v["total"])["producto"] if ventas else "N/A"

    return render_template(
        'index.html',
        ventas=ventas,
        total_general=total_general,
        labels=labels,
        data=data,
        total_registros=total_registros,
        total_productos_vendidos=total_productos_vendidos,
        producto_mas_vendido=producto_mas_vendido,
        producto_mayores_ingresos=producto_mayores_ingresos,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
