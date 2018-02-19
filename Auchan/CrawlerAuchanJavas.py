
from selenium import webdriver


auchan_page = 'https://www.auchandirect.fr/produits/222741'

# Open the url in a new browser window
driver = webdriver.Firefox()
driver.get(auchan_page)

# Get the interesting elements by their CSS class
name_element = driver.find_element_by_class_name('LooprArticleDetailsInformation__Title')
price_element = driver.find_element_by_class_name('SparkCurrency')
infos = [name_element.text, price_element.text]

# Print infos
print(infos)
for a in infos:
    print(a)

# Close the browser window
driver.close()

