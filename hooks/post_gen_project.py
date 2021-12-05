# post generation step 1: rename requirement*.txt if needed
from pathlib import Path

cwd = Path.cwd()

requirements_out = "{{ cookiecutter.requirements_out }}"
if requirements_out != "requirements_barebone.txt":
    current_requirements_file = cwd / "requirements_barebone.txt"
    renamed_requirements_file = cwd / "{{ cookiecutter.requirements_out }}"
    current_requirements_file.rename(renamed_requirements_file)
