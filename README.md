# scrape-linkedin
Linkedin scraper to get all details on public linkedin profiles.


## Introduction

Linkedin recently changed its api policy and put more limitation on the use of their api's

Some precautions you should take if you want scrape linkedin with python :
* Change the default python requests user-agent for a browser user-agent like "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

* By default Linkedin has black listed the ip from AWS instances by responding with a non standard http status `999` to the requests. Same for Heroku (they are using aws instances), you can try digital ocean instances.

* If your are scraping a lot of profiles add a random delay between requests

* You can use proxies if you want to do concurrent requests you can free proxy [here](http://proxylist.hidemyass.com/) (nevertheless free proxies are slow and are often failing a lot)

## Installation

### Install from source
`git clone https://github.com/ericfourrier/scrape-linkedin.git`
go to repo directory and run from the command line `python setup install`


### Using this package

It relies on two class:

`CustomRequest` which is just a way to customise your http request specifying a list of user-agents or proxies.

    c = CustomRequest() # default with rotating proxies
    c = CustomRequest(rotating_ua = False) # without rotating proxies
    c = CustomRequest(list_proxies=[{'https':'http://186.233.94.106:8080','https':'http://186.233.94.106:8080'}]))

`LinkedinItem` is the main class, you can instantiate it with the url or with the response.


    l = LinkedinItem(url = 'https://www.linkedin.com/in/kennethreitz')
    l - LinkedinItem(html_string = profile_string)


'LinkedinItem' has the folowing syntax the get the info :

    l.get_name() # to get the name
    l.get_skills() # to get the skills
    l.get_publications()  # to get the publications
    # etc
    # the most important
    l.to_dict() to scrape all the infos in the profile with a dictionnary format


### Exhaustive list of the fields scraped

  [volunteerings, last_name, number_recommendations, number_connections, current_location, honors, first_name, current_title, test_scores, current_industry, languages, similar_profiles, interests, profile_img_url, current_education, educations, experiences, groups, organizations, certifications, name, skills, websites, summary, project, courses, publications,recommendations]
