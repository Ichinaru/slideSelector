__author__ = 'Administrator'

import unittest
from numpy import zeros_like
from numpy.testing import assert_array_equal
from src.processing.base_processing import BaseExporter
from src.annotations import get_annotation_list

annotation_folder_test = 'C:/Data'
annotation_file_test = 'C:/Data/2.ndpi.ndpa'

class TestBaseExporter(unittest.TestCase):
    def test_init(self):
        be = BaseExporter(annotation_file_test)
        self.assertEqual(be.image_file, 'C:/Data/2.ndpi')
        self.assertEqual(be.export_folder, 'C:/Data/2')
        fp = be.annotations
        fp_pl = [ann.point_list for ann in fp]
        fa = get_annotation_list(annotation_file_test)
        fa_pl = [ann.point_list for ann in fa]
        for a,b in zip(fp_pl, fa_pl):
            assert_array_equal(a,b)

if __name__ == '__main__':
    unittest.main()
