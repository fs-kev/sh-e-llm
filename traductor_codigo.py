from llm_integration import pedir_al_llm
from rich.panel import Panel
from rich import print
from rich.syntax import Syntax
from rich.markdown import Markdown
import sys


def iniciar_traduccion():
    """
    Inicia el modo traductor de código, donde el usuario puede pegar un fragmento de código
    """

    print("[bold cyan]--- Modo Traductor de Código ---[/bold cyan]")
    print(
        "Pega tu código aquí. Cuando termines, presiona Ctrl+D (en Mac/Linux) o Ctrl+Z y Enter (en Windows)."
    )

    codigo_usuario = sys.stdin.read()

    if not codigo_usuario.strip():
        print(
            "[bold red]No se ha ingresado ningún código. Volviendo al menú principal.[/bold red]"
        )
        return

    print("\n[bold]Código recibido:[/bold]")
    codigo_resaltado = Syntax(
        codigo_usuario, "python", theme="dracula", line_numbers=True
    )
    print(codigo_resaltado)

    prompt_sistema = "Eres un programador Python senior y un excelente profesor. Tu tarea es explicar código de forma clara y sencilla para un principiante."
    prompt_usuario = (
        f"Por favor, explica el siguiente fragmento de código paso a paso. "
        f"Detalla qué hace cada parte importante y para qué sirven las librerías si las hay.\n\n"
        f"```python\n{codigo_usuario}\n```"
    )

    print(
        "\n[yellow]Analizando el código... Contactando al LLM para obtener la explicación.[/yellow]"
    )

    explicacion = pedir_al_llm(prompt=prompt_usuario, system_prompt=prompt_sistema)

    print(
        Panel(
            Markdown(explicacion, style="dracula"),
            title="[green]Análisis del Código[/green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    print("[bold yellow]Iniciando prueba del módulo traductor...[/bold yellow]")
    iniciar_traduccion()
