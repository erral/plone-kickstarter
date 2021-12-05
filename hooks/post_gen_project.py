# post generation step 1: rename requirement*.txt if needed
from pathlib import Path

cwd = Path.cwd()

if "{{ cookiecutter.mode }}" == "standalone":
    current_requirements_file = cwd / "requirements_barebone.txt"
    renamed_requirements_file = cwd / "requirements.txt"
    current_requirements_file.rename(renamed_requirements_file)
