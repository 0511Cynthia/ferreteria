import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Modelo simple de carrito compartido
cart_items = []  # cada item: dict con al menos {'name': ..., 'price': ...}
_cart_listeners = []

def add_to_cart(item):
    """Agregar item al carrito y notificar listeners."""
    cart_items.append(item)
    for cb in list(_cart_listeners):
        try:
            cb()
        except Exception:
            pass

def remove_from_cart(index):
    """Remover item por índice y notificar listeners."""
    if 0 <= index < len(cart_items):
        cart_items.pop(index)
        for cb in list(_cart_listeners):
            try:
                cb()
            except Exception:
                pass

def register_cart_listener(cb):
    if cb not in _cart_listeners:
        _cart_listeners.append(cb)

def unregister_cart_listener(cb):
    if cb in _cart_listeners:
        _cart_listeners.remove(cb)

class CarritoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ferreconstruction - Carrito")
        self.setFixedSize(400, 700)
        self.setStyleSheet("background-color: #C5C9CC;")
        
        # Widget principal con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #C5C9CC;")
        
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.crear_header()
        layout.addLayout(header)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.crear_menu_button())
        search_layout.addWidget(self.crear_search_bar())
        layout.addLayout(search_layout)
        
        # Banner de envío gratis
        banner = QLabel("Envío gratis con monto mínimo de $500")
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
            color: #7D7D7D;
        """)
        layout.addWidget(banner)
        
        # Título "Producto seleccionado"
        titulo = QLabel("Producto seleccionado")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setStyleSheet("color: #2C2C2C; background-color: transparent;")
        layout.addWidget(titulo)
        
        # Contenedor dinámico de productos en carrito
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout()
        self.items_layout.setSpacing(10)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_container.setLayout(self.items_layout)
        layout.addWidget(self.items_container)

        # Inicializar vista con items actuales
        self.refresh_cart()
        register_cart_listener(self.refresh_cart)
        
        # Botón Comprar ahora
        btn_comprar = QPushButton("Comprar ahora")
        btn_comprar.setStyleSheet("""
            QPushButton {
                background-color: #8B9DC3;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(btn_comprar)
        
        # Info de envío
        envio = QLabel("Envió 1\nllega martes entre 6am y 7am.")
        envio.setAlignment(Qt.AlignCenter)
        envio.setStyleSheet("color: #2C2C2C; font-size: 13px; background-color: transparent;")
        layout.addWidget(envio)
        
        layout.addStretch()
        main_widget.setLayout(layout)
        scroll.setWidget(main_widget)
        self.setCentralWidget(scroll)
    
    def crear_header(self):
        header_layout = QHBoxLayout()
        
        # Logo
        logo = QLabel("🏗️")
        logo.setStyleSheet("""
            background-color: white;
            border-radius: 30px;
            padding: 10px;
            font-size: 24px;
        """)
        logo.setFixedSize(60, 60)
        logo.setAlignment(Qt.AlignCenter)
        
        # Título
        titulo = QLabel("FERRECONSTRUCTION")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: #2C2C2C; background-color: transparent;")
        
        # Botón Iniciar sesión
        btn_login = QPushButton("👤\nIniciar sesión")
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498DB;
                border: none;
                font-size: 11px;
            }
        """)
        
        header_layout.addWidget(logo)
        header_layout.addWidget(titulo)
        header_layout.addStretch()
        header_layout.addWidget(btn_login)
        
        return header_layout
    
    def crear_menu_button(self):
        btn = QPushButton("☰\nMás")
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2C2C2C;
                border: none;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        btn.setFixedWidth(60)
        return btn
    
    def crear_search_bar(self):
        search = QLineEdit()
        search.setPlaceholderText("Buscar en Ferreconstruction                    🔍")
        search.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 13px;
                color: #7D7D7D;
            }
        """)
        return search
    
    def crear_producto(self, nombre, precio):
        producto_widget = QWidget()
        producto_widget.setStyleSheet("background-color: #B8BCC0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Nombre del producto
        lbl_nombre = QLabel(nombre)
        lbl_nombre.setStyleSheet("color: #2C2C2C; font-size: 13px; background-color: transparent;")
        layout.addWidget(lbl_nombre)
        
        # Imagen placeholder
        img = QLabel("📦")
        img.setAlignment(Qt.AlignCenter)
        img.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 30px;
            font-size: 48px;
        """)
        img.setFixedHeight(150)
        layout.addWidget(img)
        
        # Precio
        lbl_precio = QLabel(precio)
        lbl_precio.setFont(QFont("Arial", 14, QFont.Bold))
        lbl_precio.setStyleSheet("color: #2C2C2C; background-color: transparent;")
        layout.addWidget(lbl_precio)
        
        # Controles de cantidad
        controles = QHBoxLayout()
        btn_menos = self.crear_boton_cantidad("−")
        lbl_cantidad = QLabel("0")
        lbl_cantidad.setAlignment(Qt.AlignCenter)
        lbl_cantidad.setStyleSheet("""
            background-color: #8B8B8B;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
        """)
        lbl_cantidad.setFixedSize(60, 40)
        btn_mas = self.crear_boton_cantidad("+")
        
        controles.addWidget(btn_menos)
        controles.addWidget(lbl_cantidad)
        controles.addWidget(btn_mas)
        controles.addStretch()
        
        layout.addLayout(controles)
        producto_widget.setLayout(layout)
        return producto_widget

    def refresh_cart(self):
        # Limpiar layout existente
        for i in reversed(range(self.items_layout.count())):
            w = self.items_layout.itemAt(i).widget()
            if w is not None:
                w.setParent(None)

        # Obtener productos del carrito desde la base de datos
        try:
            import mysql.connector
            from db_config import get_db_config
            conn = mysql.connector.connect(**get_db_config())
            cursor = conn.cursor()
            # id_carrito fijo (ejemplo: 1)
            cursor.execute("""
                SELECT p.nombre, p.precio, c.cantidad, c.id_producto
                FROM carrito c
                JOIN productos p ON c.id_producto = p.id_producto
                WHERE c.id_carrito = %s
            """, (1,))
            rows = cursor.fetchall()
        except Exception as e:
            rows = []
            error = str(e)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

        if not rows:
            empty = QLabel("Tu carrito está vacío")
            empty.setStyleSheet("color: #2C2C2C; font-size: 14px; background-color: transparent;")
            empty.setAlignment(Qt.AlignCenter)
            self.items_layout.addWidget(empty)
            return

        # Encabezado
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.addWidget(QLabel("Producto"))
        header_layout.addWidget(QLabel("Precio"))
        header_layout.addWidget(QLabel("Cantidad"))
        header_layout.addStretch()
        header_layout.addWidget(QLabel(""))  # espacio para botón
        header.setLayout(header_layout)
        self.items_layout.addWidget(header)

        for nombre, precio, cantidad, id_producto in rows:
            row = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(10, 10, 10, 10)

            lbl_nombre = QLabel(str(nombre))
            lbl_nombre.setStyleSheet("color: #2C2C2C; background-color: transparent;")
            row_layout.addWidget(lbl_nombre)

            lbl_precio = QLabel(f"${precio}")
            lbl_precio.setStyleSheet("color: #2C2C2C; background-color: transparent;")
            row_layout.addWidget(lbl_precio)

            lbl_cantidad = QLabel(str(cantidad))
            lbl_cantidad.setStyleSheet("color: #2C2C2C; background-color: transparent;")
            row_layout.addWidget(lbl_cantidad)

            row_layout.addStretch()

            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 12px;
                }
            """)
            def on_remove(checked=False, id_prod=id_producto):
                try:
                    from db_logic import remove_from_cart
                    # Elimina todas las filas de ese producto para el carrito actual
                    while True:
                        ok = remove_from_cart(id_prod, 1)
                        if not ok:
                            break
                    self.refresh_cart()
                except Exception as e:
                    pass
            btn_eliminar.clicked.connect(on_remove)
            row_layout.addWidget(btn_eliminar)
            row.setLayout(row_layout)
            self.items_layout.addWidget(row)

    def closeEvent(self, event):
        # Desregistrar listener cuando la ventana se cierra
        try:
            unregister_cart_listener(self.refresh_cart)
        except Exception:
            pass
        super().closeEvent(event)
    
    def crear_boton_cantidad(self, texto):
        btn = QPushButton(texto)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #6B6B6B;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        btn.setFixedSize(40, 40)
        return btn

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CarritoWindow()
    window.show()
    sys.exit(app.exec_())
