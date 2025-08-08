from llm_integration import pedir_al_llm
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from datetime import datetime
from rich.live import Live
from rich.spinner import Spinner
import json 


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
        f.write("---\n")  # Añade una línea separadora


def iniciar_tutor():

    print("[bold cyan]--- Modo Tutor Socrático ---[/bold cyan]")

    tema = Prompt.ask(
        "De que tema quieres que hablemos? (Presiona Enter para 'Python básico')",
        default="Python básico",
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

    historial_conversacion = [
        {"role": "system", "content": prompt_sistema},
    ]

    # Ultimos 10 mensajes, en numero par para mantener pares de pregunta/respuesta
    MAX_HiSTORIAL = 10

    print(
        "[dim][i]Consejo: Si necesitas escribir código, puedes hacerlo en una sola línea o describirlo.[/i][/dim]"
    )

    print("[yellow]Pensando la primera pregunta...[/yellow]")
    prompt_inicial_usuario = f"Quiero aprender sobre '{tema}'. Por favor, hazme la primera pregunta para empezar."
    historial_conversacion.append({"role": "user", "content": prompt_inicial_usuario})

    with Live(Spinner("dots", text="Pensando la siguiente pregunta...")) as live:
        pregunta_actual = pedir_al_llm(
            messages=historial_conversacion
        )
        
    historial_conversacion.append({"role": "assistant", "content": pregunta_actual})    
    guardar_en_historial(nombre_historial, "Tutor", pregunta_actual)


    # BUCLE DE CONVERSACIÓN
    while True:
        print(
            Panel(
                Markdown(pregunta_actual, style="dracula"),
                title="[yellow]Pregunta del Tutor[/yellow]",
                border_style="yellow",
            )
        )

        respuesta_usuario = Prompt.ask(
            "[bold]Tu respuesta[/bold] (escribe 'salir' para terminar)"
        )

        if respuesta_usuario.lower() in ["salir", "exit", "quit"]:
            print(
                "[bold green]¡Buena sesión de estudio! La conversación ha sido guardada. ¡Hasta la próxima![/bold green]"
            )
            break

        guardar_en_historial(nombre_historial, "Usuario", respuesta_usuario)
        historial_conversacion.append(
            {"role": "user", "content": respuesta_usuario}
        )

        # --- LÓGICA DE LA VENTANA DESLIZANTE ---
        if len(historial_conversacion) > MAX_HiSTORIAL + 1:
            historial_a_enviar = [historial_conversacion[0]] + historial_conversacion[-MAX_HiSTORIAL:]
        else:
            historial_a_enviar = historial_conversacion   


        print(
            "\n[yellow]Analizando tu respuesta y pensando la siguiente pregunta...[/yellow]"
        )

      
        with Live(Spinner("dots", text=" Analizando y pensando la siguiente pregunta..."), transient=True) as live:
            pregunta_actual = pedir_al_llm(messages=historial_a_enviar)
            
        historial_conversacion.append({"role": "assistant", "content": pregunta_actual})
        guardar_en_historial(nombre_historial, "Tutor", pregunta_actual)


if __name__ == "__main__":
    print("[bold yellow]Iniciando prueba del módulo tutor...[/bold yellow]")
    iniciar_tutor()
