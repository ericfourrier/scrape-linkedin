from pylinkedin.scraper import *
from pylinkedin.utils import *
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

    def test_clean(self):
        assert clean(u'  engineer ') == u'engineer'
        assert clean([' R',' Python',' Mathlab']) == [u'R',u'Python',u'Mathlab']
        assert clean(3) == 3
        assert clean(3.0) == 3.0


class TestConnection(unittest.TestCase):

    def test_get_jeff_weiner(self):
        linkedin = LinkedinItem(url = "https://www.linkedin.com/in/jeffweiner08")
        assert linkedin.response.ok == True


class TestLinkedinOffline(unittest.TestCase):

    def setUp(self):
        """ creating test data set for the test module """
        self.linkedin = LinkedinItem(html_string = read_linkedin_template('test_adarshmani.html'))

    def test_get_name(self):
        assert self.linkedin.get_name() == u'Adarsh Kumar Mani'

    def test_get_current_title(self):
        assert self.linkedin.get_current_title() == u'Software Engineer at Apple'

    def test_get_current_education(self):
        assert isinstance(self.linkedin.get_current_education(),dict) == True
        assert self.linkedin.get_current_education()['name'] == u'University of California, Berkeley'
        assert self.linkedin.get_current_education()['url'] == u'http://www.linkedin.com/edu/school?id=17939&trk=ppro_sprof'



