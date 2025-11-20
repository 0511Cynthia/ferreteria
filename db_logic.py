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
        # Asegurar que exista el carrito referenciado por id_carrito.
        # Si no existe, crear un nuevo carrito con id_usuario por defecto 1
        # y usar su id generado.
        cursor.execute("SELECT id_carrito FROM carritos WHERE id_carrito=%s", (id_carrito,))
        carrito_row = cursor.fetchone()
        if not carrito_row:
            cursor.execute("INSERT INTO carritos (id_usuario) VALUES (%s)", (1,))
            conn.commit()
            id_carrito = cursor.lastrowid
        # Verificar si ya existe ese producto en la nueva tabla carrito_items
        query_check = "SELECT cantidad, id_item FROM carrito_items WHERE id_producto=%s AND id_carrito=%s"
        cursor.execute(query_check, (id_producto, id_carrito))
        row = cursor.fetchone()
        if row:
            # Actualizar cantidad
            nueva_cantidad = row[0] + cantidad
            query_update = "UPDATE carrito_items SET cantidad=%s WHERE id_item=%s"
            cursor.execute(query_update, (nueva_cantidad, row[1]))
        else:
            # Insertar nuevo en carrito_items
            query_insert = "INSERT INTO carrito_items (id_carrito, id_producto, cantidad) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (id_carrito, id_producto, cantidad))
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

def remove_from_cart(id_item):
    """Elimina un item del carrito en la tabla `carrito_items` por su `id_item`.

    Parámetro:
    - id_item: primary key (INT) de la tabla `carrito_items`.
    """
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()
        query = "DELETE FROM carrito_items WHERE id_item=%s"
        cursor.execute(query, (id_item,))
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