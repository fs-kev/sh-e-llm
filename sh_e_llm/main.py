import typer
from rich import print

app  = typer.Typer(
    name="shelm",
    help="A smart, LLM-powered shell assistant with soul.",
    add_completion=False
)

@app.command()

def chat(
    persona_name: str = typer.Argument(..., help="The name of the persona to chat with.")
):
    """
    Starts a new chat session with a specified persona.
    """
    print(f"[bold green]Starting chat session with persona:[/bold green] [yellow]{persona_name}[/yellow]")
    print("[dim]Chat logic not implemented yet.[/dim]")

@app.command()
def personas():
    """
    Lists all available personas from the configuration file.
    """
    print("[bold cyan]Listing available personas...[/bold cyan]")
    print("[dim]Persona listing not implemented yet.[/dim]")

if __name__ == "__main__":
    app()