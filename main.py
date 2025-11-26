import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QPainter

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #titulo
        self.setWindowTitle("FERRECONSTRUCTION - Login")
        self.setFixedSize(400, 550)
        
        self.setStyleSheet("QMainWindow { background-color: #C5C9CC; }")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)

        #contenedor del logo
        logo_container = QWidget()
        logo_container.setStyleSheet("background-color: white; border-radius: 60px;")
        logo_container.setFixedSize(120, 120)
        
        logo_layout = QVBoxLayout()
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_container.setLayout(logo_layout)

        #logo
        logo_label = QLabel("🏗")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 60px; background-color: transparent; padding: 20px;")
        logo_layout.addWidget(logo_label)
        
        logo_h_layout = QHBoxLayout()
        logo_h_layout.addStretch()
        logo_h_layout.addWidget(logo_container)
        logo_h_layout.addStretch()
        main_layout.addLayout(logo_h_layout)
        
        #titulo
        company_label = QLabel("FERRECONSTRUCTION")
        company_label.setAlignment(Qt.AlignCenter)
        company_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        main_layout.addWidget(company_label)
        
        #label iniciar seción
        subtitle_label = QLabel("Iniciar sesión")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 18px; color: #3498DB; margin-bottom: 15px;")
        main_layout.addWidget(subtitle_label)
        
        #label usuario
        username_label = QLabel("Usuario")
        username_label.setStyleSheet("font-size: 13px; color: #2C3E50;")
        main_layout.addWidget(username_label)
        
        #input usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu usuario")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 30px;
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                background-color: white;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
            }
        """)
        main_layout.addWidget(self.username_input)
        
        #label password
        password_label = QLabel("Contraseña")
        password_label.setStyleSheet("font-size: 13px; color: #2C3E50; margin-top: 14px;")
        main_layout.addWidget(password_label)
        
        #input password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 30px;
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                background-color: white;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
            }
        """)
        main_layout.addWidget(self.password_input)
        
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 25px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.login_button.clicked.connect(self.login_clicked)
        main_layout.addWidget(self.login_button)
        
        # intentos permitidos
        self.attempts_remaining = 3
        
        main_layout.addSpacing(20)
        
    def login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # validar credenciales en la base de datos
        try:
            from db_logic import validate_user
            user_id = validate_user(username, password)
        except ImportError as e:
            print(f"ERROR: No se pudo importar db_logic - {e}")
            QMessageBox.critical(self, 'Error de importación', f'No se pudo encontrar el módulo de base de datos:\n{e}')
            return
        except Exception as e:
            print(f"ERROR: Excepción en validate_user - {e}")
            QMessageBox.critical(self, 'Error de conexión', f'No se pudo conectar a la base de datos:\n{e}')
            return

        if user_id:
            try:
                from home_ferreconstruction import HomeWindow
                self.home_window = HomeWindow(user_id)
                self.home_window.show()
                self.close()

            except ImportError as e:
                print(f"ERROR: No se pudo importar home_ferreconstruction - {e}")
                QMessageBox.critical(self, 'Error', f'No se pudo encontrar la ventana principal:\n{e}')
            except Exception as e:
                print(f"ERROR: Excepción al crear HomeWindow - {e}")
                QMessageBox.critical(self, 'Error', f'No se pudo abrir la ventana principal:\n{type(e).__name__}: {e}')
        else:
            # decrementar intentos
            self.attempts_remaining -= 1
            if self.attempts_remaining > 0:
                QMessageBox.warning(self, 'Credenciales inválidas',
                                    f'Usuario o contraseña incorrectos, te quedan {self.attempts_remaining} intentos')
            else:
                # sin intentos: mostrar mensaje y cerrar app
                QMessageBox.warning(self, 'Credenciales inválidas',
                                    'Usuario o contraseña incorrectos. No quedan intentos.')
                QApplication.quit()


def validate_credentials(user, password):
    """Obsoleto: ahora se valida contra la base de datos."""
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())