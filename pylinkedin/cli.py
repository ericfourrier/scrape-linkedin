"""
Usage: pylinkedin -u url
Options:
  -u --url : Url of the profile you want to scrape
  -a --attribute : Display only a specific attribute ()
  -h --help                         Show this screen.
  --version
Examples:
  skele hello
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rdegges/skele-cli
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
    """Simple program that greets NAME for a total of COUNT times."""
    linkedin = LinkedinItem(url=url)
    if attribute is None:
        pprint(linkedin.to_dict())
    else:
        pprint(linkedin.__getattribute__(attribute))
