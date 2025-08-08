import os
from tutor_socratico import iniciar_tutor
from traductor_codigo import iniciar_traduccion
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.align import Align

def limpiar_pantalla():
    """Limpia la pantalla de la terminal, compatible con Windows, Mac y Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_splash_screen():
    """Muestra una pantalla de bienvenida única al inicio."""
    limpiar_pantalla()
    print(Panel(
        Align.center(
            Text("La terminal se encuentra con la inteligencia.\nUna shell con alma.", justify="center")
            ),
            title="[bold cyan]sh-e-llm[/bold cyan]",
            subtitle="[dim]v0.8[/dim]",
            border_style="bold blue"
        )
    )
    Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

def mostrar_menu_principal():
    """Muestra el menú de opciones principal."""
    limpiar_pantalla()
    print(Rule("[bold blue]Menú Principal[/bold blue]", style="blue"))
    

    menu_text = Text.from_markup(
        """
[bold]1. 🧑‍🏫 Iniciar Tutor Socrático[/bold]
   [dim]Aprende un tema con preguntas guiadas por la IA.[/dim]

[bold]2. ↔️ Traducir Código[/bold]
   [dim]Obtén una explicación detallada de un fragmento de código.[/dim]

[bold]3. 🚪 Salir[/bold]
   [dim]Cierra la aplicación.[/dim]
"""
    )
    
    print(Panel(menu_text, border_style="blue"))

# --- Bucle Principal de la Aplicación ---

mostrar_splash_screen()

while True:
    mostrar_menu_principal()

    opcion = Prompt.ask(
        "[bold]Elige una opción[/bold]", choices=["1", "2", "3"]
    )

    limpiar_pantalla() 

    if opcion == "1":
        print(Rule("[bold green]Iniciando Tutor Socrático...[/bold green]", style="green"))
        iniciar_tutor()
    elif opcion == "2":
        print(Rule("[bold green]Iniciando Traductor de Código...[/bold green]", style="green"))
        iniciar_traduccion()
    elif opcion == "3":
        print("[bold magenta]¡Hasta luego! Gracias por usar sh-e-llm.[/bold magenta]")
        break
    
    # Pausa para que el usuario pueda ver la salida del módulo antes de volver al menú
    Prompt.ask("\n[dim]Módulo finalizado. Presiona Enter para volver al menú principal...[/dim]")