from rich.console import Console
from rich.panel import Panel

# Inicializa o console do Rich
console = Console()


def log_ping_start(host: str):
    console.print(
        f"\n[bold cyan]🔍 Iniciando teste de Ping para:[/bold cyan] [bold yellow]{host}[/bold yellow]..."
    )


def log_ping_success(host: str, output: str):
    msg = f"[bold green]✅ Sucesso na comunicação![/bold green]\n\n[dim]{output}[/dim]"
    console.print(Panel(msg, title=f"Ping: {host}", border_style="green"))


def log_ping_timeout(host: str):
    msg = f"[bold yellow]⚠️ Esgotado o tempo limite (Timeout).[/bold yellow]\nO servidor {host} não respondeu."
    console.print(Panel(msg, title=f"Timeout: {host}", border_style="yellow"))


def log_ping_error(host: str, error_msg: str):
    msg = f"[bold red]❌ Erro crítico ao pingar o destino.[/bold red]\n\n[white]Detalhes:[/white] {error_msg}"
    console.print(Panel(msg, title=f"Falha: {host}", border_style="red"))
