"""Allow running whatsup as ``python3 -m whatsup``."""

import sys
import os

# Ensure the project root (parent of whatsup/) is on sys.path so that the
# top-level cli module is importable even when not pip-installed.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from cli import main

main()
