
#import libraries

import csv, time, codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#define program variables

webAddress = 'https://www.zomato.com'

location = 'pune'
locationClass = 'l-pre-1'
locationId = 'location_input'

restaurant = 'McDonald\'s'
keywordId = 'keywords_input'

resultTitle = 'a.result-title'
nextPage = '.next.item'

resultName = '.res-name a'
resultTel = 'tel'
resultAddress = 'resinfo-icon'
resultReviewer = '.res-review-body .header a'
resultReviewerScore = '.res-review-body .ttupper'
resultReview = '.rev-text'



#launch browser
browser=webdriver.Firefox()
browser.get(webAddress)
#delay till page render
time.sleep(5)

#find location element and click on it to activate input tag
locationElement = browser.find_element_by_class_name(locationClass)
locationElement.click()

#send location value to the input tag
locationel = browser.find_element_by_id(locationId)
locationel.send_keys(location)
#delay for location search to stabilize
time.sleep(3)
#select first location suggestion
locationel.send_keys(Keys.DOWN)
locationel.send_keys(Keys.ENTER)
#delay location URL rendering
time.sleep(3)

#provide the restaurant name
keyword = browser.find_element_by_id(keywordId)
keyword.send_keys(restaurant)
#delay for keyword seach to stabilize
time.sleep(3)
keyword.send_keys(Keys.DOWN)
keyword.send_keys(Keys.ENTER)
#wait for search results to render
time.sleep(3)

#extract links for outlets
outlets = list(browser.find_elements_by_css_selector(resultTitle))
#extract URL using href attributes
links = [outlet.get_attribute('href') for outlet in outlets]
time.sleep(5)

#select next page to extract remaining results
nextPageBtn = browser.find_element_by_css_selector(nextPage)
while ('disabled' not in nextPageBtn.get_attribute('class').split(' ')):
    nextPageBtn.click()
    time.sleep(2)
    outlets = list(browser.find_elements_by_css_selector(resultTitle))
    currentlinks = [outlet.get_attribute('href') for outlet in outlets]
    #update link list
    links.extend(currentlinks)
    nextPageBtn = browser.find_element_by_css_selector(nextPage)

#open file to write the output, codecs is used to handle special characters
outputFile = codecs.open('result_set.csv','w','utf-8')
outputWriter=csv.writer(outputFile)
#write header in the file
outputWriter.writerow(['Name','phone','address','The first reviewers Name','The first reviewers Score','The review text','The page link'])

#extract information for each outlets
for link in links:
    #wait for new outlet URL to load
    time.sleep(2)
    browser.get(link)
    Name = browser.find_element_by_css_selector(resultName).text
    Phone = browser.find_element_by_class_name(resultTel).text
    Address = browser.find_element_by_class_name(resultAddress).text
    reviewerName = browser.find_element_by_css_selector(resultReviewer).text
    reviewScore = browser.find_element_by_css_selector(resultReviewerScore).get_attribute('aria-label')
    review = browser.find_element_by_css_selector(resultReview).text[8:-12]
    outputWriter.writerow([Name, Phone, Address, reviewerName, reviewScore, review, link])
    
#close file handler
outputFile.close()
#close browser
browser.close()
