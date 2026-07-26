"""Log file repository helpers."""

from pathlib import Path


def list_logs(log_dir="logs"):
    """Return the sorted list of log file names in the log directory."""
    path = Path(log_dir)
    if not path.exists():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_file())


def load_logs(logs, log_dir="logs"):
    """Return the contents of each log file as a nested list of lines."""
    path = Path(log_dir)
    contents = []
    for log_file in logs:
        file_path = path / log_file
        if not file_path.exists():
            contents.append([])
            continue
        with file_path.open(encoding="utf-8") as handle:
            contents.append(handle.readlines())
    return contents
