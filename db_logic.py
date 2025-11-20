import mysql.connector
from mysql.connector import Error
from db_config import get_db_config

def validate_user(username, password):
    """Valida si el usuario y contraseña existen en la tabla Login."""
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM usuarios WHERE user=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result[0] > 0
    except Error as e:
        print(f"Error en validate_user: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def add_product_to_cart(id_producto, cantidad, id_carrito):
    """Agrega un producto al carrito (tabla Carrito). Si ya existe, suma la cantidad."""
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()
        # Verificar si ya existe ese producto en el carrito
        query_check = "SELECT cantidad FROM carrito WHERE id_producto=%s AND id_carrito=%s"
        cursor.execute(query_check, (id_producto, id_carrito))
        row = cursor.fetchone()
        if row:
            # Actualizar cantidad
            nueva_cantidad = row[0] + cantidad
            query_update = "UPDATE carrito SET cantidad=%s WHERE id_producto=%s AND id_carrito=%s"
            cursor.execute(query_update, (nueva_cantidad, id_producto, id_carrito))
        else:
            # Insertar nuevo
            query_insert = "INSERT INTO carrito (id_producto, cantidad, id_carrito) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (id_producto, cantidad, id_carrito))
        conn.commit()
        return True
    except Error as e:
        print(f"Error en add_product_to_cart: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def remove_from_cart(id_producto, id_carrito):
    """Elimina un producto del carrito (tabla Carrito) por id_producto e id_carrito."""
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()
        query = "DELETE FROM carrito WHERE id_producto=%s AND id_carrito=%s"
        cursor.execute(query, (id_producto, id_carrito))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error en remove_from_cart: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
