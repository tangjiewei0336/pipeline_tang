import os

from res.input import get_input_uri
from res.output import get_output_folder
from run.arg_parse import args
from run.definitions.generation import cluster_results_folder
from schematic.checkpoint import ScriptWithArgs

function_name = os.path.splitext(args.filename)[0]
llm = args.llm if args.llm else "qwen"

level_0_json = cluster_results_folder / "level_0"
cypher_output_folder = get_output_folder(function_name, llm) / "6_leaf_cypher"
idl_results_folder = get_output_folder(function_name, llm) / "7_idl_results"
idl_code_folder = get_output_folder(function_name, llm) / "8_idl_code"

GRAPHING_WORKFLOW = [
    ScriptWithArgs(
        script_name='direct_extract_to_markdown.py',
        args={
            "input_file": get_input_uri(function_name + "_idl.pdf"),
            "output_folder": idl_results_folder
        },
        cached=True,
        cache_uri=idl_results_folder
    ),
    ScriptWithArgs(
        script_name='extract_idl_signals.py',
        args={
            "input_file": idl_results_folder / f"{function_name}_idl.md",
            "output_folder": idl_code_folder,
            "llm": llm
        },
        cached=True,
        cache_uri= idl_code_folder
    ),
    ScriptWithArgs(
        script_name='xmind_to_neo.py',
        args={
            "json_input_folder": level_0_json,
            "cypher_output_folder": cypher_output_folder
        }
    )
]
