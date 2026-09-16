"""Cross-platform clean: remove build artefacts and cache directories."""

import os
import shutil

NAMES = {
    'site',
    '.cache',
    '.private',
    '.pytest_cache',
    '.ruff_cache',
    '.mypy_cache',
    '__pycache__',
    'htmlcov',
}

for root, dirs, _ in os.walk('.', topdown=True):
    dirs[:] = [d for d in dirs if d not in ('.venv', '.venvs', '.git')]
    for d in list(dirs):
        if d in NAMES:
            shutil.rmtree(os.path.join(root, d), ignore_errors=True)
            dirs.remove(d)

shutil.rmtree('coverage', ignore_errors=True)
print('Done.')
