from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    #time.sleep(1) is this needed?

    #scrape page into soup
    soup = bs(browser.html, "html.parser")

    all_titles = soup.find_all(name='div', class_='content_title')
    news_title = all_titles[1].text.strip()

    all_paragraph = soup.find_all(name='div', class_='article_teaser_body')
    news_p = all_paragraph[0].text.strip()

    #Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    soup = bs(browser.html, 'html.parser')

    img_url = soup.find('article', class_='carousel_item')['style'].replace('background-image: url(','').replace(');','')[1:-1]

    main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = (main_url + img_url)

    #Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    df = tables[0]

    mars_df = df.to_html(classes= 'dataframe')


    #Mars Hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    soup = bs(browser.html, 'html.parser')

    items = soup.find_all(name='div', class_='item')

    #Create empty list
    hempishere_image_urls = []

    #Store main url
    main_url = 'https://astrogeology.usgs.gov'

    #Create loop
    for x in items:
        #find titles
        title = x.find('h3').text
    
        #pull partial img url from main page
        partial_img_url = x.find('a', class_='itemLink product-item')['href']
    
        #Go to link that has the full image
        browser.visit(main_url + partial_img_url)
    
        #Create new soup
        soup = bs(browser.html, 'html.parser')
    
        #Get full image source
        img_url = main_url + soup.find('img', class_='wide-image')['src']
    
        #Append the img names and links to a list of dicts
        hempishere_image_urls.append({"titles": title, "img_url": img_url})


    mars_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image': featured_image_url,
        'mars_facts': mars_df,
        'titles': title,
        'img_url': img_url
    }

    browser.quit()
    
    #print(mars_dict)
    return mars_dict
