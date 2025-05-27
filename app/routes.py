# app/routes.py
from flask import Blueprint, render_template
from app.services.ventas_service import obtener_ventas, calcular_totales

main = Blueprint('main', __name__)

@main.route('/')
def index():
    ventas = obtener_ventas()
    ventas, total_general = calcular_totales(ventas)
    return render_template('index.html', ventas=ventas, total_general=total_general)

