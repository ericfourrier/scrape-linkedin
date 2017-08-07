#########################################################
# Import package, helpers and constant
#########################################################

# Packages

import random
#import json
import time

import requests
from lxml import html
from .exceptions import ServerIpBlacklisted, BadStatusCode, ProfileNotFound
#########################################################
# Helpers
#########################################################

# Requests with rotating proxies and user-agent

def to_requests_format(ip, port):
    """ Returns the proxy format for requests package """
    return {'http': 'http://{}:{}'.format(ip, port),
            'https': 'http://{}:{}'.format(ip, port)}

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

    def __init__(self, list_user_agent=None, rotate_ua=False, list_proxies=None):
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

        self.list_proxies = [] if not list_proxies else list_proxies
        self.rotate_ua = rotate_ua
        # GoogleBot by default
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}
        self.proxy = {}

    def set_random_ua(self):
        self.headers['User-Agent'] = random.choice(self.list_user_agent)

    def set_random_proxy(self):
        self.proxy = random.choice(self.list_proxies)

    def _get(self, url, *args, **kwargs):
        """ Get helpers to handle exceptions """
        try:
            r = requests.get(url=url, *args, **kwargs)
            if r.status_code == 999:
                msg_error = "Linkedin blacklists ips for unauthentified http requests, Aws, Digital Ocean"
                raise ServerIpBlacklisted(msg_error)
            elif r.status_code == 404:
                raise ProfileNotFound("The following url :{} can not be publicely found on Linkedin (404 error)".format(url))
            elif r.status_code != 200:
                raise BadStatusCode("The status code of the get requests is: {}".format(r.status_code))
            return r
        except requests.exceptions.Timeout:
            raise Exception("Request timeout")
        except requests.exceptions.RequestException as e:
            print(e)

    def get(self, url, *args, **kwargs):
        if self.rotate_ua is True:
            self.set_random_ua()
        if self.list_proxies:
            self.set_random_proxy()
            return self._get(url=url, headers=self.headers, proxies=self.proxy, *args, **kwargs)
        else:
            return self._get(url=url, headers=self.headers, *args, **kwargs)

# Read and write to a pretty json


def random_delay(static=0.5, variable=1):
    time.sleep(static + variable * random.random())


def write_to_json(json_file_path, data):
    with open(json_file_path, "a") as f:
        f.write("{}\n".format(json.dumps(data)))


def read_from_json(json_file_path):
    data = []
    with open(json_file_path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data


# Others
def create_search_url(list_keyword):
    return '%20'.join(list_keyword)

