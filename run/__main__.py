from run.arg_parse import args
from run.definitions.generation import GENERATION_WORKFLOW
from run.definitions.graphing import GRAPHING_WORKFLOW
from run.definitions.validation import VALIDATION_WORKFLOW
from schematic.pipeline import run_pipeline

if __name__ == "__main__":
    # TODO： 从命令行参数解析配置文件
    to_skip = int(args.skip)
    workflow = str(args.workflow).lower()
    if workflow == 'generation':
        scripts_with_args = GENERATION_WORKFLOW
    elif workflow == 'validation':
        scripts_with_args = VALIDATION_WORKFLOW
    elif workflow == 'graphing':
        scripts_with_args = GRAPHING_WORKFLOW
    else:
        raise ValueError("Invalid workflow name.")
    if to_skip < 0:
        raise ValueError("Skip number should be non-negative.")
    run_pipeline(scripts_with_args[to_skip:])
