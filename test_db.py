import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  
        database='dashboard_ventas',
        port=3307     
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
