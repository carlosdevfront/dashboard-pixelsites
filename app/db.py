import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  
        database='dashboard_ventas',
        port=3306
    )
    return connection




