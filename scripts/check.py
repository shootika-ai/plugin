#!/usr/bin/env python3
"""The directory rules this plugin must keep: Anthropic's plugin directory and OpenAI's plugin
directory, as encoded in docs/superpowers/specs/2026-10-22-directory-listing-design.md.

Run from the repository root: `python3 scripts/check.py`. Prints one problem per line and exits 1
when there are any. No dependencies beyond the standard library, so CI and a laptop run the same
thing. `claude plugin validate --strict` covers what this does not: manifest schema and paths.
"""
import json
import re
import sys
from pathlib import Path

README_WORDS = 40
OPENAI_CATEGORIES = [
    'Productivity', 'Creativity', 'Developer Tools', 'Business & Operations', 'Data & Analytics',
    'Communication', 'Education & Research', 'Security', 'Finance', 'Healthcare', 'Travel',
    'Entertainment', 'Other',
]
OPENAI_LIMITS = {'displayName': 30, 'shortDescription': 30, 'longDescription': 4000,
                 'developerName': 80, 'defaultPrompt': 128}
MAX_STARTER_PROMPTS = 3
POSITIVE_CASES, NEGATIVE_CASES = 5, 3
POSITIVE_FIELDS = ('description', 'prompt', 'tools_triggered', 'expected_behavior')
NEGATIVE_FIELDS = ('description', 'prompt')
SKILL_DESCRIPTION_MAX = 1024
SKILL_FULL_NAME_MAX = 64
NON_IMAGE_MAX_BYTES = 256 * 1024
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.woff', '.woff2', '.ttf', '.otf'}
STRAY_NAMES = {'.DS_Store', 'Thumbs.db', '__MACOSX'}
SKIP_DIRS = {'.git', '.superpowers', 'dist', '__pycache__', 'node_modules'}
EM_DASH = '—'
TEXT_SUFFIXES = {'.md', '.json', '.yaml', '.yml', '.txt'}


def _read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def _front_matter(text: str) -> dict | None:
    """The `key: value` pairs between the first two `---` lines, or None when there is no front matter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    fields = {}
    for line in lines[1:]:
        if line.strip() == '---':
            return fields
        key, sep, value = line.partition(':')
        if sep and key.strip():
            fields[key.strip()] = value.strip()
    return None


def _prose_words(markdown: str) -> int:
    without_code = re.sub(r'```.*?```', '', markdown, flags=re.S)
    return len(without_code.split())


def _ask_lines(readme: str) -> list[str]:
    """The quoted sentences under the "What you can ask" heading."""
    match = re.search(r'^##\s+What you can ask\s*$(.*?)(?=^##\s|\Z)', readme, flags=re.M | re.S)
    if not match:
        return []
    return [m.group(1) for m in re.finditer(r'^-\s*"(.+?)"\s*$', match.group(1), flags=re.M)]


# ---- Rule families

def check_versions(root: Path) -> list[str]:
    version = (root / 'VERSION').read_text().strip()
    problems = []
    for manifest in ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
        found = _read_json(root / manifest).get('version')
        if found != version:
            problems.append(f'{manifest}: version {found!r} does not match VERSION {version!r}')
    return problems


def check_openai_interface(root: Path, readme: str) -> list[str]:
    manifest = '.codex-plugin/plugin.json'
    interface = _read_json(root / manifest).get('interface', {})
    problems = []
    for field in ('displayName', 'shortDescription', 'longDescription', 'developerName'):
        value = interface.get(field) or ''
        if len(value) > OPENAI_LIMITS[field]:
            problems.append(f'{manifest}: interface.{field} is {len(value)} characters, the limit is {OPENAI_LIMITS[field]}')
    category = interface.get('category')
    if category not in OPENAI_CATEGORIES:
        problems.append(f'{manifest}: interface.category {category!r} is not one of OpenAI\'s categories')
    prompts = interface.get('defaultPrompt') or []
    if isinstance(prompts, str):
        prompts = [prompts]
    if len(prompts) > MAX_STARTER_PROMPTS:
        problems.append(f'{manifest}: interface.defaultPrompt has {len(prompts)} entries, at most {MAX_STARTER_PROMPTS} are allowed')
    asks = _ask_lines(readme)
    for prompt in prompts:
        if len(prompt) > OPENAI_LIMITS['defaultPrompt']:
            problems.append(f'{manifest}: interface.defaultPrompt {prompt!r} is over {OPENAI_LIMITS["defaultPrompt"]} characters')
        if '@' in prompt:
            problems.append(f'{manifest}: interface.defaultPrompt {prompt!r} contains an @ mention')
        if prompt not in asks:
            problems.append(f'{manifest}: interface.defaultPrompt {prompt!r} is not a line under "What you can ask" in README.md')
    return problems


def check_openai_test_cases(root: Path) -> list[str]:
    manifest = '.codex-plugin/plugin.json'
    cases = (_read_json(root / manifest).get('extensions', {}).get('com.openai', {})
             .get('review', {}).get('test_cases', {}))
    problems = []
    for kind, count, fields in (('positive', POSITIVE_CASES, POSITIVE_FIELDS),
                                ('negative', NEGATIVE_CASES, NEGATIVE_FIELDS)):
        entries = cases.get(kind) or []
        if len(entries) != count:
            problems.append(f'{manifest}: review.test_cases.{kind} has {len(entries)} cases, exactly {count} are required')
        for i, entry in enumerate(entries):
            for field in fields:
                if not entry.get(field):
                    problems.append(f'{manifest}: review.test_cases.{kind}[{i}] is missing {field}')
    return problems


def check_skills(root: Path, plugin_name: str) -> list[str]:
    problems = []
    skills_dir = root / 'skills'
    for folder in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        rel = f'skills/{folder.name}'
        skill_md = folder / 'SKILL.md'
        if not skill_md.is_file():
            problems.append(f'{rel}: no SKILL.md')
            continue
        text = skill_md.read_text(encoding='utf-8')
        fields = _front_matter(text)
        if fields is None:
            problems.append(f'{rel}/SKILL.md: no front matter')
            continue
        if fields.get('name') != folder.name:
            problems.append(f'{rel}/SKILL.md: name {fields.get("name")!r} does not match the folder {folder.name!r}')
        description = fields.get('description', '')
        if not description:
            problems.append(f'{rel}/SKILL.md: no description')
        elif len(description) > SKILL_DESCRIPTION_MAX:
            problems.append(f'{rel}/SKILL.md: description is {len(description)} characters, the limit is {SKILL_DESCRIPTION_MAX}')
        for extra in sorted(set(fields) - {'name', 'description'}):
            problems.append(f'{rel}/SKILL.md: front matter field {extra!r} is not portable (only name and description)')
        full_name = f'{plugin_name}:{folder.name}'
        if len(full_name) > SKILL_FULL_NAME_MAX:
            problems.append(f'{rel}: {full_name!r} is {len(full_name)} characters, the limit is {SKILL_FULL_NAME_MAX}')
        problems.extend(_check_references(folder, rel, text))
    return problems


def _check_references(folder: Path, rel: str, skill_text: str) -> list[str]:
    problems = []
    on_disk = sorted(p.relative_to(folder).as_posix() for p in (folder / 'references').glob('*') if p.is_file())
    mentioned = sorted(set(re.findall(r'references/[A-Za-z0-9_.\-]+\.md', skill_text)))
    for path in on_disk:
        if path not in mentioned:
            problems.append(f'{rel}/{path}: no mention of it in {rel}/SKILL.md')
    for path in mentioned:
        if path not in on_disk:
            problems.append(f'{rel}/SKILL.md mentions {path}, which does not exist with that exact name')
    return problems


def check_readme(readme: str) -> list[str]:
    words = _prose_words(readme)
    if words < README_WORDS:
        return [f'README.md: {words} words outside code blocks, the directory needs at least {README_WORDS}']
    return []


def check_mcp(root: Path) -> list[str]:
    problems = []
    for name, server in _read_json(root / '.mcp.json').get('mcpServers', {}).items():
        if server.get('type') != 'http':
            problems.append(f'.mcp.json: server {name!r} must have type "http"')
        if not str(server.get('url', '')).startswith('https://'):
            problems.append(f'.mcp.json: server {name!r} must have an absolute https:// url')
    return problems


def _text_content(path: Path) -> str:
    """A file's text as a reader sees it: JSON is decoded first, so an escaped `\\u2014` counts too."""
    text = path.read_text(encoding='utf-8', errors='replace')
    if path.suffix.lower() == '.json':
        try:
            return json.dumps(json.loads(text), ensure_ascii=False)
        except ValueError:
            return text
    return text


def check_files(root: Path) -> list[str]:
    problems = []
    for path in sorted(root.rglob('*')):
        parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        rel = path.relative_to(root).as_posix()
        if path.name in STRAY_NAMES:
            problems.append(f'{rel}: a system file the directory refuses')
            continue
        if path.is_symlink():
            problems.append(f'{rel}: a symbolic link')
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_SUFFIXES and path.stat().st_size > NON_IMAGE_MAX_BYTES:
            problems.append(f'{rel}: {path.stat().st_size} bytes, non-image files must stay under 256 KiB')
        if path.suffix.lower() in TEXT_SUFFIXES and EM_DASH in _text_content(path):
            problems.append(f'{rel}: contains an em-dash')
    return problems


def run(root: Path) -> list[str]:
    root = Path(root)
    readme = (root / 'README.md').read_text(encoding='utf-8') if (root / 'README.md').is_file() else ''
    plugin_name = _read_json(root / '.claude-plugin' / 'plugin.json').get('name', '')
    problems = []
    problems += check_versions(root)
    problems += check_openai_interface(root, readme)
    problems += check_openai_test_cases(root)
    problems += check_skills(root, plugin_name)
    problems += check_readme(readme)
    problems += check_mcp(root)
    problems += check_files(root)
    return problems


def main() -> int:
    problems = run(Path.cwd())
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
