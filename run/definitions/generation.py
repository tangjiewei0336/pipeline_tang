import os

from res.input import get_input_uri
from res.output import get_output_folder, get_output_uri
from run.arg_parse import args
from schematic.checkpoint import ScriptWithArgs

function_name = os.path.splitext(args.filename)[0]
llm = args.llm
split_results_folder = get_output_folder(function_name, llm) / "1_split_results"
table_explained_folder = get_output_folder(function_name, llm) / "2_table_explained"
summary_results_folder = get_output_folder(function_name, llm) / "3_summary_results"
cluster_results_folder = get_output_folder(function_name, llm) / "4_cluster_results"
llm_xmind_file = get_output_folder(function_name, llm) / f"{function_name}_llm.xmind"

# 可以同时使用两种形式
GENERATION_WORKFLOW = [
    ScriptWithArgs(
        script_name='direct_extract_to_markdown.py',
        args={
            "input_file": get_input_uri(args.filename),
            "output_folder": get_output_folder(function_name, llm)
        },
        cache_uri=get_output_folder(function_name, llm),
        cached=True
    ),
    ScriptWithArgs(
        script_name='split_into_chunks.py',
        args={
            "input_file": get_output_uri(function_name, llm, args.filename.replace(".pdf", ".md")),
            "output_folder": split_results_folder
        },
        cache_uri=split_results_folder,
        cached=True
    ),
    ScriptWithArgs(
        script_name='paraphrase_tables.py',
        args={"input_folder": split_results_folder,
              "output_folder": table_explained_folder,
              "llm": args.llm},
        enabled=True,
        cached=True,
        cache_uri=table_explained_folder
    ),
    ScriptWithArgs(
        script_name='summarize_key_points.py',
        args={
            "input_folder": table_explained_folder,
            "output_folder": summary_results_folder,
            "llm": args.llm
        },
        cached=True,
        cache_uri=summary_results_folder
    ),
    ScriptWithArgs(
        script_name='merge_summaries.py',
        args={
            "input_folder": summary_results_folder,
            "output_folder": cluster_results_folder,
            "strategy": args.strategy,
            "llm": args.llm
        },
        cached=True,
        cache_uri=cluster_results_folder
    ),
    ScriptWithArgs(
        script_name='generate_xmind.py',
        args={
            "input_folder": cluster_results_folder,
            "output_file": llm_xmind_file,
            "level": int(args.level)
        },
        cached=True,
        cache_uri=llm_xmind_file
    )
]
