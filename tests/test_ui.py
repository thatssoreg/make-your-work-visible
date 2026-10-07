"""Compatibility entry point for the browser suite."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('test_native.py')),run_name='__main__')
