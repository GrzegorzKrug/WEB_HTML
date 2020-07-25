# import pytest
import unittest
from image.ImageCollector import grab_image_from_url, validate_url


class TestingClass(unittest.TestCase):

    # def test_fail(self):
    #     assert False
    #     pass

    def test_pos(self):
        pass

    # def test_error(self):
    #     raise ValueError

    def test_longloop(self):
        for x in range(2**8):
            for j in range(2**8):
                pass

    def test_5(self):
        validate_url('www.google.pl')

if __name__ == '__main__':
    unittest.main()


