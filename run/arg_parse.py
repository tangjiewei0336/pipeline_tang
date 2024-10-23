import argparse

from schematic.print_on_instantiate import debug_output


@debug_output("陈老师别卷了")
def parse_args():
    parser = argparse.ArgumentParser(description='Run the pipeline with specified file(s).')
    
    # both
    parser.add_argument('--filename', required=True, help='Path relative to input folder of the input file')
    parser.add_argument('--workflow', required=False, default='generation', help='Workflow to run')
    parser.add_argument('--skip', required=False, default=0, help='Number of components to skip')
    parser.add_argument('--llm', required=False, default='qwen', help='Base model to use')
    
    # generation
    parser.add_argument('--strategy', required=False, default='direct', help='Strategy to cluster summary results, direct or hierarchical')
    parser.add_argument('--level', required=False, default=0, help='Level of cluster results to generate xmind')
    
    # validation
    parser.add_argument('--xmind_type', required=False, default='llm', help='Type of Xmind to evaluate, llm or human')
    parser.add_argument('--threshold', required=False, default=60.0, help='Threshold of completeness scores')
    
    return parser.parse_args()


args = parse_args()
