# Import 
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver


# Defining scrape

def scrape():
    # 
    browser = Browser('chrome', headless=False)
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    time.sleep(2)
    # 
    html = browser.html
    soup = bs(html, 'html.parser')
    # 
    item_list = soup.find("ul", class_="item_list")
    category = item_list.find("li", class_="slide")
    # 
    latest_news_title = category.find("div", class_="content_title").get_text()
    latest_paragraph = category.find("div", class_="image_and_description_container").get_text()
    # 
    mars = {
        "Latest_News_Title": latest_news_title,
        "Information": latest_paragraph
    }
    # ### JPL Mars Space Images - Featured Image
    # 
    browser = Browser('chrome', headless=False)
    url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_featured)
    time.sleep(3)
    # 
    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
        articles = soup.find('a', class_='button fancybox')
        browser.click_link_by_partial_text('FULL')
        time.sleep(3)
    xpath = '//*[@id="fancybox-lock"]/div/div[1]/img'
    results = browser.find_by_xpath(xpath)
    link = results['src']
    # 
    mars["Feature_Image_Link"] = link
    # 
    browser = Browser('chrome', headless=False)
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(2)
    # 
    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
        tweets = soup.find_all('div', class_='js-tweet-text-container')[0]
        mars_weather = tweets.get_text()
        mars["Mars_Weather"] = mars_weather
    # ### Mars Facts
    # 
    browser = Browser('chrome', headless=False)
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(2)
    # 
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    # 
    mars_facts_df = df.rename(index=None, columns={0: "Mars_Planet_Profile", 1: "table_info"})
    # 
    planet_profile = mars_facts_df["Mars_Planet_Profile"]
    planet_variables = mars_facts_df["table_info"]
    final_facts = zip(planet_profile, planet_variables)
    # 
    for x, y in final_facts:
        mars[x] = y
    # ### Mars Hemisperes
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # * Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    browser = Browser('chrome', headless=False)
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    time.sleep(2)
    # looping through to print the text given to the full resolution image
    for x in range(1):
        title=[]
        img_url = []
        html = browser.html
        soup = bs(html, 'html.parser')
        div = soup.find('div', class_='collapsible results')
        h3 = div.find_all('h3')
        for x in h3:
            title.append(x.text)
        # Clicking the link to the specific hemisphere
        for x in range(len(title)):
            browser.click_link_by_partial_text(title[x])
            # Waiting two seconds for page to load     
            time.sleep(2)
            # xpath to full res image
            xpath = '//*[@id="wide-image"]/img'
            results = browser.find_by_xpath(xpath)
            # naming the link and printing the result
            link = results['src']
            img_url.append(link)
            # clicking back in the browser to the main page
            browser.click_link_by_partial_text("Back")
            time.sleep(2)
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    mars["title"] = title
    mars["img_url"] = img_url

    # mars = {}
    # for i in range(len(title)):
    #     mars['title'] = title[i]
    #     mars['img_url'] = img_url[i]


    return mars
