
import asyncio
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.markdown import Markdown
from dotenv import load_dotenv

from Artistic_DeepResearch.deep_researcher import deep_researcher_builder
from Artistic_DeepResearch.report_generator import generate_artistic_report
from Artistic_DeepResearch.utils import get_today_str

load_dotenv()

app = typer.Typer(help="Artistic Deep Research CLI")
console = Console()

async def run_research(topic: str, recursion_limit: int):
    """
    Run the deep research process on the given topic.
    """
    console.print(Panel(f"[bold blue]Starting Research on:[/bold blue] [green]{topic}[/green]", title="Artistic_DeepResearch"))

    # Initialize Graph
    graph = deep_researcher_builder.compile()
    
    initial_state = {
        "user_notes": {"topic": topic},
        "today": get_today_str(),
    }

    config = {"recursion_limit": recursion_limit}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Researching...", total=None)
        
        final_report = ""
        
        # We'll stream the updates to show progress
        async for event in graph.astream(initial_state, config):
            # Checking for report generation
            if "write_final_section" in event:
                 console.print("[yellow]Writing final sections...[/yellow]")
            elif "search" in event:
                 console.print(f"[cyan]Searching web...[/cyan]")
            elif "summarize_search" in event:
                 console.print(f"[magenta]Summarizing findings...[/magenta]")
            
            # Capture final output if present
            # Depending on graph structure, we might need to look at specific keys
            pass
            
        # Get final state
        result = await graph.ainvoke(initial_state, config)
        final_report = result.get("report", "No report generated.")

        progress.update(task, completed=True)

    console.print(Panel("[bold green]Research Complete![/bold green]"))
    
    # Display Report in Console
    console.print(Markdown(final_report))
    
    # Generate Artistic HTML Report
    html_report = generate_artistic_report(final_report, {"title": f"Research: {topic}", "date": get_today_str()})
    
    filename = f"report_{topic.replace(' ', '_').lower()}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_report)
        
    console.print(f"\n[bold green]Artistic Report saved to: {filename}[/bold green]")


@app.command()
def start(
    topic: Optional[str] = typer.Option(None, "--topic", "-t", help="The research topic"),
    recursion_limit: int = typer.Option(100, "--limit", "-l", help="Max recursion steps for the graph"),
):
    """
    Start a new research session.
    """
    if not topic:
        topic = Prompt.ask("[bold yellow]What would you like to research today?[/bold yellow]")
    
    asyncio.run(run_research(topic, recursion_limit))

if __name__ == "__main__":
    app()
