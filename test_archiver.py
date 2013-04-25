#!/usr/bin/env python
import mock
import unittest
from archiver import fetch


class TestPDF(unittest.TestCase):
    #FIXME test network problems
    #FIXME mock stuff
    def setUp(self):
        self.link = "http://nvidia.com/content/PDF/sc_2010/CUDA_Tutorial/SC10_Accelerating_GPU_Computation_Through_Mixed-Precision_Methods.pdf"

    def test_content_type(self):
        l = fetch.Archive(self.link)
        self.assertEqual(l.content_type(), 'application/pdf')

    def test_fetch_pdf(self):
        l = fetch.Archive(self.link)
        pass


if __name__ == '__main__':
    unittest.main()