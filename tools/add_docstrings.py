"""対象Pythonファイルへ不足しているdocstringを自動付与するユーティリティ。"""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "accounts", ROOT / "dish", ROOT / "gourmet"]
EXTRA_FILES = [ROOT / "manage.py"]


def iter_targets() -> list[Path]:
    """docstring付与対象のファイル一覧を返す。"""
    files: list[Path] = []
    for base in TARGET_DIRS:
        for path in base.rglob("*.py"):
            if "migrations" in path.parts:
                continue
            if path.name == "__init__.py":
                continue
            files.append(path)
    for path in EXTRA_FILES:
        if path.exists():
            files.append(path)
    return sorted(set(files))


def leading_spaces(text: str) -> str:
    """行頭の空白を返す。"""
    return text[: len(text) - len(text.lstrip(" "))]


def add_missing_docstrings(path: Path) -> bool:
    """単一ファイルに不足docstringを追加し、変更有無を返す。"""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    modified = False

    insertions: list[tuple[int, str]] = []

    if ast.get_docstring(tree) is None:
        module_name = path.stem
        insertions.append((1, f'"""{module_name} モジュール。"""'))

    for node in ast.walk(tree):
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.body:
            continue
        if ast.get_docstring(node) is not None:
            continue

        first_body = node.body[0].lineno
        base_indent = leading_spaces(lines[first_body - 1])
        if isinstance(node, ast.ClassDef):
            message = f'"""{node.name} の責務を表すクラス。"""'
        else:
            message = f'"""{node.name} を実行する。"""'
        insertions.append((first_body, f"{base_indent}{message}"))

    for line_no, text in sorted(insertions, key=lambda x: x[0], reverse=True):
        lines.insert(line_no - 1, text)
        modified = True

    if modified:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return modified


def main() -> None:
    """エントリーポイント。"""
    changed = 0
    for target in iter_targets():
        if add_missing_docstrings(target):
            changed += 1
            print(f"updated: {target.relative_to(ROOT)}")
    print(f"changed_files={changed}")


if __name__ == "__main__":
    main()
