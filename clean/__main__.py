import shutil
import sys

from res.output import get_output_parent_folder

folder = get_output_parent_folder()
if not folder.exists():
    folder.mkdir()
    sys.exit(0)
# clear all content
for item in folder.iterdir():
    if item.is_file():
        item.unlink()
    elif item.is_dir():
        shutil.rmtree(item)
