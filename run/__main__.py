from run.arg_parse import args
from run.definitions.example_workflow import EXAMPLE_WORKFLOW
from schematic.pipeline import run_pipeline

if __name__ == "__main__":
    # TODO： 从命令行参数解析配置文件
    to_skip = int(args.skip)
    workflow = str(args.workflow).lower()
    if workflow == 'example':
        scripts_with_args = EXAMPLE_WORKFLOW
    else:
        raise ValueError("Invalid workflow name.")
    if to_skip < 0:
        raise ValueError("Skip number should be non-negative.")
    run_pipeline(scripts_with_args[to_skip:])
