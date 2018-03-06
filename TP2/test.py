import re
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import csv

############### Test  data file json ############################

with open('scraped_data/data_eolienne.json', 'r') as json_data:
    data_dict = json.load(json_data)

# with open('scraped_data/data_eolienne.csv', 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)



"""Initialize the csv file"""
file = 'data_eolienne_test' + '.csv'
with open('scraped_data/' + file, 'w+') as file:
    writer = csv.writer(file)
    # Write a header if the file is empty
    writer.writerow(['Country', 'Project', 'Developers/Owners/Operators', 'Turbines', 'Substations', 'Foundations',
                     'Array Cabling', 'Export Cabling', 'Met Masts', 'Consultants', 'Others'])


"""Write data dictionary in a csv file."""
with open('scraped_data/data_eolienne_test.csv', 'a') as file:
    writer = csv.writer(file)

    country_name = 'Vietnam'
    project_name = 'Windpark Phu Cuong 800MW  - 200MW phase 1 (intertidal)'

    country_names = list(data_dict.keys())
    for country_name in country_names:
        project_names = list(data_dict[country_name].keys())
        for project_name in project_names:
            category_list = list(data_dict[country_name][project_name].keys())
            columns = []
            for idx_cat, category in enumerate(category_list):
                roles = list(data_dict[country_name][project_name][category].keys())
                interm_columns = []
                for role in roles:
                    for org in data_dict[country_name][project_name][category][role]:
                        interm_columns.append("{}: {}\n".format(role, re.split('\n', org)[0]))
                columns.append(''.join(interm_columns))

            try:
                # print(''.join(columns))
                writer.writerow([country_name, project_name, columns[0], columns[1], columns[2], columns[3],
                                 columns[4], columns[5], columns[6], columns[7], columns[8]])
            except IndexError:
                print("Data missing in {} for the project: {}".format(country_name, project_name))
                pass

# d = var = {"Belgium": {"SeaStar": {"Developers/Owners/Operators": {"Developer": [
#     "Seastar NV\n\n\nSeastar NV is owned by a consortium of Otary,Elicio Offshore NV, Rent-a-Port, DEME NV, SRIW Environment, Aspiravi\u00a0 Offshore NV, Z\u2010kracht NV, Power@Sea NV and Socofe NV"],
#                                                                    "Owner": [
#                                                                        "Aspiravi Offshore NV (Aspiravi Holding NV)\n\n\nAspiravi Offshore NV own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "Rent-A-Port Energy n.v. (Rent-A-Port n.v.)\n\n\nRent-A-Port Energy n.v. own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "DEME NV\n\n\nDEME NV own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "SRIW Environment\n\n\nSRIW Environment, NV own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "Socofe\n\n\nSocofe NV own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "Z-kracht (Nuhma)\n\n\nZ-kracht own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "Power@Sea NV\n\n\nPower@Sea NV own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "Elicio Offshore (formally Electrawinds Offshore NV) (Elicio nv (formerly Electrawinds NV))\n\n\nElicio NV own 12.5% of project with its share in Seastar NV and 12.5% share of Otary.",
#                                                                        "Otary RS N.V.\n\n\nThe Otary partnership consists of 8 Belgian companies each having a 12.5% share (Elicio, Rent-a-Port, DEME NV, SRIW Environment, Aspiravi\u00a0 Offshore NV, Z\u2010kracht NV, Power@Sea NV and Socofe NV)"]},
#                                    "Turbines": {}, "Substations": {}, "Foundations": {}, "Array Cabling": {},
#                                    "Export Cabling": {}, "Met Masts": {}, "Consultants": {"Consultant-Financial": [
#         "Green Giraffe\nClient: Upgrade\n\n\nProvided financial modelling services (both at project level and holding level) and early phase development services (bankability assessment of the newly proposed subsidy system, strategic advice and assistance in the WTG selection process)."]},
#                                    "Others": {}}}}
# with open('data_eolienne.csv', 'w+') as file:
#     # writer = csv.writer(file)
#     # # Write a header if the file is empty
#     # test = [row for row in csv.DictReader(file)]
#     # if len(test) == 0:
#     #     writer.writerow(['Country', 'Project', 'Category', 'Role', 'Organisation'])
#     #     print('Empty file !!!!!!!!!!!!!!!!!!!!!!')
#     # else:
#     #     pass
#     # # writer.writerow(['Country', 'Project', 'Category', 'Role', 'Organisation'])
#     csvreader = csv.reader(file)
#     for row in csvreader:
#         print(row)
#         if row[0] is (None, ""):
#             print("12")
#
#
#
#
#     country_list = list(d.keys())  # Country as a list
#     country = country_list[0]  # Country as a string
#
#     project_list = list(d[country].keys())  # Project as a list
#     project = project_list[0]  # Project as a string
#
#     category_list = list(d[country][project].keys())
#
#     for category in category_list:
#         roles = list(d[country][project][category].keys())
#         for role in roles:
#             for org in d[country][project][category][role]:
#                 print(org)
#                 writer.writerow([country, project, category, role, org])
#
# with open('test2.csv', 'w+') as file:
#     a = [row for row in csv.DictReader(file)]
#     if a == []:
#         print('Empty file')
#     else:
#         pass


# # url = 'http://www.4coffshore.com/windfarms/windfarms.aspx?windfarmId=CA26'
# url = 'http://www.4coffshore.com/windfarms/contracts-on-star-of-the-south-energy-project-au02.html'
#
# # header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
# # proxy = {"https": "https//190.19.32.132:80"}
#
# browser = webdriver.Firefox()  # Open new browser window
# browser.get(url)
# time.sleep(6)  # Waiting to be sure the page is loaded and we are not sending requests too fast.
# html = browser.page_source  # Load the page to be read by BS
# soup = BeautifulSoup(html, 'html.parser')  # BS read



# ################# Method get_projects ###################################
# projects = soup.find_all('a', {'class': 'linkWF'})
# url_projects = []
# projects_name = []
# for project in projects:
#     url_project = project['href']
#     project_name = project.find('span').text.strip()
#     print(url_project + '\n' + project_name)
#     url_projects.append(url_project)
#     projects_name.append(project_name)
#
# if soup.find('tr', {'class': 'gvwfsPager'}) is not None:
#     project_header = soup.find('tr', {'class': 'gvwfsPager'})
#     project_pages = project_header.find_all('a')
#     pages = [page.text.strip() for page in project_pages]
#
#     for page in pages:
#         page_link = browser.find_element_by_link_text(page)
#         page_link.click()
#         time.sleep(3)
#         html = browser.page_source  # Load the page to be read by BS
#         soup = BeautifulSoup(html, 'html.parser')  # BS read
#         projects = soup.find_all('a', {'class': 'linkWF'})
#         for project in projects:
#             url_project = project['href']
#             project_name = project.find('span').text.strip()
#             print(url_project + '\n' + project_name)
#             url_projects.append(url_project)
#             projects_name.append(project_name)
#
# else:
#     pass
# ##############################################################################


# ######### Method scrapper #########################
# # Find categories of the table
# table = soup.find('section', id='overview')
# categories = table.find_all('a', href='#')
# categories = [re.sub(r'\([^)]*\)', '', ele.text).strip() for ele in categories] # Clean up
#
# # Find the list of contractors
# lists = soup.find_all('table', {'class': 'table table-striped'})
# title = soup.find('title')
#
# # Initialisation of the for loop
# empty_field = 'Be the first to associate your organisation with this Wind farm'
# country_name = 'Country PlaceHolder'
# project_name = 'Project PlaceHolder'
# data_country = {}
# data_country[country_name] = {}
# data_country[country_name][project_name] = {}
#
# for idx_list, list in enumerate(lists):
#     # Explore the html table
#     table_body = list.find('tbody')
#     rows = table_body.find_all('tr')
#     contractor = {}
#
#     if list.text.strip() != empty_field:
#         # Store the values in a dictionary, remove empty fields.
#         for row in rows:
#             cols = row.find_all('td')
#             tempcol = [ele.text.strip() for ele in cols]
#             if tempcol != []:
#                 if tempcol[0] in contractor:
#                     contractor[tempcol[0]].append(tempcol[1])  # Append key= col1 and value= col2
#                 else:
#                     contractor[tempcol[0]] = [tempcol[1]]  # Create new key= col1 and value= col2
#             else:
#                 pass
#     else:
#         pass
#
#     data_country[country_name][project_name][categories[idx_list]] = contractor
#
#     # print(list.text.strip())
# #################################################################