import os
import time

from res.output import get_output_folder
from run.arg_parse import args
from run.definitions.generation import GENERATION_WORKFLOW, split_results_folder, llm_xmind_file
from schematic.checkpoint import ScriptWithArgs

function_name = os.path.splitext(args.filename)[0]
llm = args.llm
xmind_type = args.xmind_type

if xmind_type == 'llm':
    xmind_file = llm_xmind_file
elif xmind_type == 'human':
    xmind_file = get_output_folder(function_name, llm) / f"{function_name}_human.xmind"
else:
    raise ValueError("Invalid xmind type.")
    
xmind_info_zh_folder = get_output_folder(function_name, llm) / f"5_xmind_info_{xmind_type}"
score_output_folder = get_output_folder(function_name, llm) / f"6_scores_{xmind_type}" / f"{time.time()}"

VALIDATION_WORKFLOW = [
    *GENERATION_WORKFLOW,
    ScriptWithArgs(
        script_name='walk_xmind_tree.py',
        cached=True,
        cache_uri=xmind_info_zh_folder,
        args={
            "input_file": xmind_file,
            "output_folder": xmind_info_zh_folder,
            "xmind_type": str(args.xmind_type).lower()
        }
    ),
    ScriptWithArgs(
        script_name='scores/calculate_accuracy_score_old.py',
        args={
            "xmind_folder": xmind_info_zh_folder,  # rag - retrieve
            "fds_md_folder": split_results_folder,
            "output_file":  score_output_folder / "accuracy_score.jsonl",
            "llm": args.llm
        },
        enabled=False
    ),
    ScriptWithArgs(
        script_name='scores/calculate_accuracy_score.py',
        args={
            "xmind_chunk_folder": xmind_info_zh_folder,
            "text_chunk_folder": split_results_folder,
            "output_file": score_output_folder / "purity_score.txt",
            "llm": args.llm
        },
        enabled=True
    ),
    ScriptWithArgs(
        script_name='scores/calculate_completeness_score.py',
        args={
            "xmind_chunk_folder": xmind_info_zh_folder,
            "text_chunk_folder": split_results_folder,
            "output_folder": score_output_folder,
            "llm": args.llm,
            "threshold": args.threshold,
        },
        enabled=False
    )
]
