import subprocess
import sys
from time import sleep
from typing import Tuple, Dict, List

from schematic.logger import global_logger
from schematic.checkpoint import ScriptWithArgs

def run_script(script_name: str, args: Dict[str, str] = None) -> bool:
    if args is None:
        args = {}
    cmd_args = [f"--{key}={value}" for key, value in args.items()] + [f"--script={script_name}"]
    cmd = ['python', 'schematic/code_runner.py'] + cmd_args

    percent = 0
    avg_step_time = "--"
    remaining_time = "--"

    try:
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        info_str = ""
        sys.stdout.write("\n")
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if "{percent}" in output:
                percent = output.lstrip('{percent}').strip('\n')
                print(f"\rProgress: {percent}%  Speed: {avg_step_time}s/it  ETA: {remaining_time}secs", end="")
            elif "{avg_step_time}" in output:
                avg_step_time = output.lstrip('{avg_step_time}').strip('\n')
                print(f"\rProgress: {percent}%  Speed: {avg_step_time}s/it  ETA: {remaining_time}secs", end="")
            elif "{remaining_time}" in output:
                remaining_time = output.lstrip('{remaining_time}').strip('\n')
                print(f"\rProgress: {percent}%  Speed: {avg_step_time}s/it  ETA: {remaining_time}secs", end="")
            elif "{log}" in output:
                global_logger.log(output.lstrip('{log}').strip('\n').replace('\x10','\n'), level="WARNING")
            else:
                info_str += output


        sys.stdout.write(f"\r")
        stderr = process.communicate()[1]
        if process.returncode != 0:
            global_logger.log(f"Error occurred while running {script_name}:\n{stderr}", level="CRITICAL")
            sys.stdout.flush()
            sleep(1)
            ans = input(f"A critical or unhandled error occurred while running {script_name}.\n"
                        f"However, this program can try to run rest of the workflow. \nDo you wish to continue? (y/n): ")
            if ans not in ["y", "Y"]:
                return True
            else:
                return False
        else:
            global_logger.log(f"Finished running {script_name}.")
            if info_str != "":
                global_logger.log(f"Info from {script_name} :\n {info_str}")

    except Exception as e:
        global_logger.log(f"Exception occurred while running {script_name}: {str(e)}", level="CRITICAL")
        ans = input("A critical or unhandled error occurred while running {script_name}. Continue? (y/n): ")
        if ans not in ["y", "Y"]:
            return True
        else:
            return False


def run_pipeline(scripts_with_args: List[Tuple[str, Dict[str, str]] | ScriptWithArgs]):
    total_scripts = len(scripts_with_args)
    current_script_index = 0  # 用于记录当前执行的脚本序号

    for script, args in scripts_with_args:
        current_script_index += 1
        if script == "noscript":
            continue
        if script == "exit":
            break

        global_logger.log(f"Running script {current_script_index}/{total_scripts}: {script}...")
        terminate_sign = run_script("run/workflow/" + script, args)
        if terminate_sign:
            global_logger.log(f"Workflow terminated by user at script {current_script_index}.")
            sys.exit(0)
