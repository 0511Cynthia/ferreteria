import pymysql
from pymysql.err import MySQLError as DBError
from db_config import get_db_config

def validate_user(username, password):
    """Valida si el usuario y contraseña existen en la tabla Login."""
    try:
        # Añadir un timeout de conexión corto para evitar bloqueos largos
        cfg = get_db_config()
        # Hacer una verificación TCP rápida para detectar problemas de red/puerto
        try:
            import socket
            host = cfg.get('host', 'localhost')
            port = int(cfg.get('port', 3306))
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
        except Exception as e:
            # TCP check failed; continue and let connect handle errors
            pass
        # Intentar conectar con PyMySQL en un hilo con timeout para evitar bloqueos
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
        host = cfg.get('host', 'localhost')
        port = int(cfg.get('port', 3306))
        user = cfg.get('user')
        password_cfg = cfg.get('password')
        database = cfg.get('database')
        cfg_connect_kwargs = {
            'host': host,
            'user': user,
            'password': password_cfg,
            'database': database,
            'port': port,
            'connect_timeout': 5,
        }
        # iniciar conexión PyMySQL en hilo con timeout
        conn = None
        try:
            with ThreadPoolExecutor(max_workers=1) as ex:
                future = ex.submit(pymysql.connect, **cfg_connect_kwargs)
                try:
                    conn = future.result(timeout=6)
                except FutureTimeout:
                    return False
                except Exception:
                    return False
        except Exception as e:
            return False
            return False
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM usuarios WHERE user=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return (result is not None) and (result[0] > 0)
    except DBError as e:
        print(f"Error en validate_user: {e}")
        return False
    finally:
        if 'cursor' in locals():
            try:
                cursor.close()
            except Exception:
                pass
        if 'conn' in locals():
            try:
                conn.close()
            except Exception:
                pass

def add_product_to_cart(id_producto, cantidad, id_carrito):
    """Agrega un producto al carrito (tabla Carrito). Si ya existe, suma la cantidad."""
    try:
        cfg = get_db_config()
        conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
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
    except DBError as e:
        print(f"Error en add_product_to_cart: {e}")
        return False
    finally:
        if 'cursor' in locals():
            try:
                cursor.close()
            except Exception:
                pass
        if 'conn' in locals():
            try:
                conn.close()
            except Exception:
                pass

def remove_from_cart(id_item):
    """Elimina un item del carrito en la tabla `carrito_items` por su `id_item`.

    Parámetro:
    - id_item: primary key (INT) de la tabla `carrito_items`.
    """
    try:
        cfg = get_db_config()
        conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
        cursor = conn.cursor()
        query = "DELETE FROM carrito_items WHERE id_item=%s"
        cursor.execute(query, (id_item,))
        conn.commit()
        return cursor.rowcount > 0
    except DBError as e:
        print(f"Error en remove_from_cart: {e}")
        return False
    finally:
        if 'cursor' in locals():
            try:
                cursor.close()
            except Exception:
                pass
        if 'conn' in locals():
            try:
                conn.close()
            except Exception:
                pass