"""Bounded Skill context selection and linked-contract validation.

Execution reads only explicitly selected references. Contract-module expansion is
for repository validation, not permission to load every reference into a task.
This module neither grants approval nor executes any Skill instruction.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import re

_LINK = re.compile(r'\[[^\]\n]*\]\((references/[^\s)]+\.md)\)')
_MODULE = re.compile(r'<!-- contract-module: ([^\s]+) -->')


def load_skill_context(skill_file: Path, references: tuple[str, ...] | list[str] = ()) -> dict[Path, str]:
    """Return complete requested documents; never expand their child references."""
    skill_file = Path(skill_file).resolve(strict=True)
    body = skill_file.read_text(encoding='utf-8')
    links = set(_LINK.findall(body))
    pack = {skill_file: body}
    reference_root = (skill_file.parent / 'references').resolve()
    if references and not reference_root.is_relative_to(skill_file.parent):
        raise ValueError('Skill reference directory escapes its package')
    for name in references:
        relative = PurePosixPath(name)
        if name not in links or relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
            raise ValueError(f'Unlinked or unsafe Skill reference: {name}')
        path = (skill_file.parent / name).resolve(strict=True)
        if not path.is_relative_to(reference_root) or not path.is_file():
            raise ValueError(f'Skill reference escapes its reference directory: {name}')
        if path not in pack:
            pack[path] = path.read_text(encoding='utf-8')
    return pack


def read_skill_contract(skill_file: Path) -> str:
    """Validation-only union of the entrypoint and explicitly declared fragments."""
    body = Path(skill_file).read_text(encoding='utf-8')
    modules = _MODULE.findall(body)
    return '\n'.join(load_skill_context(skill_file, modules).values())
