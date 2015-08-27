#########################################################
# Import package, helpers and constant
#########################################################

# Packages

import random
import json
import pickle
import time

import requests
import lxml
from lxml import html
from requests import Request, Session


# Helpers

class CustomRequest(object):
	"""
	This is a Class based on top of the requests package providing
	the ability to easily to request rotating user-agent and/or proxies

	Arguments
	---------
	list_user_agent: a list of user-agent by default the list provided in the
	beginning of the program
	list_proxies : a list of dictionnary of proxies :
	[{'https': 'https://186.233.94.106:8080'},{...},], default []

	Returns
	-------
	A class with a get method that is just a customization of requests.get()
	"""

	def __init__(self,list_user_agent=None,rotate_ua = True,list_proxies = []):
		if not list_user_agent:
			self.list_user_agent = [
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
	    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
	    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
	    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
	    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
	    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
	    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
	]
		else:
			self.list_user_agent = list_user_agent

		self.list_proxies = list_proxies
		self.rotate_ua = rotate_ua
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
		self.proxy = {}

	def set_random_ua(self):
		self.headers['user-agent'] = random.choice(self.list_user_agent)

	def set_random_proxy(self):
	    self.proxy = random.choice(self.list_proxies)

	def get(self,url,*args,**kwargs):
		if self.rotate_ua is True:
			self.set_random_ua()
		if self.list_proxies :
		    self.set_random_proxy()
		    return requests.get(url = url ,headers = self.headers,proxies = self.proxy,*args,**kwargs)
		else :
			return requests.get(url = url ,headers = self.headers,*args,**kwargs)



def create_search_url(list_keyword):
	return '%20'.join(list_keyword)


def get_linkedin_url(list_keyword,*args,**kwargs):
	""" This function will search the linkedin profile with duckduckgo with the requested
	list_keyword and select the best result

	Arguments
	---------
	list_keyword : list of keywords (don't need to add linkedin on it)

	"""
	if 'linkedin' not in [k.lower() for k in list_keyword]:
		list_keyword.append('Linkedin')
	url_to_get = self.url_ddg + self.create_search_url(list_keyword=list_keyword)
	response = self.crequest.get(url_to_get)
	hxs = html.fromstring(response.text)
	url_to_follow = hxs.xpath(('(//div[@id = "links"]//' +\
    'div[@class = "results_links results_links_deep web-result"])[1]//a[@class ="large"]/@href'))
	return url_to_follow[0]
