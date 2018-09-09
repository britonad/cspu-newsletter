import unittest

from utils.common import check_uploaded_files


class TestCommonUtils(unittest.TestCase):
    def setUp(self):
        self.data_empty = []

    def test_not_uploaded_files(self):
        self.assertEqual(check_uploaded_files(self.data_empty), [])
