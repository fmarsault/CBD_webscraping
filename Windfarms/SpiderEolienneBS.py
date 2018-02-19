# Felix Marsault CBD1
# TP Scrapping

import re
import time
import json
import csv
from selenium import webdriver
from bs4 import BeautifulSoup


class SpiderEolienneBS():
    """A class to scrap 4coffshore.com/windfarms/ database"""

    def __init__(self):
        """Initialization of the spider"""
        self.start_url = "http://www.4coffshore.com/windfarms/belwind--belgium-be03.html"
        self.browser = webdriver.Firefox()  # Open new browser window
        self.sleep_time = 0.5

    def url_request(self,url):
        """Make an url request using only Selenium"""
        self.browser.get(url)
        time.sleep(self.sleep_time)  # Waiting to be sure the page is loaded and we are not sending requests too fast.

    def url_request_bs(self, url):
        """Make an url request using Selenium and BS"""
        self.browser.get(url)
        time.sleep(self.sleep_time)  # Waiting to be sure the page is loaded and we are not sending requests too fast.
        html = self.browser.page_source  # Load the page to be read by BS
        soup = BeautifulSoup(html, 'html.parser')  # BS read
        return soup

    def get_countries(self):
        """Find the list of countries and the html code to access them"""
        self.url_request(self.start_url)
        time.sleep(2*self.sleep_time)
        countries = self.browser.find_elements_by_css_selector('option')
        codes = []
        country_names = []
        for country in countries:
            codes.append(country.get_attribute('value'))
            country_names.append(country.text)

        return codes, country_names

    def get_projects(self, soup):
        """Find the url and name of each project for a particular country."""
        projects = soup.find_all('a', {'class': 'linkWF'})  # Find all the project links on this page

        # Initialisation of the for loop
        url_projects = []
        projects_name = []
        for project in projects:
            url_project = project['href']  # Get project url
            project_name = project.find('span').text.strip()  # Get project name
            url_projects.append(url_project)  # Construction of the list
            projects_name.append(project_name)

        # Verification: if several project pages continue to append
        if soup.find('tr', {'class': 'gvwfsPager'}) is not None:
            project_header = soup.find('tr', {'class': 'gvwfsPager'})   # Looking for the pages header
            project_pages = project_header.find_all('a')
            pages = [page.text.strip() for page in project_pages]  # Get the pages number in a list

            # Locate and navigate the clickable page elements with selenium
            for page in pages:
                page_link = self.browser.find_element_by_link_text(page)
                page_link.click()
                time.sleep(self.sleep_time)  # Waiting for the page to load
                html = self.browser.page_source  # Load the page to be read by BS
                soup = BeautifulSoup(html, 'html.parser')  # BS read
                projects = soup.find_all('a', {'class': 'linkWF'})  # Find all the project links on this page
                for project in projects:
                    url_project = project['href']  # Get project url
                    project_name = project.find('span').text.strip()  # Get project name
                    url_projects.append(url_project)  # Construction of the list
                    projects_name.append(project_name)

        else:
            pass
        return url_projects, projects_name

    def crawler(self):
        """Main method, crawl through the entire website and call the scrapper."""
        base_url = "http://www.4coffshore.com"
        codes, country_names = self.get_countries()
        data_project = {}
        self.init_csv('data_eolienne')

        # Navigate through all the country pages
        for idx_country, code in enumerate(codes):
            country_name = country_names[idx_country]
            data_project[country_name] = {}
            print(str(idx_country + 1) + '/' + str(len(codes)))
            print('Country: ' + country_name)

            url_country = base_url + '/windfarms/windfarms.aspx?windfarmId=' + code
            soup = self.url_request_bs(url_country)  # Request the next country url
            # Get the url and name of each project for a country
            url_projects, projects_name = self.get_projects(soup)
            #
            for idx_project, url_project in enumerate(url_projects):
                project_name = projects_name[idx_project]  # Initialize dictionary to store the data
                data_project[country_name][project_name] = {}
                print(str(idx_project + 1) + '/' + str(len(projects_name)))
                print('Project: ' + project_name)
                soup = self.url_request_bs(base_url + url_project)  # Request project url

                try:
                    # Navigate to the SupplyChain url
                    supplychain =soup.find('a', id='ctl00_Body_Page_SubMenu_hypSupplychain')['href']
                    url_supplychain = base_url + '/windfarms/' + supplychain

                    # Scrape through the project page
                    data_project = self.scrapper(url_supplychain, country_name, project_name, data_project)

                    # Append the project data in a csv file
                    self.write_csv(country_name, project_name, data_project)
                except (TypeError, ValueError):
                    print("Page not found!")
                    pass

        self.write_json(data_project)
        return data_project

    def scrapper(self, url_supplychain, country_name, project_name, data_project):
        """Scrap through the project page and return the data in a dictionary"""
        soup = self.url_request_bs(url_supplychain)
        # Find categories of the table
        table = soup.find('section', id='overview')
        categories = table.find_all('a', href='#')
        categories = [re.sub(r'\([^)]*\)', '', ele.text).strip() for ele in categories]  # Clean up

        # Find the list of contractors
        lists = soup.find_all('table', {'class': 'table table-striped'})
        title = soup.find('title')

        # Initialisation of the for loop
        empty_field = 'Be the first to associate your organisation with this Wind farm'

        for idx_list, list in enumerate(lists):
            # Explore the html table
            table_body = list.find('tbody')
            rows = table_body.find_all('tr')
            contractor = {}

            if list.text.strip() != empty_field:
                # Store the values in a dictionary, remove empty fields.
                for row in rows:
                    cols = row.find_all('td')
                    tempcol = [ele.text.strip() for ele in cols]
                    if tempcol != []:
                        if tempcol[0] in contractor:
                            contractor[tempcol[0]].append(tempcol[1])  # Append key= col1 and value= col2
                        else:
                            contractor[tempcol[0]] = [tempcol[1]]  # Create new key= col1 and value= col2
                    else:
                        pass
            else:
                pass
            data_project[country_name][project_name][categories[idx_list]] = contractor

        return data_project

    def write_json(self, data_dict):
        """Write the whole resulting data dictionary in a Json file."""
        with open('scraped_data/data_eolienne.json', 'w+') as outfile:
            json.dump(data_dict, outfile)

    def init_csv(self, filename):
        """Initialize the csv file"""
        file = filename + '.csv'
        with open('scraped_data/' + file, 'w+') as file:
            writer = csv.writer(file)
            # Write a header if the file is empty
            writer.writerow(['Country', 'Project', 'Category', 'Role', 'Organisation'])

    def write_csv(self, country_name, project_name, data_dict):
        """Write data dictionary in a csv file."""
        with open('scraped_data/data_eolienne.csv', 'a') as file:
            writer = csv.writer(file)

            category_list = list(data_dict[country_name][project_name].keys())
            for category in category_list:
                roles = list(data_dict[country_name][project_name][category].keys())
                for role in roles:
                    for org in data_dict[country_name][project_name][category][role]:
                        writer.writerow([country_name, project_name, category, role, org])



eole = SpiderEolienneBS()
data = eole.crawler()
