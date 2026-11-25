"""Regression coverage for non-destructive output preparation."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from utils.output_directory import prepare_output_directory, validate_output_directory

ROOT = Path(__file__).resolve().parents[1]


class OutputDirectoryTests(unittest.TestCase):
    def test_protected_paths(self):
        for path in (Path('/'), Path.home(), ROOT, ROOT.parent, ROOT / 'tools',
                     ROOT / 'utils' / 'new', Path('/etc/new-output')):
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_output_directory(path)

    def test_source_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            for path in (source, source / 'child', source.parent):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    validate_output_directory(path, source_roots=(source,))

    def test_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'real').mkdir()
            (root / 'link').symlink_to(root / 'real', target_is_directory=True)
            for path in (root / 'link', root / 'link' / 'child'):
                with self.assertRaises(ValueError):
                    prepare_output_directory(path)

    def test_existing_output_is_backed_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = prepare_output_directory(root / 'output')
            (out / 'keep.txt').write_text('original')
            with self.assertRaises(FileExistsError):
                prepare_output_directory(out, overwrite=False)
            self.assertEqual((out / 'keep.txt').read_text(), 'original')
            self.assertEqual(prepare_output_directory(out), out)
            self.assertEqual(list(out.iterdir()), [])
            backups = list(root.glob('.output.backup-*/output/keep.txt'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'original')

    def test_invalid_merge_does_not_touch_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'output'
            out.mkdir()
            marker = out / 'keep.txt'
            marker.write_text('original')
            result = subprocess.run([sys.executable, '-m', 'tools.minigrid.merge_banks',
                                     '--source', 'invalid', '--out-root', str(out)],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(), 'original')
            self.assertEqual(list(Path(tmp).glob('.output.backup-*')), [])

    def test_successful_merge_preserves_rows_and_previous_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            (source / 'group').mkdir(parents=True)
            (source / 'group' / 'image.txt').write_text('image fixture')
            row = '{"group_id": "group", "uid": "fixture", "variant": "full"}\n'
            (source / 'triplets.jsonl').write_text(row)
            out = root / 'output'
            out.mkdir()
            (out / 'keep.txt').write_text('original')
            env = dict(os.environ, GRIDWM_REPORT_ROOT=str(root / 'reports'))
            result = subprocess.run([sys.executable, '-m', 'tools.minigrid.merge_banks',
                                     '--source', f'fixture={source}', '--out-root', str(out)],
                                    cwd=ROOT, capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((out / 'triplets.jsonl').read_text(), row)
            self.assertEqual((out / 'group' / 'image.txt').read_text(), 'image fixture')
            self.assertEqual(len(list(root.glob('.output.backup-*/output/keep.txt'))), 1)

    def test_merge_source_overlap_preserves_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            source.mkdir()
            marker = source / 'triplets.jsonl'
            marker.write_text('{"group_id":"group"}\n')
            for out in (source, source.parent, source / 'child'):
                result = subprocess.run([sys.executable, '-m', 'tools.minigrid.merge_banks',
                                         '--source', f'fixture={source}', '--out-root', str(out)],
                                        cwd=ROOT, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(marker.read_text(), '{"group_id":"group"}\n')


if __name__ == '__main__':
    unittest.main()
