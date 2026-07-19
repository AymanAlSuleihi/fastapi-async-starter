from src.workers.settings import broker


@broker.task(task_name="example_task")
async def example_task(message: str) -> str:
    """Example task."""
    return f"Processed: {message}"
