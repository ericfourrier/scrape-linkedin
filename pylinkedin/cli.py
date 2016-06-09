"""
Usage: pylinkedin -u url
Options:
  -u --url : Url of the profile you want to scrape
  -a --attribute : Display only a specific attribute, display everything by default
  -h --help : Show this screen.
Examples:
    pylinkedin -u https://www.linkedin.com/in/nadia-freitag-81173966 -a skills
"""

import click
from .scraper import LinkedinItem
from pprint import pprint


@click.command()
@click.option('--url', '-u', type=str, help='Url of the profile you want to scrape')
@click.option('--attribute', '-a', type=click.Choice(LinkedinItem.attributes_key),
              default=None, help='Display only a specific attribute, display everything by default')
#@click.option('--html', '-h', type=str, help='Raw html of the profile you want to scrape')
def scrape(url, attribute):
    """Simple command line to """
    linkedin = LinkedinItem(url=url)
    if attribute is None:
        pprint(linkedin.to_dict())
    else:
        pprint(linkedin.__getattribute__(attribute))
