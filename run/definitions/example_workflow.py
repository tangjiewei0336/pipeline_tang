from res.input import get_input_uri
from res.output import get_output_folder, get_output_uri
from run.arg_parse import args
from schematic.checkpoint import ScriptWithArgs

example_output_folder = get_output_folder("1_output")

# 可以同时使用两种形式
EXAMPLE_WORKFLOW = [
    ScriptWithArgs(
        script_name='example_script.py',
        args={
            "input_file": get_input_uri(args.filename),
            "output_folder": example_output_folder
        },
        cache_uri= get_output_folder("1_output"),
        cached=True
    )
]
