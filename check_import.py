#!/usr/bin/env python3
import ast
import sys
from pathlib import Path
from typing import Set

# Стандартная библиотека (не требует установки)
STDLIB = {
    "sys", "os", "re", "json", "typing", "pathlib", "ast", "collections",
    "itertools", "functools", "math", "random", "datetime", "time"
}

def extract_imports(file_path: Path) -> Set[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return set()
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split('.')[0]
                imports.add(root)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root = node.module.split('.')[0]
                imports.add(root)
    return imports

def main():
    src_dir = Path("src")
    req_file = Path("requirements.txt")
    if not src_dir.exists():
        print("Папка src/ не найдена")
        return 1
    if not req_file.exists():
        print("requirements.txt не найден")
        return 1

    all_imports = set()
    for py_file in src_dir.glob("*.py"):
        all_imports.update(extract_imports(py_file))

    required = {imp for imp in all_imports if imp not in STDLIB}

    with open(req_file) as f:
        installed = set()
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            pkg = line.split('==')[0].split('>=')[0].split('<')[0].strip()
            installed.add(pkg)

    # Игнорируем dev-инструменты
    dev_tools = {"mypy", "flake8", "black", "pip_check_reqs"}
    installed -= dev_tools

    missing = required - installed
    if missing:
        print("Отсутствуют в requirements.txt:")
        for p in sorted(missing):
            print(f"   - {p}")
        return 1
    print("Все импорты соответствуют requirements.txt")
    return 0

if __name__ == "__main__":
    sys.exit(main())