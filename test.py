from linkedin.scraper import *
from linkedin.utils import *
import unittest
import pytest
import time
import codecs

def read_linkedin_template(file_name):
    with codecs.open('data/' + file_name,'r',encoding = 'utf-8') as f:
        data = f.read()
    return data

def clock(func):
    """ decorator to measure the duration of each test of the unittest suite,
    this is extensible for any kind of functions it will just add a print  """
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args)
        elapsed = (time.time() - t0) * 1000  # in ms
        print 'elapsed : [{0:0.3f}ms]'.format(elapsed)
        return result


class TestUtils(unittest.TestCase):

    def test_extract_one(self):
        assert extract_one([u'engineer'])  == u'engineer'
        assert extract_one([]) is None
        assert extract_one([u'R',u'Python']) == [u'R',u'Python']

    def test_clean(self):
        assert clean(u'  engineer ') == u'engineer'
        assert clean([' R',' Python',' Mathlab']) == [u'R',u'Python',u'Mathlab']
        assert clean(3) == 3
        assert clean(3.0) == 3.0



# class TestLinkedinOffline(unittest.TestCase):

#     def setUp(self):
#         """ creating test data set for the test module """
#         self.linkedin = LinkedinItem(html_code = read_linkedin_template('test_adarshmani.html'))

