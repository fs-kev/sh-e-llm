from tutor_socratico import iniciar_tutor
from traductor_codigo import iniciar_traduccion
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel



while True:

    print(Panel("""
[bold cyan]Bienvenido a sh-e-llm[/bold cyan]

Selecciona una opción:
1. Iniciar Tutor Socrático
2. Traducir Código
3. Salir
"""
,
title='Menu Principal sh-e-llm',border_style="blue"))

    opcion = Prompt.ask("[bold]Elige una opción[/bold]", choices=["1", "2", "3"], default="1")

    if opcion == "1":
        iniciar_tutor()
    elif opcion == "2":
        iniciar_traduccion()
    elif opcion == "3":
        print("[bold green]¡Hasta luego! Gracias por usar sh-e-llm.[/bold green]")
        break
    else:
        print("[bold red]Opción no válida. Por favor, elige 1, 2 o 3.[/bold red]")

    print("\n")

