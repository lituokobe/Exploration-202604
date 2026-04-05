from pathlib import Path

current_file = Path(__file__).resolve()
project_dir = current_file.parent.parent

LOG_PATH = project_dir / "logs"
ENV_PATH = project_dir / ".env"