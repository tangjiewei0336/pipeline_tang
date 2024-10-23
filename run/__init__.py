import os
import pathlib

os.environ['PATH'] = os.path.abspath(os.path.dirname(__file__)) + os.pathsep + os.environ.get('PATH', '')
os.environ['PYTHONPATH'] = os.path.abspath(os.path.dirname(__file__)) + os.pathsep + os.environ.get('PYTHONPATH', '')
