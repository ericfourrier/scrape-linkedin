from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='scrape-linkedin',
      version="0.1",
      description='Linkedin scraper to get all details on public linkedin profiles.',
      long_description=readme(),
      author='Eric Fourrier',
      author_email='ericfourrier0@gmail.com',
      license='MIT',
      url='https://github.com/ericfourrier/scrape-linkedin',
      packages=['pylinkedin'],
      entry_points={'console_scripts': ['pylinkedin=pylinkedin.cli:scrape']},
      test_suite='test_linkedin',
      keywords=['linkedin', 'api', 'scraper'],
      include_package_data=True,
      package_data={'pylinkedin': ['data/*.txt']},
      zip_safe=False,
      install_requires=[
          'requests>=2.0.0',
          'lxml',
          'click']
      )
