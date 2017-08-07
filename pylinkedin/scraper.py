# -*- coding: utf-8 -*-
"""
@author: efourrier

Purpose : Create a unofficial api to get linkedin employment info with
http request and DOM parsing.

Scraper for v3-public

Notes :

"""

#########################################################
# Import package, helpers and constant
#########################################################

# Packages

from .utils import CustomRequest
from .exceptions import ProfileNotFound, NotAProfile

import time

from lxml import html


# Helpers

def extract_one(l, value=None):
    """ Return value if empy list else return first element """
    if len(l) == 0:
        return value
    else:
        return l[0]


def clean(l):
    """ bad coding for python 3 support """
    if isinstance(l, list):
        if l == []:
            return []
        else:
            l = ([x.strip().replace('\t', u"") for x in l])
            l = [x for x in l if x != u""]
            l = [x for x in l if x != ',']
            return l
    elif isinstance(l, float) or isinstance(l, int):
        return l
    else:
        return l.strip()


def get_first_n(l):
    if l == []:
        return 'error'
    else:
        return l[0]

def get_list_i(l, i):
    if not isinstance(l, list):
        return None
    try :
        return l[i]
    except IndexError:
        return None
    else:
        None
# Constants

# proxy = {"http": "http://123proxysites.science",
#         "https" : "https://www.proxery.com"}

# get = partial(requests.get, headers={'user-agent':
# random.choice(list_user_agent)},allow_redirects=True)


# gd_url = 'http://www.glassdoor.com'
# url_api_glassdoor = 'http://www.glassdoor.com/api/employer/'


#########################################################
# MySession class
#########################################################


class LinkedinItem(object):

    attributes_key = ['volunteerings', 'last_name', 'number_recommendations',
                     'number_connections', 'current_location', 'honors', 'first_name',
                     'current_title', 'test_scores', 'current_industry', 'languages',
                     'similar_profiles', 'interests', 'has_profile_picture', 'current_education',
                     'educations', 'experiences', 'groups', 'organizations', 'certifications',
                     'name', 'skills', 'websites', 'summary', 'project', 'courses',
                     'publications', 'recommendations']

    def __init__(self, url=None, html_string=None, crequest=None):
        # if you want put the html text directly
        self.url = url
        self.html_string = html_string
        if self.html_string is not None:
            self.tree = html.fromstring(self.html_string)

        # otherwise request the url
        elif self.html_string is None and self.url is not None:
            self.crequest = CustomRequest() if crequest is None else crequest
            if 'linkedin.com/in' not in url:
                raise NotAProfile("The url passed does not contain a valid lnkedin profile")
            self.response = self.crequest.get(self.url)
            self.tree = html.fromstring(self.response.text)
        else:
            raise ValueError('url or html_string should be defined')
        # if extract_one(self.tree.xpath('.//div[@id="content"]/h1/text()')).strip() == "Profile Not Found":
        #     raise ProfileNotFound("The following url :{} can not be publicely found on Linkedin".format(
        #             self.url))
        # Header path
        self.xp_header = extract_one(self.tree.xpath('.//div[@class = "profile-overview"]'))
        # Experiences path
        self.xp_experiences = self.tree.xpath('//section[@id = "experience"]/ul/li[@class="position"]')
        # Projets
        self.xp_projects = self.tree.xpath('//section[@id = "projects"]/ul/li[@class="project"]')
        # Language
        self.xp_languages = self.tree.xpath('//section[@id = "languages"]/ul/li[@class="language"]')
        # Volunteering
        self.xp_volunteerings = self.tree.xpath('//section[@id = "volunteering"]/ul/li[@class="volunteering"]')
        # Organizations
        self.xp_organizations = self.tree.xpath('//section[@id = "organizations"]/ul/li[@class="organization"]')
        # Honors
        self.xp_honors = self.tree.xpath('//section[@id = "awards"]/ul/li[@class="award"]')
        # Test Scores
        self.xp_test_scores = self.tree.xpath('//section[@id = "test-scores"]/ul/li[@class="publication"]')
        # Publications
        self.xp_publications = self.tree.xpath('//section[@id = "publications"]/ul/li[@class="publication"]')
        # Education
        self.xp_educations = self.tree.xpath('//section[@id = "education"]/ul/li[@class="school"]')
        # Certifications
        self.xp_certifications = self.tree.xpath('//section[@id = "publication"]/ul/li[@class="certification"]')
        # Courses
        self.xp_courses = self.tree.xpath('//section[@id = "courses"]/ul/li[@class="course"]')
        # Similar profiles
        self.xp_similar_profiles = self.tree.xpath('//div[contains(@class,"browse-map")]/ul/li[@class="profile-card"]')
        # Publications
        self.xp_publications = self.tree.xpath('//section[@id = "publications"]/ul/li[@class="publication"]')
        # Interests
        self.xp_interests = self.tree.xpath('//section[@id = "interests"]/ul/li[@class="interest"]')
        # Groups
        self.xp_groups = self.tree.xpath('//section[@id = "groups"]/ul/li[@class="group"]')
        # Skills
        self.xp_skills = self.tree.xpath('//section[@id = "skills"]/ul/li[@class="skill"]')
        # Organization
        self.xp_organizations = self.tree.xpath('//section[@id = "organizations"]//ul/li')
        # Recommendations
        self.xp_recommendations = self.tree.xpath('//section[@id = "recommendations"]//ul/li')
        # Summary
        # self.xp_summary = extract_one(self.tree.xpath('//div[@id = "summary"]'))
        # Recommendation
        # self.xp_recommendations = extract_one(self.tree.xpath('//div[@id = "recommendations"]'))

    @staticmethod
    def get_xp(origin, path):
        """ Helper to query xpath from origin """
        return clean(origin.xpath(path))

    def get_clean_xpath(self, x):
        return clean(self.tree.xpath(x))

    # Header

    def create_raw_path(self):
        """ Generate raw path as standard variables """
        # Header path
        self.xp_header_raw = extract_one(self.tree.xpath('.//div[@class = "profile-overview"]'))
        # Experiences path
        self.xp_experiences_raw = extract_one(self.tree.xpath('//section[@id = "experience"]'))
        # Projets
        self.xp_projects_raw = extract_one(self.tree.xpath('//section[@id = "projects"]'))
        # Language
        self.xp_languages_raw = extract_one(self.tree.xpath('//section[@id = "languages"]'))
        # Volunteering
        self.xp_volunteerings_raw = extract_one(self.tree.xpath('//section[@id = "volunteering"]'))
        # Organizations
        self.xp_organizations_raw = extract_one(self.tree.xpath('//section[@id = "organizations"]'))
        # Honors
        self.xp_honors_raw = extract_one(self.tree.xpath('//section[@id = "honors"]'))
        # Test Scores
        self.xp_test_scores_raw = extract_one(self.tree.xpath('//section[@id = "test-scores"]'))
        # Publications
        self.xp_publications_raw = extract_one(self.tree.xpath('//section[@id = "publications"]'))
        # Education
        self.xp_educations_raw = extract_one(self.tree.xpath('//section[@id = "education"]'))
        # Certifications
        self.xp_certifications_raw = extract_one(self.tree.xpath('//section[@id = "certifications"]'))
        # Courses
        self.xp_courses_raw = extract_one(self.tree.xpath('//section[@id = "courses"]'))
        # Similar profiles
        self.xp_similar_profiles_raw = extract_one(self.tree.xpath('//div[contains(@class,"browse-map")]'))
        # Interests
        self.xp_interests_raw = extract_one(self.tree.xpath('//section[@id = "interests"]'))
        # Groups
        self.xp_groups_raw = extract_one(self.tree.xpath('//section[@id = "groups"]'))
        # Skills
        self.xp_skills_raw = extract_one(self.tree.xpath('//section[@id = "skills"]'))
        # Organization
        self.xp_organizations_raw = extract_one(self.tree.xpath('//section[@id = "organizations"]'))
        # Summary

    @property
    def url_detected(self):
        """ Return the url detected on the web page """
        return extract_one(self.tree.xpath('.//head/link[@rel = "canonical"]/@href'))

    @property
    def has_profile_picture(self):
        picture = self.tree.xpath('.//div[@class="profile-picture"]/a')
        return True if picture else  False

    @property
    def name(self):
        """ Return name of the profile """
        return extract_one(self.get_xp(self.xp_header, './/h1[@id="name"]/text()'))

    @property
    def first_name(self):
        """ Return first name """
        first_name = get_list_i(self.name.split(' ', 1), 0) if self.name is not None else None
        return first_name

    @property
    def last_name(self):
        """ Return last name of the profile """
        last_name = get_list_i(self.name.split(' ', 1), 1) if self.name is not None else None
        return last_name

    @property
    def current_title(self):
        """ Return current title """
        return extract_one(self.get_xp(self.xp_header, './/p[@class="headline title"]/text()'))

    @property
    def current_location(self):
        """ Return current location """
        return extract_one(self.get_xp(self.xp_header, './/dl[@id="demographics"]/dd[@class="descriptor adr"]/span/text()'))

    @property
    def current_industry(self):
        """ Return current industry """
        return extract_one(self.get_xp(self.xp_header, './/dl[@id="demographics"]/dd[@class="descriptor"]/text()'))

    @property
    def current_education(self):
        """ Return current education """
        name = extract_one(self.get_xp(
            self.xp_header, './/tr[@data-section="educationsDetails"]//a//text()'))
        url = extract_one(self.get_xp(
            self.xp_header, './/tr[@data-section="educationsDetails"]//a/@href'))
        return {'name': name, 'url': url}

    @property
    def websites(self):
        """ Return a list of websites of the linkedin member """
        return self.get_xp(self.xp_header, './/tr[@class="websites"]//li/a/@href')

    @property
    def number_connections(self):
        """ Return the number of connections """
        return extract_one(self.get_xp(self.xp_header, './/div[@class = "member-connections"]//strong//text()'))

    @property
    def number_recommendations(self):
        """ Return the number of recommendations """
        return extract_one(self.get_clean_xpath('//table[@class="extra-info"]//tr/th[contains(text(),"Recommandations") or contains(text(),"Recommendations") ]/following::td/strong[1]/text()'))

    # Interests, Groups  Skills  and Languages
    @property
    def interests(self):
        """ Return a list of Interests """
        if len(self.xp_interests) > 0:
            return [extract_one(self.get_xp(i, './/text()')) for i in self.xp_interests]
        else:
            return []

    @property
    def groups(self):
        """ Return a dictionnary of the groups with different parameters (name,img, url) """
        if len(self.xp_groups) > 0:
            return [{'name': extract_one(self.get_xp(g, './/h5/a/img/@alt')),
                    'img': extract_one(self.get_xp(g, './/h5/a/img/@src')),
                    'url': extract_one(self.get_xp(g, './/h4/a/@href'))}
                    for g in self.xp_groups]
        else:
            return []

    @property
    def skills(self):
        """ Return a list of skills """
        if len(self.xp_skills) > 0:
            return [{'name': extract_one(self.get_xp(s, './span//text()')),
                    'url': extract_one(self.get_xp(s, './a/@href'))}
                    for s in self.xp_skills]
        else:
            return []

    @property
    def languages(self):
        """ Return a list of dictionnary of languages with proficiency """
        if len(self.xp_languages) > 0:
            return [{'name': extract_one(self.get_xp(l, './/h4//text()')),
                     'proficiency': extract_one(self.get_xp(l, './/p[@class="proficiency"]/text()'))} for l in self.xp_languages]
        else:
            return []

    @property
    def summary(self):
        """ Return the summary of the linkedin profile """
        return ' '.join(self.get_clean_xpath('//section[@id = "summary"]//div[@class = "description"]/p//text()'))

    @property
    def recommendations(self):
        """ Return a list of description of the recommendations """
        return self.get_clean_xpath('//div[@id = "recommendations"]//ul/li/div[@class = "description"]/text()')

    @property
    def volunteering_opportunities(self):
        """ Return a list of the volunteering causes the linkedin member is looking for """
        return self.get_clean_xpath('//div[@class="opportunities"]/ul[@class="volunteering-opportunities"]/li/text()')

    @property
    def volunteering_causes(self):
        """ Return a list of the volunteering causes the linkedin member cares bout """
        return self.get_clean_xpath('//div[@id="volunteering-causes-view"]//ul[@class="volunteering-listing"]/li/text()')

    @property
    def experiences(self):
        """ Return a list of dictionnary with experience details """
        experiences = []
        if len(self.xp_experiences) > 0:
            for experience in self.xp_experiences:
                data = {}
                data['jobtitle'] = extract_one(
                    self.get_xp(experience, './/h4[@class="item-title"]//text()'))
                data['jobtitle_url'] = extract_one(
                    self.get_xp(experience, './/h4[@class="item-title"]/a/@href'))
                data['company'] = extract_one(

                    self.get_xp(experience, './/h5[@class="item-subtitle"]//text()'))
                data['linkedin_company_url'] = extract_one(
                    self.get_xp(experience, './/h5[@class="item-subtitle"]/a/@href'))
                data['linkedin_company_img_url'] = extract_one(
                    self.get_xp(experience, './/h5[@class="logo"]/a/img/@src'))
                data['area'] = extract_one(self.get_xp(
                    experience, './div//span[@class="locality"]/text()'))
                data['description'] = ' '.join(self.get_xp(
                    experience, './/p[contains(@class,"description")]/text()'))
                start_date = self.get_xp(
                    experience, './/span[@class="date-range"]/time[1]/text()')
                end_date = self.get_xp(
                    experience, './/span[@class="date-range"]/time[2]/text()')
                data['start_date'] = extract_one(start_date)
                if end_date:
                    data['end_date'] = extract_one(end_date)
                else:
                    data['end_date'] = time.strftime("%B-%Y")
                experiences.append(data)
        return experiences

    @property
    def educations(self):
        """
        Return a list of dictionnary with education details
        """
        schools = []
        if len(self.xp_educations) > 0:
            for school in self.xp_educations:
                data = {}
                data['university_name'] = extract_one(self.get_xp(school,
                    './/h4[@class="item-title"]//text()'))
                data['linkedin_university_url'] = extract_one(self.get_xp(school,
                    './/h4[@class="item-title"]/a/@href'))
                data['linkedin_university_img_url'] = extract_one(self.get_xp(school,
                    './/h5[@class="logo"]/a/img/@src'))
                data['description'] = extract_one(self.get_xp(
                    school, './/h5[@class="item-subtitle"]//text()'))
                if data['description'] is not None:
                    data['degree'] = get_list_i(data['description'].split(','), 0)
                    data['major'] = get_list_i(data['description'].split(','), 1)
                else :
                    data['degree'] = None
                    data['major'] = None
                start_date = self.get_xp(
                    school, './/span[@class="date-range"]/time[1]/text()')
                end_date = self.get_xp(
                    school, './/span[@class="date-range"]/time[2]/text()')
                data['start_date'] = extract_one(start_date)
                if end_date:
                    data['end_date'] = extract_one(end_date)
                else:
                    data['end_date'] = time.strftime("%B-%Y")
                schools.append(data)
        return schools

    @property
    def projects(self):
        """ Return a list of dictionnary with project details """
        projects = []
        if len(self.xp_projects) > 0:
            for project in self.xp_projects:
                data = {}
                data['title'] = extract_one(self.get_xp(project, './/h4//span[1]/text()'))
                data['url'] = extract_one(self.get_xp(project, './/h4/a/@href'))
                data['description'] = ' '.join(self.get_xp(project, './/p[contains(@class,"description")]//text()'))
                data['team_members'] = self.get_xp(project, './/dd[@class="associated-endorsements"]//li/a/text()')
                data['team_members_url'] = self.get_xp(project, './/dd[@class="associated-endorsements"]//li/a/@href')
                # data['team_members'] = [{'name': n, 'url': url} for n,url in
                # zip(team_members,team_members_url)]
                start_date = self.get_xp(project, './div//span[@class="date-range"]/time[1]/text()')
                end_date = self.get_xp(project, './div//span[@class="date-range"]/time[2]/text()')
                data['start_date'] = extract_one(start_date)
                if end_date:
                    data['end_date'] = extract_one(end_date)
                else:
                    data['end_date'] = time.strftime("%B-%Y")
                projects.append(data)
        return projects


    @property
    def courses(self):
        """ Return a list of dictionnary with courses details """
        courses=[]
        if len(self.xp_courses) > 0:
            for course in self.xp_courses:
                data={}
                data['university']=extract_one(self.get_xp(course, './/div[@id="courses-view"]//h4/a/text()'))
                data['university_url']=extract_one(self.get_xp(course, './/div[@id="courses-view"]//h4/a/@href'))
                data['course_name']=extract_one(self.get_xp(course, './/div[@id="courses-view"]//li/text()'))
                data['course_number']=extract_one(self.get_xp(course, './/div[@id="courses-view"]//li/span/text()'))
                courses.append(data)
        return courses

    @property
    def honors(self):
        """ Return a list of dictionnary with honors and awards details """
        honors=[]
        if len(self.xp_honors) > 0:
            for honor in self.xp_honors:
                data={}
                data['title']=extract_one(self.get_xp(honor, './/h4//text()'))
                data['delivred_by']=extract_one(self.get_xp(honor, './/h5//text()'))
                data['description']=' '.join((self.get_xp(honor, './/p[contains(@class,"description")]//text()')))
                data['date']=extract_one(self.get_xp(honor, './/span[@class = "date-range"]/time[1]/text()'))
                honors.append(data)
        return honors

    @property
    def volunteerings(self):
        """ Return a list of dictionnary with volunteering experiences """
        volunteerings=[]
        if len(self.xp_volunteerings) > 0:
            for volunteering in self.xp_volunteerings:
                data={}
                data['title']=extract_one(self.get_xp(volunteering, './/h4//text()'))
                data['company']=extract_one(self.get_xp(volunteering, './/h5//text()'))
                data['company_url']=extract_one(self.get_xp(volunteering, './/h5//@href'))
                data['description']=' '.join((self.get_xp(volunteering, './/p[contains(@class,"description")]//text()')))
                data['start_date']=extract_one(self.get_xp(volunteering, './/span[@class = "date-range"]/time[1]/text()'))
                data['end_date']=extract_one(self.get_xp(volunteering, './/span[@class = "date-range"]/time[2]/text()'))
                volunteerings.append(data)
        return volunteerings

    @property
    def organizations(self):
        """ Return a list of dictionnary with organizations """
        organizations=[]
        if len(self.xp_organizations) > 0 :
            for organization in self.xp_organizations:
                data={}
                data['title']=extract_one(self.get_xp(organization, './/h4[@class="item-title"]//text()'))
                data['title_url']=extract_one(self.get_xp(organization, './/h4[@class="item-title"]/a/@href'))
                data['name']=extract_one(self.get_xp(organization, './/h5[@class="item-subtitle"]//text()'))
                data['description']=' '.join((self.get_xp(organization, './/p[contains(@class,"description")]//text()')))
                organizations.append(data)
        return organizations

    @property
    def recommendations(self):
        """ Return a list of dictionnary with organizations """
        recommendations=[]
        if len(self.xp_recommendations) > 0 :
            for recommendation in self.xp_recommendations:
                data = {}
                data['text'] = extract_one(self.get_xp(recommendation, './/blockquote[@class="recommendation"]//text()'))
                recommendations.append(data)
        return recommendations

    @property
    def test_scores(self):
        """ Return a list of dictionnary with test scores """
        if isinstance(self.xp_test_scores, html.HtmlElement) is True:
            count=int(self.get_clean_xpath(
                'count(//div[@id="background-test-scores"]/div[contains(@id, "scores-")])'))
            test_scores=[]
            for i in range(1, count + 1):
                data={}
                data['name']=extract_one(
                    self.get_xp(self.xp_test_scores, './/h4//text()'))
                data['score']=extract_one(
                    self.get_xp(self.xp_test_scores, './/h5//text()'))
                data['description']=' '.join((self.get_xp(
                    self.xp_test_scores, './/p[contains(@class,"description")]//text()')))
                data['date']=extract_one(self.get_xp(
                    self.xp_test_scores, './/span[@class = "date-range"]/time[1]/text()'))
                test_scores.append(data)
        else:
            test_scores=[]
        return test_scores

    @property
    def certifications(self):
        """ Return a list of dictionnary with certifications infos """
        certifications=[]
        if len(self.xp_certifications) > 0:
            for certification in self.xp_certifications:
                data={}
                data['title']=extract_one(self.get_xp(certification, './/h4/a/text()'))
                data['title_url']=extract_one(self.get_xp(certification, './/h4/a/@href'))
                data['company_name']=extract_one(self.get_xp(certification, './/h5/a/text()'))
                data['linkedin_company_url']=extract_one(self.get_xp(certification, './/h5//@href'))
                data['date']=extract_one(self.get_xp(certification, './/span[@class = "date-range"]/time/text()'))
                certifications.append(data)
        return certifications

    @property
    def publications(self):
        """ Return a list of dictionnary with publications details """
        publications = []
        if len(self.xp_publications) > 0:
            for publication in self.xp_publications:
                data={}
                data['title']=extract_one(self.get_xp(publication, './/h4[@class="item-title"]/a/text()'))
                data['title_url']=extract_one(self.get_xp(publication, './/h4[@class="item-title"]/a/@href'))
                data['source']=extract_one(self.get_xp(publication, './/h5[@class="item-subtitle"]//text()'))
                #data['description']=' '.join((self.get_xp(publication, './/p[contains(@class,"description")]//text()')))
                data['date']=extract_one(self.get_xp(publication, './/span[@class = "date-range"]//text()'))
                data['authors']=self.get_xp(publication, './/dl[@class = "contributors"]//li//text()')
                data['authors_linkedin_profile']=self.get_xp(publication, './/dl[@class = "contributors"]//li//@href')
                publications.append(data)
        return publications

    @property
    def similar_profiles(self):
        """ Get a list of dictionnaries of profiles from 'people also viewed' on linkedin """
        similar_profiles = []
        if len(self.xp_similar_profiles) > 0 :
            for profile in self.xp_similar_profiles:
                data={}
                data['url']=extract_one(self.get_xp(profile, './div/h4/a/@href'))
                data['name']=extract_one(self.get_xp(profile, './div/h4/a/text()'))
                data['current_title']=extract_one(self.get_xp(profile, './div/p/text()'))
                data['img_url']=extract_one(self.get_xp(profile, './a/img/@data-li-src'))
                similar_profiles.append(data)
        return similar_profiles



    def to_dict(self):
        data={
        'url': self.url,
        'url_detected': self.url_detected,
        'name': self.name,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'number_connections': self.number_connections,
        'number_recommendations': self.number_recommendations,
        'websites': self.websites,
        'has_profile_picture': self.has_profile_picture,
        'current_education': self.current_education,
        'current_title': self.current_title,
        'current_location': self.current_location,
        'current_industry': self.current_industry,
        'summary': self.summary,
        'recommendations': self.recommendations,
        'experiences': self.experiences,
        'educations': self.educations,
        'project': self.projects,
        'skills': self.skills,
        'courses': self.courses,
        'interests': self.interests,
        'groups': self.groups,
        'languages': self.languages,
        'honors': self.honors,
        'volunteerings': self.volunteerings,
        'organizations': self.organizations,
        'test_scores': self.test_scores,
        'certifications': self.certifications,
        'publications': self.publications,
        'similar_profiles': self.similar_profiles
        }
        return data
