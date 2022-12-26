#!/usr/bin/env python3
import os
import shutil
import unittest

from fcon import (
    clear_globals_for_unittests,
    fcon,
    set_output_immediately,
    set_trial_move,
    set_verbose_output,
    set_no_rename,
)

version = "0.1.1"


# self.assertTrue(exp)
# self.assertEqual(a,b)
# self.assertContains(response, 'must supply test_name')
# self.assertRegex(response.content.decode('utf-8'), 'Test Passed: True')
# self.assertNotRegex(response.content.decode('utf-8'), 'delete id test')


def one_time_setup():
    set_verbose_output(True)
    set_output_immediately(False)
    set_trial_move(True)


class Testfcon(unittest.TestCase):
    def setUp(self):
        clear_globals_for_unittests()
        pass

    def tearDown(self):
        pass

    # ToDo: Only increment folder number if it contained files

    def test_verbose_output_enabled(self):
        response = fcon("test/one_file")
        self.assertRegex(response, "Processing file")

    def test_files_in_path_root_not_processed(self):
        response = fcon("test/two_files")
        self.assertRegex(response, "Processing file test.two_files.sub1.bbb.txt")
        self.assertNotRegex(response, "Processing file test.two_files.aaa.txt")

    def test_trial_move_of_file_in_subfolder_to_path(self):
        response = fcon("test/two_files")
        self.assertRegex(response, "... moved bbb.txt")

    def test_move_file_in_subfolder_to_path(self):
        shutil.rmtree("test/move_two_files", ignore_errors=True)
        shutil.rmtree("test/move_two_files", ignore_errors=True)
        shutil.rmtree("test/move_two_files", ignore_errors=True)
        shutil.copytree("test/two_files", "test/move_two_files")
        set_trial_move(False)
        response = fcon("test/move_two_files")
        set_trial_move(True)
        self.assertRegex(response, "... moved bbb.txt")
        self.assertTrue(os.path.isfile("test/move_two_files/000-bbb.txt"))
        self.assertFalse(os.path.isfile("test/move_two_files/sub1/bbb.txt"))

    def test_rename_file_if_needed_to_avoid_clash_and_preserve_sort_order(self):
        shutil.rmtree("test/move_three_files", ignore_errors=True)
        shutil.rmtree("test/move_three_files", ignore_errors=True)
        shutil.rmtree("test/move_three_files", ignore_errors=True)
        shutil.copytree("test/three_files", "test/move_three_files")
        set_trial_move(False)
        response = fcon("test/move_three_files")
        set_trial_move(True)
        self.assertRegex(response, "... moved aaa.txt --> 000-aaa.txt\n")
        self.assertRegex(response, "... moved bbb.txt --> 000-bbb.txt")
        self.assertRegex(response, "... moved aaa.txt --> 001-aaa.txt")
        self.assertRegex(response, "... moved aaa.txt --> 002-aaa-1.txt")
        self.assertTrue(os.path.isfile("test/move_three_files/000-aaa.txt"))
        self.assertTrue(os.path.isfile("test/move_three_files/001-aaa.txt"))
        self.assertTrue(os.path.isfile("test/move_three_files/002-aaa-1.txt"))
        self.assertTrue(os.path.isfile("test/move_three_files/002-aaa.txt"))

    def test_unicode_files(self):
        response = fcon("test/unicode_files")
        self.assertRegex(response, "0 files moved")

    def test_print_summary(self):
        response = fcon("test/two_files")
        self.assertRegex(response, "files moved")

    def test_no_rename(self):
        shutil.rmtree("test/norename_three_files", ignore_errors=True)
        shutil.rmtree("test/norename_three_files", ignore_errors=True)
        shutil.rmtree("test/norename_three_files", ignore_errors=True)
        shutil.copytree("test/three_files", "test/norename_three_files")
        set_trial_move(False)
        set_no_rename(True)
        response = fcon("test/norename_three_files")
        set_no_rename(False)
        set_trial_move(True)
        self.assertRegex(response, "... moved aaa.txt\n")
        self.assertRegex(response, "... moved bbb.txt\n")
        self.assertRegex(response, "... skipping test/norename_three_files/sub1/sub2/aaa.txt\n")
        self.assertRegex(response, "... skipping test/norename_three_files/sub1/sub2/sub3/aaa.txt\n")
        self.assertRegex(response, "2 files moved")
        self.assertTrue(os.path.isfile("test/norename_three_files/aaa.txt"))
        self.assertTrue(os.path.isfile("test/norename_three_files/aaa.txt"))


if __name__ == "__main__":
    one_time_setup()
    unittest.main()
