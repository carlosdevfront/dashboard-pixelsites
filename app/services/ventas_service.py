# app/services/ventas_service.py

def obtener_ventas():
    # Aquí irán los datos de prueba o conexión futura a base de datos
    return [
        {'producto': 'Camiseta', 'cantidad': 3, 'precio': 20.0},
        {'producto': 'Pantalón', 'cantidad': 2, 'precio': 35.0},
        {'producto': 'Zapatos', 'cantidad': 1, 'precio': 50.0}
    ]


def calcular_totales(ventas):
    for venta in ventas:
        venta['total'] = venta['cantidad'] * venta['precio']
    
    total_general = sum(v['total'] for v in ventas)
    return ventas, total_general
