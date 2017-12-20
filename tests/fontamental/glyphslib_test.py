import sys
import unittest
from fontamental.glyphslib import GlyphsLib


class IndexTest(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def setUp(self):
        # self.infoTab = NameTabWidget(None)
        self.gl = GlyphsLib()


    def tearDown(self):
        # self.fontInfo.close()
        pass

    def test_sample1(self):
        val = self.gl.getAGL2UV()
        self.assertEqual(1, 1)

    def test_sample2(self):
        self.assertEqual(2, 2)


if __name__ == "__main__":
    unittest.main()
