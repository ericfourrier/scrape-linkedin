# pylinkedin
[![Travis-CI Build Status](https://travis-ci.org/ericfourrier/scrape-linkedin.svg?branch=master)](https://travis-ci.org/ericfourrier/scrape-linkedin)




## Introduction

`pylinkedin` is a python package to scrape all details from public LinkedIn profiles.
 It can also be used as a parser to transform html LinkedIn profiles into structured json.
 
Some precautions you should take if you want scrape LinkedIn with python :
* Change the default python requests user-agent for a browser user-agent like "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1".
* By default LinkedIn has strong anti-scraping policies.
LinkedIn will quickly blacklist ips making unauthentified requests
from by responding with a non standard http status code `999` to the  http requests. Especially LinkedIn banned most ips from cloud providers (Aws, Digital Ocean, ...).
* You can use proxies if you want to do concurrent requests but they may also fail a lot.

## Installation

### Install with pip
Run `pip install git+git://github.com/ericfourrier/scrape-linkedin.git`

### Install from source
`git clone https://github.com/ericfourrier/scrape-linkedin.git`

Run `python setup.py install`

### Tests
The tests are runs with a html file from a LinkedIn profile. The main reason is because [Travis](https://travis-ci.org/) use aws machine
and its ips are banned by Linkedin.

Especially the fact that the test suite is passed is not a good indicator than the package will work (Your ip can be banned or LinkedIn html source code changed).

You can still run the test suite at the root of the package with pytest: `py.test test.py`.

## Using this package

### Command line
pylinkedin comes with a simple command line argument module `pylinkedin`.

Options:
* -u --url : Url of the profile you want to scrape
* -a --attribute : Display only a specific attribute, display everything by default
* -f --file_path : Raw path to html file of the profile you want to scrape
* -h --help : Show this screen.

Examples:
* Get a json of Jeff Weiner profile: `pylinkedin -u https://www.linkedin.com/in/jeffweiner08`
* Get only the skills of Jeff Weiner: `pylinkedin -u https://www.linkedin.com/in/jeffweiner08 -a skills`
* Parse html stored profile and get json: `pylinkedin -f /path/file.html`

### Python Package

It relies on two class:

`CustomRequest` which is just a way to customise your http request specifying a list of user-agents or proxies.
    
    from pylinkedin.utils import CustomRequest
    c = CustomRequest() # default with rotating proxies
    c = CustomRequest(rotating_ua=False) # without rotating user-agent
    c = CustomRequest(list_proxies=[{'https':'http://186.233.94.106:8080',
    'http':'http://186.233.94.106:8080'}]))

`LinkedinItem` is the main class, you can instantiate it with the URL of public profile using the `url` parameter, or with the HTML contents of the profile page, using `html_string`. See `test.py` for an example of using a save HTML file as input for the scrapper.

    from pylinkedin.scraper import LinkedinItem
    l = LinkedinItem(url='https://www.linkedin.com/in/kennethreitz')
    l = LinkedinItem(html_string=profile_string)
    
You can customize your requests using `CustomRequest` class for `LinkedinItem`

    c = CustomRequest(rotating_ua = True)
    url_to_scrape = "https://www.linkedin.com/in/jeffweiner08"
    l = LinkedinItem(url=url_to_scrape, crequest=c) # passing requests with rotating user-agent

To use the `html_string`, make sure to browse to the public version of the profile page, as the private version will not work. The private version is the one showing the edit controls next to each section.  

'LinkedinItem' has the folowing syntax the get the info :

    l.name # to get the name
    l.skills # to get the skills
    l.publications  # to get the publications
    ...
    # the most important
    l.to_dict() to get all infos


### Exhaustive list of the fields scraped

  [volunteerings, last_name, number_recommendations, number_connections, current_location, honors, first_name, current_title, test_scores, current_industry, languages, similar_profiles, interests, profile_img_url, current_education, educations, experiences, groups, organizations, certifications, name, skills, websites, summary, project, courses, publications,recommendations]

### Issues
Package is not actively maintained.

You can post bugs and issues [here](https://github.com/ericfourrier/scrape-linkedin/issues).
