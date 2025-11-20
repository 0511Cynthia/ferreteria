import os

def get_db_config():
    """Devuelve un diccionario con la configuración de conexión a MySQL desde variables de entorno."""
    return {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', 'contraseña'),
        'database': os.environ.get('MYSQL_DATABASE', 'ferreteria'),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
    }
