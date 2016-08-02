"""
Usage: pylinkedin -u url
Options:
  -u --url : Url of the profile you want to scrape
  -a --attribute : Display only a specific attribute, display everything by default
  -f --file_path : Raw path to html of the profile you want to scrape
  -h --help : Show this screen.
Examples:
    pylinkedin -u https://www.linkedin.com/in/nadia-freitag-81173966 -a skills
"""

import click
from .scraper import LinkedinItem
from pprint import pprint

def read_text(file_path):
    with open(file_path, 'r') as f:
        return f.read()

@click.command()
@click.option('--url', '-u', type=str, help='Url of the profile you want to scrape')
@click.option('--attribute', '-a', type=click.Choice(LinkedinItem.attributes_key),
              default=None, help='Display only a specific attribute, display everything by default')
@click.option('--file_path', '-f',type=click.Path(exists=True),default=None, help='Raw path to html of the profile you want to scrape')
def scrape(url, attribute, file_path):
    """Simple command line to scrape a profile"""
    if file_path is not None:
        linkedin_profile = LinkedinItem(html_string=read_text(file_path))
    else:
        linkedin_profile = LinkedinItem(url=url)

    if attribute is not None:
        pprint(linkedin_profile.__getattribute__(attribute))
    else:
        pprint(linkedin_profile.to_dict())
