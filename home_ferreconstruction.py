import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ferreconstruction - Inicio")
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
        
        # Categorías
        layout.addWidget(self.crear_categorias())
        
        # Campo de ubicación
        layout.addWidget(self.crear_ubicacion())
        
        # Banners promocionales
        layout.addWidget(self.crear_banner("Adhesivos Recubritech...", "#E67E50"))
        layout.addWidget(self.crear_banner("Cemento GemeX Tolteca Extra", "#A8B85C"))
        
        # Sección "Indispensable en tu obra"
        titulo = QLabel("Indispensable en tu obra")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: #2C2C2C; background-color: transparent;")
        layout.addWidget(titulo)
        
        # Productos desde la base de datos
        try:
            import pymysql
            from db_config import get_db_config
            cfg = get_db_config()
            conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM productos")
            productos = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            productos = []
            error = str(e)
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

        productos_layout = QHBoxLayout()
        if productos:
            for nombre in productos:
                productos_layout.addWidget(self.crear_producto_card(nombre))
        else:
            lbl_error = QLabel("No se pudieron cargar los productos" + (f": {error}" if 'error' in locals() else ""))
            lbl_error.setStyleSheet("color: #E74C3C; font-size: 13px;")
            productos_layout.addWidget(lbl_error)
        layout.addLayout(productos_layout)
        
        # Barra de navegación inferior
        layout.addStretch()
        layout.addWidget(self.crear_nav_bar())
        
        main_widget.setLayout(layout)
        scroll.setWidget(main_widget)
        self.setCentralWidget(scroll)
    
    def crear_header(self):
        header_layout = QHBoxLayout()
        
        logo = QLabel("🏗️")
        logo.setStyleSheet("""
            background-color: white;
            border-radius: 30px;
            padding: 10px;
            font-size: 24px;
        """)
        logo.setFixedSize(60, 60)
        logo.setAlignment(Qt.AlignCenter)
        
        titulo = QLabel("FERRECONSTRUCTION")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: #2C2C2C; background-color: transparent;")
        
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
    
    def crear_categorias(self):
        categorias_widget = QWidget()
        categorias_widget.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        categorias = ["Cemento", "Plomeria", "Ferreteria", "Aceros", "Materiales de construcción"]
        for cat in categorias:
            lbl = QLabel(cat)
            lbl.setStyleSheet("color: #3498DB; font-size: 11px; background-color: transparent;")
            layout.addWidget(lbl)
        
        categorias_widget.setLayout(layout)
        return categorias_widget
    
    def crear_ubicacion(self):
        ubicacion_widget = QWidget()
        ubicacion_widget.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        input_ubicacion = QLineEdit()
        input_ubicacion.setPlaceholderText("📍 Ingresa tu dirección o código postal para ver las tiendas")
        input_ubicacion.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 11px;
                color: #7D7D7D;
                background-color: transparent;
            }
        """)
        
        btn_ver = QPushButton("Ver tiendas")
        btn_ver.setStyleSheet("""
            QPushButton {
                background-color: #E89A3C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(input_ubicacion)
        layout.addWidget(btn_ver)
        ubicacion_widget.setLayout(layout)
        return ubicacion_widget
    
    def crear_banner(self, texto, color):
        banner = QLabel(texto)
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 30px;
            border-radius: 15px;
            font-size: 14px;
            font-weight: bold;
        """)
        banner.setFixedHeight(100)
        return banner
    
    def crear_producto_card(self, nombre):
        card = QWidget()
        card.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        img = QLabel("📦")
        img.setAlignment(Qt.AlignCenter)
        img.setStyleSheet("font-size: 36px; background-color: transparent;")

        lbl_nombre = QLabel(nombre)
        lbl_nombre.setWordWrap(True)
        lbl_nombre.setStyleSheet("color: #2C2C2C; font-size: 11px; background-color: transparent;")
        lbl_nombre.setAlignment(Qt.AlignCenter)

        # Botón agregar al carrito
        btn_agregar = QPushButton("Agregar")
        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #E89A3C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
        """)

        def on_add():
            try:
                from db_logic import add_product_to_cart
                import pymysql
                # Buscar id_producto por nombre
                cfg = __import__('db_config').get_db_config()
                conn = None
                id_producto = None
                try:
                    conn = pymysql.connect(host=cfg.get('host','localhost'), user=cfg.get('user'), password=cfg.get('password'), database=cfg.get('database'), port=int(cfg.get('port',3306)), connect_timeout=5)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_producto FROM productos WHERE nombre=%s", (nombre,))
                    row = cursor.fetchone()
                    if row:
                        id_producto = row[0]
                finally:
                    if 'conn' in locals():
                        try:
                            conn.close()
                        except Exception:
                            pass
                if not id_producto:
                    QMessageBox.warning(self, 'Error', f'No se encontró el producto en la base de datos.')
                    return
                # id_carrito fijo (ejemplo: 1), cantidad 1
                ok = add_product_to_cart(id_producto, 1, 1)
                if ok:
                    QMessageBox.information(self, 'Carrito', f'"{nombre}" agregado al carrito')
                else:
                    QMessageBox.warning(self, 'Error', f'No se pudo agregar el producto al carrito (DB)')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'No se pudo agregar el producto:\n{e}')

        btn_agregar.clicked.connect(on_add)

        layout.addWidget(img)
        layout.addWidget(lbl_nombre)
        layout.addWidget(btn_agregar)
        card.setLayout(layout)
        return card
    
    def abrir_carrito(self):
        from carrito_ferreconstruction import CarritoWindow
        self.carrito_window = CarritoWindow()
        self.carrito_window.show()
    
    def crear_nav_bar(self):
        nav_widget = QWidget()
        nav_widget.setStyleSheet("background-color: white; border-radius: 15px;")
        nav_widget.setFixedHeight(80)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        opciones = [
            ("❤️", "Favorito"),
            ("🛒", "Carrito"),
            ("🔔", "Notificación"),
            ("📞", "Llamar")
        ]
        
        for icono, texto in opciones:
            btn = QPushButton(f"{icono}\n{texto}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #3498DB;
                    border: none;
                    font-size: 10px;
                }
            """)
            if texto == "Carrito":
                btn.clicked.connect(self.abrir_carrito)
            
            layout.addWidget(btn)
        
        nav_widget.setLayout(layout)
        return nav_widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())
