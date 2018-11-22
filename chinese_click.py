import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Browser
path = '/Users/martin/Documents/codingnomads/nlpython/_onwards/click/'
driver = webdriver.Chrome(f"{path}chromedriver")
driver.get('http://newssearch.chinadaily.com.cn/en/search?query=trade%20war')

link_bucket = []  # a bucket to collect all our links
num_pages = 5  # define here how many pages shall be scraped

# get the first click on "NEXT". has a different path than the following ones
first_next_path = "/html[1]/body[1]/div[5]/div[2]/div[5]/div[1]/div[2]/span[1]/a[5]"
next_next_paths = "/html[1]/body[1]/div[5]/div[2]/div[5]/div[1]/div[2]/span[1]/a[6]"

# first time round!
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, first_next_path)))
next_button = driver.find_element_by_xpath(first_next_path)
next_button.click()  # clicking button

for _ in range(num_pages):
    # waiting to find element.
    # this might have to be improved to wait for an element that is
    # only present once all the links on the page are loaded. otherwise
    # the scraper might not fetch all the links on the page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_next_paths)))
    next_button = driver.find_element_by_xpath(next_next_paths)
    next_button.click()  # clicking button
    # quick fix to make it more likely that the relevant links are loaded
    # TODO: make sure all links are there before fetching them
    time.sleep(1)
    try:
        # we only want the links, which means searching for the href
        # attribute on all <a> tags
        elem = driver.find_elements_by_xpath("//a")
        for e in elem:
            link_bucket.append(e.get_attribute("href"))
    except Exception as e:
        print(e)

# TODO: tweak the section on filtering the right web addresses either
# with regular expressions with python string methods. e.g.:
# * ends with htm or html
# * etc.
p = re.compile(r"https?://www")  # matches both http and https
links = set([link for link in link_bucket if re.match(p, link)])

# creating a CSV string to write to file
out_string = ""
for link in links:
    out_string += link + ",\n"

with open("links.csv", 'w') as fout:
    fout.write(out_string)

driver.quit()  # close the webdriver session
