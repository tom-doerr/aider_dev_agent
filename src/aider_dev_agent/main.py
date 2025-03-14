import click
from .task_manager import TaskManager
from .report_parser import ReportParser
from pathlib import Path

@click.command()
@click.option("--workers", default=4, help="Number of parallel worker processes")
@click.option("--report", default="report.md", type=click.Path(exists=True), 
             help="Path to the report file containing tasks")
def cli(workers, report):
    """Run parallel AI analysis tasks with dependency management"""
    # Validate report file exists
    if not Path(report).exists():
        raise click.BadParameter(f"Report file {report} not found")
    
    # Parse tasks from report
    parser = ReportParser(report)
    tasks = parser.parse()
    
    # Initialize task manager with conflict detection
    manager = TaskManager(worker_count=workers)
    
    # Add parsed tasks with dependency resolution
    for task in tasks.values():
        manager.add_task(task)
    
    # Start processing with proper cleanup
    try:
        manager.start_workers()
        manager.monitor_progress()
        click.echo("\nAll tasks completed successfully!")
    except KeyboardInterrupt:
        click.echo("\nAborted by user. Cleaning up...")
        manager.shutdown()
    finally:
        manager.generate_final_report(report)

if __name__ == "__main__":
    cli()
