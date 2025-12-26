import flet as ft
import os
import datetime
from dotenv import load_dotenv
from ecotech import Database, Auth, Finance

load_dotenv()


class App:
    def __init__(self, page: ft.Page):
        
        self.page = page
        self.page.title = "Ecotech Solutions"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.bgcolor = ft.Colors.GREY_100
        
        self.primary_color = ft.Colors.GREEN_700
        self.card_color = ft.Colors.WHITE
        
        # BD y servicios
        self.db = Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )
        self.db.create_all_tables()

        self.finance = Finance()
        self.user_id = None
        self.username = ""

        self.page_register()
        

    def card(self, controls, width=420):
        return ft.Container(
        content=ft.Column(
            controls,
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=width,
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 8)
        )
    )

    
    def primary_button(self, text, on_click):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=self.primary_color,
            color=ft.Colors.WHITE,
            width=280,
            height=48,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
    
    def input(self, label, password=False):
        return ft.TextField(
            label=label,
            password=password,
            can_reveal_password=password,
            width=250,
            border_radius=8
        )  
    # ================= REGISTRO =================
    def page_register(self):
        self.page.controls.clear()

        self.input_id = self.input("ID usuario (numérico)")
        self.input_username = self.input("Usuario")
        self.input_password = self.input("Contraseña", password=True)

        self.text_status = ft.Text(size=12)

        self.page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    # TÍTULO
                    ft.Text(
                        "Ecotech Solutions",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        "Crea tu cuenta para continuar",
                        size=14,
                        color=ft.Colors.GREY_700
                    ),

                    ft.Container(height=20),

                    # CARD
                    self.card([
                        self.input_id,
                        self.input_username,
                        self.input_password,
                        self.primary_button("Registrarse", self.handle_register),
                        self.text_status,
                        ft.TextButton(
                            "¿Ya tienes cuenta? Inicia sesión",
                            on_click=lambda e: self.page_login()
                        )
                    ])
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )


    def handle_register(self, e):
        try:
            # Validaciones básicas
            if not self.input_id.value or not self.input_username.value or not self.input_password.value:
                self.text_status.value = "Todos los campos son obligatorios"
                self.text_status.color = ft.Colors.RED
                self.page.update()
                return

            Auth.register(
                db=self.db,
                id=int(self.input_id.value),
                username=self.input_username.value.strip(),
                password=self.input_password.value.strip()
            )

            # Mensaje de éxito
            self.text_status.value = "Usuario registrado correctamente"
            self.text_status.color = ft.Colors.GREEN
            self.page.update()

            # Ir a login
            self.page_login()

        except ValueError:
            self.text_status.value = "El ID debe ser numérico"
            self.text_status.color = ft.Colors.RED
            self.page.update()

        except Exception as err:
            self.text_status.value = f"Error: {err}"
            self.text_status.color = ft.Colors.RED
            self.page.update()
    # ================= LOGIN =================
    def handle_login(self, e):
        try:
            if not self.input_username.value or not self.input_password.value:
                self.text_status.value = "Ingrese usuario y contraseña"
                self.text_status.color = ft.Colors.RED
                self.page.update()
                return

            user_id = Auth.login(
                db=self.db,
                username=self.input_username.value.strip(),
                password=self.input_password.value.strip()
            )

            if user_id:
                self.user_id = user_id               # ✅ ES UN INT
                self.username = self.input_username.value.strip()
                self.page_main_menu()
            else:
                self.text_status.value = "Credenciales incorrectas"
                self.text_status.color = ft.Colors.RED
                self.page.update()

        except Exception as err:
            self.text_status.value = f"Error: {err}"
            self.text_status.color = ft.Colors.RED
            self.page.update()
        
    def page_login(self):
        self.page.controls.clear()

        self.input_username = self.input("Usuario")
        self.input_password = self.input("Contraseña", password=True)
        self.text_status = ft.Text(size=12)

        self.page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,  # 🎯 CENTRADO REAL
            content=ft.Column(
                [
                    # TÍTULO
                    ft.Text(
                        "Iniciar sesión",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Container(height=20),

                    # CARD
                    self.card([
                        self.input_username,
                        self.input_password,
                        self.primary_button("Entrar", self.handle_login),
                        self.text_status,
                        ft.TextButton(
                            "Registrarse",
                            on_click=lambda e: self.page_register()
                        )
                    ])
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )
        self.page.update()

    # ================= MENÚ PRINCIPAL =================
    def page_main_menu(self):
        self.page.controls.clear()

        self.page.add(
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Text(
                            f"Bienvenido, {self.username}",
                            size=26,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Container(height=20),

                        self.card([
                            self.primary_button(
                                "Consultar indicador",
                                lambda e: self.page_indicator()
                            ),
                            self.primary_button(
                                "Ver historial",
                                lambda e: self.page_history()
                            ),
                            ft.OutlinedButton(
                                "Cerrar sesión",
                                width=280,
                                on_click=lambda e: self.page_login()
                            )
                        ])
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )

        self.page.update()
    # ================= CONSULTA INDICADOR =================
    def page_indicator(self):
        self.page.controls.clear()

        self.dropdown = ft.Dropdown(
            label="Indicador",
            options=[
                ft.dropdown.Option("dolar"),
                ft.dropdown.Option("euro"),
                ft.dropdown.Option("uf"),
                ft.dropdown.Option("ipc"),
                ft.dropdown.Option("utm"),
            ],
            width=250
        )

        self.date_input = self.input("Fecha (DD-MM-YYYY)")
        self.result_text = ft.Text(size=16, weight="bold")

        self.page.add(
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Text(
                            "Consulta de indicadores",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Container(height=20),

                        self.card([
                            self.dropdown,
                            self.date_input,
                            self.primary_button("Consultar", self.handle_indicator),
                            self.result_text,
                            ft.TextButton(
                                "Volver",
                                on_click=lambda e: self.page_main_menu()
                            )
                        ])
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )

    def handle_indicator(self, e):
        try:
            if not self.dropdown.value:
                self.result_text.value = "Seleccione un indicador"
                self.page.update()
                return

            indicator = self.dropdown.value
            date_str = self.date_input.value.strip()

            # ───── Fecha solo para BD ─────
            if date_str:
                try:
                    dt = datetime.datetime.strptime(date_str, "%d-%m-%Y")
                    oracle_date = dt.strftime("%Y-%m-%d")
                except ValueError:
                    self.result_text.value = "Formato de fecha inválido (DD-MM-YYYY)"
                    self.page.update()
                    return
            else:
                oracle_date = datetime.date.today().strftime("%Y-%m-%d")

            # ───── Obtener indicador ─────
            if indicator == "ipc":
                # 🔥 IGNORA la fecha completamente
                value = self.finance.get_ipc()
            else:
                value = self.finance.get_chilean_indicator(indicator, oracle_date)

            if value is None:
                self.result_text.value = "No se pudo obtener el indicador"
                self.page.update()
                return

            self.result_text.value = f"Valor: {value}"

            # ───── Guardar historial ─────
            self.db.insert_indicator_history(
                indicator_name=indicator,
                value=value,
                value_date=oracle_date,
                source="mindicador.cl",
                retrieved_by=self.user_id
            )

            self.page.update()

        except Exception as err:
            self.result_text.value = f"Error: {err}"
            self.page.update()


    
    # ================= HISTORIAL =================
    def page_history(self):
        self.page.controls.clear()

        history = self.db.get_indicator_history(self.user_id)

        items = [
            ft.ListTile(
                title=ft.Text(h[0].upper()),
                subtitle=ft.Text(f"{h[2]} | {h[1]}"),
                trailing=ft.Text(h[3])
            )
            for h in history
        ] if history else [ft.Text("No hay registros")]

        self.page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text(
                        "Historial de consultas",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Container(height=20),

                    self.card(items, width=520),

                    ft.TextButton(
                        "Volver",
                        on_click=lambda e: self.page_main_menu()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )


if __name__ == "__main__":
    ft.app(target=App)
