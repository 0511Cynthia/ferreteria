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
        # Devolver id_usuario si existe, para llevar sesión
        query = "SELECT id_usuario FROM usuarios WHERE user=%s AND password=%s"
        cursor.execute(query, (username, password))
        row = cursor.fetchone()
        if row:
            return int(row[0])
        return None
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


def get_or_create_carrito(id_usuario=1):
    """Devuelve el id_carrito asociado al usuario. Crea uno si no existe."""
    try:
        cfg = get_db_config()
        conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
        cursor = conn.cursor()
        # Buscar un carrito existente para el usuario
        cursor.execute("SELECT id_carrito FROM carritos WHERE id_usuario=%s", (id_usuario,))
        row = cursor.fetchone()
        if row:
            return int(row[0])
        # Crear nuevo carrito
        cursor.execute("INSERT INTO carritos (id_usuario) VALUES (%s)", (id_usuario,))
        conn.commit()
        return int(cursor.lastrowid)
    except Exception as e:
        print(f"Error en get_or_create_carrito: {e}")
        return None
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


def decrement_item(id_item):
    """Resta 1 a la cantidad del item indicado; si llega a 0 lo elimina. Devuelve True si cambió algo."""
    try:
        cfg = get_db_config()
        conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad FROM carrito_items WHERE id_item=%s", (id_item,))
        row = cursor.fetchone()
        if not row:
            return False
        cantidad = int(row[0])
        if cantidad > 1:
            cursor.execute("UPDATE carrito_items SET cantidad = cantidad - 1 WHERE id_item=%s", (id_item,))
        else:
            cursor.execute("DELETE FROM carrito_items WHERE id_item=%s", (id_item,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error en decrement_item: {e}")
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


def create_ticket_from_cart(id_carrito, id_usuario):
    """Crea un ticket y sus ticket_items a partir del contenido del carrito. Devuelve id_ticket o None."""
    try:
        cfg = get_db_config()
        conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
        cursor = conn.cursor()
        # Obtener items actuales
        cursor.execute("""
            SELECT ci.id_item, ci.id_producto, ci.cantidad, p.precio, p.nombre
            FROM carrito_items ci
            JOIN productos p ON ci.id_producto = p.id_producto
            WHERE ci.id_carrito = %s
        """, (id_carrito,))
        rows = cursor.fetchall()
        if not rows:
            return None
        # Calcular totales
        total_compra = 0.0
        items = []
        for id_item, id_producto, cantidad, precio, nombre in rows:
            subtotal = float(precio) * int(cantidad)
            total_compra += subtotal
            items.append({'id_producto': int(id_producto), 'cantidad': int(cantidad), 'precio': float(precio), 'subtotal': subtotal, 'nombre': nombre})
        # Insertar ticket
        cursor.execute("INSERT INTO tickets (id_usuario, total) VALUES (%s, %s)", (id_usuario, total_compra))
        id_ticket = int(cursor.lastrowid)
        # Insertar ticket_items
        for it in items:
            cursor.execute("INSERT INTO ticket_items (id_ticket, id_producto, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)", (id_ticket, it['id_producto'], it['cantidad'], it['precio'], it['subtotal']))
        # Vaciar carrito (eliminar items)
        cursor.execute("DELETE FROM carrito_items WHERE id_carrito=%s", (id_carrito,))
        conn.commit()
        return id_ticket
    except Exception as e:
        print(f"Error en create_ticket_from_cart: {e}")
        return None
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


def generate_ticket_pdf(id_ticket, filepath):
    """Genera un PDF del ticket. Requiere reportlab (`pip install reportlab`)."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        cfg = get_db_config()
        conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, total, fecha FROM tickets WHERE id_ticket=%s", (id_ticket,))
        ticket = cursor.fetchone()
        if not ticket:
            return False
        id_usuario, total, fecha = ticket
        cursor.execute("SELECT ti.id_producto, ti.cantidad, ti.precio_unitario, ti.subtotal, p.nombre FROM ticket_items ti JOIN productos p ON ti.id_producto = p.id_producto WHERE ti.id_ticket=%s", (id_ticket,))
        items = cursor.fetchall()
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        y = height - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, f"Ticket #{id_ticket}")
        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Usuario: {id_usuario}")
        y -= 20
        c.drawString(50, y, f"Fecha: {fecha}")
        y -= 30
        c.drawString(50, y, "Producto")
        c.drawString(280, y, "Cantidad")
        c.drawString(350, y, "Precio unit.")
        c.drawString(450, y, "Subtotal")
        y -= 20
        for pid, cantidad, precio, subtotal, nombre in items:
            c.drawString(50, y, str(nombre))
            c.drawString(280, y, str(cantidad))
            c.drawString(350, y, f"{precio:.2f}")
            c.drawString(450, y, f"{subtotal:.2f}")
            y -= 18
            if y < 80:
                c.showPage()
                y = height - 50
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, y, "Total:")
        c.drawString(450, y, f"{float(total):.2f}")
        c.save()
        return True
    except Exception as e:
        print(f"Error en generate_ticket_pdf: {e}")
        return False

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