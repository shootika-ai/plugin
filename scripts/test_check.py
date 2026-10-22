"""Tests for scripts/check.py: each one breaks one directory rule in a minimal passing plugin."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check  # noqa: E402

VERSION = '0.2.0'
PROMPTS = [
    'Which of my products have no model photos yet?',
    'Shoot my newest product on a model and show me the frames.',
    'How many frames do I have left this month?',
]
README_LINES = PROMPTS[:2] + ['Show me the frames from today and publish the second one.'] + PROMPTS[2:]
PROSE = ' '.join(['word'] * 50)
CODE_BLOCK = '```\n' + ' '.join(['code'] * 200) + '\n```\n'
SKILL = ('---\nname: shoot-products\ndescription: Shoot products. Use when asked to shoot.\n---\n\n'
         'Body text.\n')


def claude_manifest(**over):
    m = {'name': 'shootika', 'version': VERSION, 'description': 'Shoot on-model photos.',
         'author': {'name': 'Dimenso'}, 'license': 'MIT'}
    m.update(over)
    return m


def codex_manifest(**over):
    m = {
        'name': 'shootika', 'version': VERSION, 'description': 'Shoot on-model photos.',
        'author': {'name': 'Dimenso'}, 'skills': './skills/', 'mcpServers': './.mcp.json',
        'interface': {
            'displayName': 'Shootika', 'shortDescription': 'On-model product photos',
            'longDescription': 'Shoot on-model product photos for your store.',
            'developerName': 'Dimenso', 'category': 'Productivity', 'capabilities': ['Read', 'Write'],
            'composerIcon': './assets/icon.png', 'logo': './assets/icon.png',
            'defaultPrompt': list(PROMPTS),
            'websiteURL': 'https://shootika.com', 'supportURL': 'https://shootika.com/contact/',
            'privacyPolicyURL': 'https://shootika.com/legal/privacy/',
            'termsOfServiceURL': 'https://shootika.com/legal/terms/',
        },
        'extensions': {'com.openai': {'review': {'test_cases': {
            'positive': [{'description': f'p{i}', 'prompt': f'prompt {i}', 'tools_triggered': 'get_account',
                          'expected_behavior': 'Calls get_account.'} for i in range(5)],
            'negative': [{'description': f'n{i}', 'prompt': f'prompt {i}'} for i in range(3)],
        }}}},
    }
    m.update(over)
    return m


def readme(lines=README_LINES, prose=PROSE):
    asks = '\n'.join(f'- "{line}"' for line in lines)
    return f'# Shootika\n\n{prose}\n\n## What you can ask\n\n{asks}\n\n{CODE_BLOCK}'


def make_plugin(root: Path, *, claude=None, codex=None, readme_text=None, skill=SKILL, mcp=None):
    (root / '.claude-plugin').mkdir()
    (root / '.claude-plugin' / 'plugin.json').write_text(json.dumps(claude or claude_manifest()))
    (root / '.codex-plugin').mkdir()
    (root / '.codex-plugin' / 'plugin.json').write_text(json.dumps(codex or codex_manifest()))
    (root / '.mcp.json').write_text(json.dumps(mcp or {'mcpServers': {'shootika': {
        'type': 'http', 'url': 'https://mcp.shootika.com'}}}))
    (root / 'VERSION').write_text(VERSION + '\n')
    (root / 'README.md').write_text(readme() if readme_text is None else readme_text)
    (root / 'LICENSE').write_text('MIT\n')
    (root / 'assets').mkdir()
    (root / 'assets' / 'icon.png').write_bytes(b'\x89PNG' + b'\0' * 300 * 1024)
    (root / 'skills' / 'shoot-products').mkdir(parents=True)
    (root / 'skills' / 'shoot-products' / 'SKILL.md').write_text(skill)


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def plugin(self, **kw):
        make_plugin(self.root, **kw)
        return self.root

    def problems(self, **kw):
        return check.run(self.plugin(**kw))

    def assert_reported(self, problems, *needles):
        text = '\n'.join(problems)
        for needle in needles:
            self.assertIn(needle, text, problems)

    def test_a_complete_plugin_has_no_problems(self):
        self.assertEqual(self.problems(), [])

    def test_version_mismatch_is_reported(self):
        self.assert_reported(self.problems(claude=claude_manifest(version='0.1.9')), 'version', '0.1.9')

    def test_display_name_over_30_is_reported(self):
        codex = codex_manifest()
        codex['interface']['displayName'] = 'x' * 31
        self.assert_reported(self.problems(codex=codex), 'displayName', '30')

    def test_short_description_over_30_is_reported(self):
        codex = codex_manifest()
        codex['interface']['shortDescription'] = 'x' * 31
        self.assert_reported(self.problems(codex=codex), 'shortDescription', '30')

    def test_long_description_over_4000_is_reported(self):
        codex = codex_manifest()
        codex['interface']['longDescription'] = 'x' * 4001
        self.assert_reported(self.problems(codex=codex), 'longDescription', '4000')

    def test_unknown_category_is_reported(self):
        codex = codex_manifest()
        codex['interface']['category'] = 'Photography'
        self.assert_reported(self.problems(codex=codex), 'category', 'Photography')

    def test_four_starter_prompts_are_reported(self):
        codex = codex_manifest()
        codex['interface']['defaultPrompt'] = PROMPTS + ['Show me the frames from today and publish the second one.']
        self.assert_reported(self.problems(codex=codex), 'defaultPrompt', '3')

    def test_starter_prompt_with_mention_is_reported(self):
        codex = codex_manifest()
        codex['interface']['defaultPrompt'] = ['Ask @Shootika for frames'] + PROMPTS[1:]
        self.assert_reported(self.problems(codex=codex), 'defaultPrompt', '@')

    def test_starter_prompt_missing_from_readme_is_reported(self):
        codex = codex_manifest()
        codex['interface']['defaultPrompt'] = ['Shoot the linen dresses.'] + PROMPTS[1:]
        self.assert_reported(self.problems(codex=codex), 'What you can ask', 'Shoot the linen dresses.')

    def test_test_case_counts_other_than_5_and_3_are_reported(self):
        codex = codex_manifest()
        cases = codex['extensions']['com.openai']['review']['test_cases']
        cases['positive'].pop()
        cases['negative'].append({'description': 'n3', 'prompt': 'p'})
        self.assert_reported(self.problems(codex=codex), 'positive', '5', 'negative', '3')

    def test_positive_case_missing_expected_behavior_is_reported(self):
        codex = codex_manifest()
        del codex['extensions']['com.openai']['review']['test_cases']['positive'][2]['expected_behavior']
        self.assert_reported(self.problems(codex=codex), 'expected_behavior')

    def test_skill_without_skill_md_is_reported(self):
        root = self.plugin()
        (root / 'skills' / 'empty').mkdir()
        self.assert_reported(check.run(root), 'skills/empty', 'SKILL.md')

    def test_skill_name_not_matching_folder_is_reported(self):
        self.assert_reported(self.problems(skill=SKILL.replace('name: shoot-products', 'name: shoot')),
                             'shoot-products', 'name')

    def test_skill_description_over_1024_is_reported(self):
        long = SKILL.replace('Use when asked to shoot.', 'x' * 1030)
        self.assert_reported(self.problems(skill=long), 'description', '1024')

    def test_skill_with_metadata_field_is_reported(self):
        self.assert_reported(self.problems(skill=SKILL.replace('---\n\n', 'metadata: x\n---\n\n', 1)),
                             'metadata')

    def test_combined_skill_name_over_64_is_reported(self):
        root = self.plugin()
        name = 'a' * 60
        (root / 'skills' / name).mkdir()
        (root / 'skills' / name / 'SKILL.md').write_text(SKILL.replace('shoot-products', name))
        self.assert_reported(check.run(root), name, '64')

    def test_orphan_reference_file_is_reported(self):
        root = self.plugin()
        (root / 'skills' / 'shoot-products' / 'references').mkdir()
        (root / 'skills' / 'shoot-products' / 'references' / 'x.md').write_text('x')
        self.assert_reported(check.run(root), 'references/x.md', 'mention')

    def test_missing_reference_file_is_reported(self):
        self.assert_reported(self.problems(skill=SKILL + 'See references/gone.md.\n'), 'references/gone.md')

    def test_reference_path_case_mismatch_is_reported(self):
        root = self.plugin(skill=SKILL + 'See references/Store-Types.md.\n')
        (root / 'skills' / 'shoot-products' / 'references').mkdir()
        (root / 'skills' / 'shoot-products' / 'references' / 'store-types.md').write_text('x')
        problems = check.run(root)
        self.assert_reported(problems, 'references/Store-Types.md')
        self.assert_reported(problems, 'references/store-types.md')

    def test_readme_under_40_prose_words_is_reported(self):
        short = '# Shootika\n\nfive prose words only here\n\n' + CODE_BLOCK  # 200 words, all in a code block
        self.assert_reported(self.problems(readme_text=short), 'README', '40')

    def test_em_dash_in_readme_skill_or_manifest_is_reported(self):
        with self.subTest('readme'):
            self.assert_reported(self.problems(readme_text=readme(prose=PROSE + ' a — b')), 'README.md', 'em-dash')
        self.setUp()
        with self.subTest('skill'):
            self.assert_reported(self.problems(skill=SKILL + 'a — b\n'), 'SKILL.md', 'em-dash')
        self.setUp()
        with self.subTest('manifest'):
            self.assert_reported(self.problems(claude=claude_manifest(description='a — b')),
                                 'plugin.json', 'em-dash')

    def test_stray_system_file_is_reported(self):
        root = self.plugin()
        (root / 'skills' / '.DS_Store').write_bytes(b'\0')
        self.assert_reported(check.run(root), '.DS_Store')

    def test_non_image_file_over_256_kib_is_reported(self):
        root = self.plugin()
        (root / 'skills' / 'shoot-products' / 'big.md').write_text('x' * (256 * 1024 + 1))
        self.assert_reported(check.run(root), 'big.md', '256')

    def test_mcp_server_without_https_or_type_http_is_reported(self):
        self.assert_reported(self.problems(mcp={'mcpServers': {'s': {'type': 'sse', 'url': 'http://x'}}}),
                             '.mcp.json')

    def test_main_returns_1_with_problems_and_0_without(self):
        root = self.plugin()
        cwd = os.getcwd()
        try:
            os.chdir(root)
            self.assertEqual(check.main(), 0)
            (root / 'skills' / '.DS_Store').write_bytes(b'\0')
            self.assertEqual(check.main(), 1)
        finally:
            os.chdir(cwd)


if __name__ == '__main__':
    unittest.main()
