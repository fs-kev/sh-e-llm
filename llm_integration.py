# llm_integration.py

import requests
import json
import os
from dotenv import load_dotenv
from rich import print


load_dotenv()


# Verificar la conexión a la API de Groq y listar modelos disponibles
# api_key = os.getenv("GROQ_API_KEY")
# url = "https://api.groq.com/openai/v1/models"

# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# response = requests.get(url, headers=headers)

# print(response.json())

# --- Configuración de Proveedores en Orden de Prioridad ---
PROVEEDORES_EN_ORDEN = [
    {
        "nombre": "Groq",
        "api_url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key": os.getenv("GROQ_API_KEY"),
        "modelo": "moonshotai/kimi-k2-instruct",
    },
    {
        "nombre": "OpenRouter",
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        # "modelo": "qwen/qwen3-30b-a3b:free"
        "modelo": "z-ai/glm-4.5-air:free",
    },
]


def pedir_al_llm(prompt: str, system_prompt: str) -> str:
    """
    Pide una respuesta a los LLMs configurados, en orden de prioridad.
    Intentará con el primer proveedor. Si falla, pasará automáticamente al siguiente.
    """

    for proveedor in PROVEEDORES_EN_ORDEN:
        nombre_proveedor = proveedor["nombre"]
        api_url = proveedor["api_url"]
        api_key = proveedor["api_key"]
        modelo = proveedor["modelo"]

        # Si no hay clave de API para este proveedor, sáltalo y pasa al siguiente
        if not api_key:
            print(
                f"[yellow]Advertencia: No se encontró clave de API para {nombre_proveedor}. Saltando...[/yellow]"
            )
            continue

        print(f"[yellow]Intentando con el proveedor: {nombre_proveedor}...[/yellow]")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        body = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }

        try:
            response = requests.post(
                api_url, headers=headers, data=json.dumps(body), timeout=30
            )
            response.raise_for_status()  # Lanza un error si la respuesta no es 2xx

            # Si llegamos aquí, la petición fue exitosa. Devolvemos la respuesta.
            respuesta_json = response.json()
            contenido = respuesta_json["choices"][0]["message"]["content"]

            print(f"[green]Respuesta recibida de {nombre_proveedor}![/green]")
            return contenido

        except requests.exceptions.RequestException as e:
            # Si hay un error de red o de HTTP, lo notificamos y el bucle continuará con el siguiente proveedor.
            print(f"[bold red]Falló {nombre_proveedor}: {e}[/bold red]")
            continue  # Pasa al siguiente proveedor en la lista

    # Si el bucle termina y ningún proveedor funcionó, devolvemos un mensaje de error final.
    print("[bold red]Todos los proveedores de LLM fallaron.[/bold red]")
    return "Lo siento, no pude conectarme con ninguno de mis cerebros en este momento. Por favor, verifica tu conexión a internet y las claves de API."


if __name__ == "__main__":
    print("[bold yellow]Iniciando prueba del módulo llm_integration...[/bold yellow]")
    prompt = "¿Qué es Python?"
    system_prompt = (
        "Eres un experto en Python y debes responder de manera clara y concisa."
    )
    respuesta = pedir_al_llm(prompt, system_prompt)
    print(f"[bold green]Respuesta del LLM:[/bold green] {respuesta}")
