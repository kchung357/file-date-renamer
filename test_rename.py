import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime

import rename


def touch(directory, name, when):
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("x")
    stamp = when.timestamp()
    os.utime(path, (stamp, stamp))
    return path


class RenameFilesTest(unittest.TestCase):
    def test_name_uses_mtime_and_keeps_extension(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "in")
            dest = os.path.join(root, "out")
            os.makedirs(source)
            os.makedirs(dest)
            touch(source, "photo.JPG", datetime(2026, 6, 20, 14, 25, 3))

            failed = rename.rename_files(source, dest)

            self.assertEqual(failed, 0)
            self.assertEqual(os.listdir(dest), ["2026062014250000.JPG"])
            self.assertEqual(os.listdir(source), [])

    def test_same_minute_gets_distinct_names(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "in")
            dest = os.path.join(root, "out")
            os.makedirs(source)
            os.makedirs(dest)
            when = datetime(2026, 6, 20, 14, 25, 3)
            touch(source, "a.jpg", when)
            touch(source, "b.jpg", when)

            rename.rename_files(source, dest)

            self.assertEqual(
                sorted(os.listdir(dest)),
                ["2026062014250000.jpg", "2026062014250001.jpg"],
            )

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "in")
            dest = os.path.join(root, "out")
            os.makedirs(source)
            os.makedirs(dest)
            when = datetime(2026, 6, 20, 14, 25, 3)
            taken = touch(dest, "2026062014250000.jpg", when)
            with open(taken, "w", encoding="utf-8") as handle:
                handle.write("keep")
            touch(source, "photo.jpg", when)

            rename.rename_files(source, dest)

            with open(taken, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "keep")
            self.assertTrue(os.path.exists(os.path.join(dest, "2026062014250001.jpg")))

    def test_skips_subdirectories(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "in")
            dest = os.path.join(root, "out")
            os.makedirs(os.path.join(source, "nested"))
            os.makedirs(dest)
            touch(source, "photo.jpg", datetime(2026, 6, 20, 14, 25, 3))

            rename.rename_files(source, dest)

            self.assertEqual(os.listdir(dest), ["2026062014250000.jpg"])
            self.assertTrue(os.path.isdir(os.path.join(source, "nested")))

    def test_dry_run_leaves_files_in_place(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "in")
            dest = os.path.join(root, "out")
            os.makedirs(source)
            os.makedirs(dest)
            touch(source, "photo.jpg", datetime(2026, 6, 20, 14, 25, 3))

            rename.rename_files(source, dest, dry_run=True)

            self.assertEqual(os.listdir(source), ["photo.jpg"])
            self.assertEqual(os.listdir(dest), [])

    def test_invalid_directory_exits_with_usage_error(self):
        script = os.path.join(os.path.dirname(__file__), "rename.py")
        result = subprocess.run(
            [sys.executable, script, "-i", "missing-in", "-o", "missing-out"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
