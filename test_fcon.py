#!/usr/bin/env python3
import stat
import os
import shutil
import unittest
from fcon import fcon, set_verbose_output, set_output_immediately, set_trial_move, clear_globals_for_unittests
from stat import S_IREAD, S_IRGRP, S_IROTH
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
        response = fcon('test/one_file')
        self.assertRegex(response, 'Processing file')

    def test_files_in_path_root_not_processed(self):
        response = fcon('test/two_files')
        self.assertRegex(
            response, 'Processing file test.two_files.sub1.bbb.txt')
        self.assertNotRegex(response, 'Processing file test.two_files.aaa.txt')

    def test_trial_move_of_file_in_subfolder_to_path(self):
        response = fcon('test/two_files')
        self.assertRegex(response, '... moved bbb.txt')

    def test_move_file_in_subfolder_to_path(self):
        shutil.rmtree('test/move_two_files', ignore_errors=True)
        shutil.rmtree('test/move_two_files', ignore_errors=True)
        shutil.rmtree('test/move_two_files', ignore_errors=True)
        shutil.copytree('test/two_files', 'test/move_two_files')
        set_trial_move(False)
        response = fcon('test/move_two_files')
        set_trial_move(True)
        self.assertRegex(response, '... moved bbb.txt')
        self.assertTrue(os.path.isfile('test/move_two_files/000-bbb.txt'))
        self.assertFalse(os.path.isfile('test/move_two_files/sub1/bbb.txt'))

    def test_rename_file_if_needed_to_avoid_clash_and_preserve_sort_order(self):
        shutil.rmtree('test/move_three_files', ignore_errors=True)
        shutil.rmtree('test/move_three_files', ignore_errors=True)
        shutil.rmtree('test/move_three_files', ignore_errors=True)
        shutil.copytree('test/three_files', 'test/move_three_files')
        set_trial_move(False)
        response = fcon('test/move_three_files')
        set_trial_move(True)
        self.assertRegex(response, '... moved aaa.txt --> 000-aaa.txt\n')
        self.assertRegex(response, '... moved bbb.txt --> 000-bbb.txt')
        self.assertRegex(response, '... moved aaa.txt --> 001-aaa.txt')
        self.assertRegex(response, '... moved aaa.txt --> 002-aaa-1.txt')
        self.assertTrue(os.path.isfile('test/move_three_files/000-aaa.txt'))
        self.assertTrue(os.path.isfile('test/move_three_files/001-aaa.txt'))
        self.assertTrue(os.path.isfile('test/move_three_files/002-aaa-1.txt'))
        self.assertTrue(os.path.isfile('test/move_three_files/002-aaa.txt'))

    def test_unicode_files(self):
        response = fcon('test/unicode_files')
        self.assertRegex(response, '6 files moved')

    def test_print_summary(self):
        response = fcon('test/two_files')
        self.assertRegex(response, 'files moved')


if __name__ == '__main__':
    one_time_setup()
    unittest.main()
