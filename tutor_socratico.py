from llm_integration import pedir_al_llm
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from datetime import datetime
import sys

def guardar_en_historial(nombre_archivo: str, rol: str, texto: str):
    """
    Añade una entrada al archivo de historial en formato Markdown.
    'rol' puede ser "Tutor" o "Usuario".
    """

    with open(nombre_archivo, "a", encoding="utf-8") as f:
        if rol == "Tutor":
            f.write(f"### 🧑‍🏫 Tutor\n{texto}\n\n")
        else:
            f.write(f"### 🧑‍💻 Usuario\n**{texto}**\n\n")
        f.write("---\n") # Añade una línea separadora


def iniciar_tutor():

    print("[bold cyan]--- Modo Tutor Socrático ---[/bold cyan]")

    tema = Prompt.ask(
        "De que tema quieres que hablemos? (Presiona Enter para 'Python básico')",
        default="Python básico"
        )
    print(f"[dim]Perfecto, vamos a hablar sobre: [bold]{tema}[/bold][/dim]")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_historial = f"historial_{tema.replace(' ', '_').lower()}_{timestamp}.md"
    print(f"[dim]La conversación se guardará en: {nombre_historial}[/dim]\n")


    prompt_sistema = (
    "Eres 'sh-e-llm', un tutor experto de élite especializado en Python y su aplicación en el análisis de datos biológicos (Bioinformática). "
    "Tu método de enseñanza es estrictamente socrático: guías al estudiante con preguntas inteligentes, nunca das la respuesta directa. "
    "Tu objetivo es que el estudiante razone y llegue a sus propias conclusiones. "
    "Si el tema es sobre bioinformática, puedes usar ejemplos biológicos. Si es sobre Python general, mantente en ese carril. "
    "Tu tono es siempre amigable, paciente y alentador."
    )

    print("[dim][i]Consejo: Si necesitas escribir código, puedes hacerlo en una sola línea o describirlo.[/i][/dim]")

    print("[yellow]Pensando la primera pregunta...[/yellow]")
    prompt_inicial_usuario = f"Quiero aprender sobre '{tema}'. Por favor, hazme la primera pregunta para empezar."

    pregunta_actual = pedir_al_llm(prompt=prompt_inicial_usuario, system_prompt=prompt_sistema)
    guardar_en_historial(nombre_historial, "Tutor", pregunta_actual)


    # Bucle conversacion
    while True:
        print(Panel(Markdown(pregunta_actual, style="dracula"), title="[yellow]Pregunta del Tutor[/yellow]", border_style="yellow"))
    
        respuesta_usuario = Prompt.ask("[bold]Tu respuesta[/bold] (escribe 'salir' para terminar)")

        if respuesta_usuario.lower() in ["salir", "exit", "quit"]:
            print("[bold green]¡Buena sesión de estudio! La conversación ha sido guardada. ¡Hasta la próxima![/bold green]")
            break

        guardar_en_historial(nombre_historial, "Usuario", respuesta_usuario)


        print("\n[yellow]Analizando tu respuesta y pensando la siguiente pregunta...[/yellow]")
        
        prompt_siguiente_pregunta = (
            f"El tema es '{tema}'. La pregunta anterior fue: '{pregunta_actual}'. "
            f"Mi respuesta fue: '{respuesta_usuario}'. "
            "Por favor, evalúa mi respuesta brevemente y hazme la siguiente pregunta socrática para continuar."
        )

        pregunta_actual = pedir_al_llm(prompt=prompt_siguiente_pregunta, system_prompt=prompt_sistema)
        guardar_en_historial(nombre_historial, "Tutor", pregunta_actual)


if __name__ == "__main__":
    print("[bold yellow]Iniciando prueba del módulo tutor...[/bold yellow]")
    iniciar_tutor()