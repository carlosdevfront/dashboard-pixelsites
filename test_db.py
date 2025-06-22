import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Déjalo vacío si no tienes clave
        database='dashboard_ventas',
        port=3307     # Cámbialo a 3306 si ese es el puerto correcto
    )

    if connection.is_connected():
        print("✅ ¡Conexión exitosa!")
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        for table in cursor.fetchall():
            print("📦 Tabla encontrada:", table)

except mysql.connector.Error as err:
    print("❌ Error de conexión:", err)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
