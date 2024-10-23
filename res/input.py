from pathlib import Path

script_path = Path(__file__).resolve()
script_dir = script_path.parent


def get_input_uri(filename):
    return script_dir.parent / "input" / filename


if __name__ == '__main__':
    print(get_input_uri('input.txt'))
