#!/usr/bin/env python3
"""Compatibility checks; generated values are never retained in test artifacts."""
from pathlib import Path
import re
import subprocess
import sys

command = ['./word-salad'] if sys.argv[1:] == ['--local'] else ['snap', 'run', 'word-salad']
help_result = subprocess.run(command + ['--help'], capture_output=True, text=True, timeout=10, check=True)
assert 'Usage: word-salad' in help_result.stdout
assert subprocess.run(command + ['--invalid'], capture_output=True, timeout=10).returncode != 0
pattern = re.compile(r'[A-Z][a-z]{2}[0-9][A-Z][a-z]{2}[!.?](?:[A-Z][a-z]{2}){2}\n')
for _ in range(20):
    result = subprocess.run(command, capture_output=True, text=True, timeout=10, check=True)
    assert pattern.fullmatch(result.stdout), 'Unexpected generated output format'
    assert not result.stderr, 'Unexpected stderr output'
Path('artifacts').mkdir(exist_ok=True)
Path('artifacts/smoke-test.log').write_text('Help, invalid argument, and 20 generation format checks passed. No entropy claim.\n')
print('Word Salad compatibility checks passed')
