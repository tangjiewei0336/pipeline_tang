import datetime
import pathlib
from pathlib import Path

script_path = Path(__file__).resolve()
script_dir = script_path.parent


def get_output_uri(function_name: str, llm: str, filename: str) -> pathlib.Path:
    return get_output_folder(function_name, llm) / filename


def get_output_parent_folder() -> pathlib.Path:
    return script_dir.parent / "output"


def get_output_folder(function_name: str, llm: str, timestamp: bool = False) -> pathlib.Path:
    # ymdhms
    if timestamp:
        output_folder = script_dir.parent / "output" / f"{function_name}_{llm}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    else:
        output_folder = script_dir.parent / "output" / f"{function_name}_{llm}"
    
    output_folder.mkdir(parents=True, exist_ok=True)

    return output_folder
