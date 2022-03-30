from flask import Flask, render_template
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
#import pandas as pd

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

app = Flask(__name__)

@app.route("/scrape")
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    results = soup.find('div', id='news')


    for result in results:
        title = soup.find('div', class_='content_title').text
        article = soup.find('div', class_='article_teaser_body').text


    url = "https://spaceimages-mars.com"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    results = soup.find('div', class_='header')

    for result in results: 
        featured_image = soup.find('img', class_='headerimage fade-in')

    featured_image_url = url + '/' + featured_image.get('src')


    url = "https://galaxyfacts-mars.com"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    results = soup.find('table', class_='table')



    mars_data = results.find_all('span', class_='orange')
    row_names = results.find_all('th', scope='row')

    facts = []
    rows = []

    for row in mars_data:
        facts.append(row.text)
    for row in row_names:
        rows.append(row.text)


    #mars_df = pd.DataFrame({
    #    'Mars Stats' : rows[1:],
    #    '' : facts[1:]
    #})

    #mars_df.set_index('Mars Stats', inplace=True)
    #mars_df


    #mars_df.to_html('Mars_Table.html')


    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    results = soup.find_all('div', class_='item')

    hemispheres = []
    hemisphere_titles = []

    for result in results:
        hemi_path = result.find('a', class_='itemLink').get('href')
        hemispheres.append(hemi_path)
        hemisphere_titles.append(result.find('h3').text.rsplit(' ', 1)[0])


    hemisphere_img_links = []

    for hemisphere in hemispheres:
        hemi_url = url + hemisphere
        browser.visit(hemi_url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')

        downloads = soup.find('div', class_='downloads')
        full_img = downloads.find('a', target='_blank').get('href')
        full_img_url = url + full_img
        hemisphere_img_links.append(full_img_url)


    hemi_images = []

    for x in range(len(hemispheres)):
        hemi_dict = {
            'title': hemisphere_titles[x],
            'img_url': hemisphere_img_links[x]
        }
        hemi_images.append(hemi_dict)

    scraped_data = {
        'headline_title': title,
        'headline_article': article,
        'featured_img': featured_image_url,
        'hemispheres': hemi_images
    }

    return scraped_data

db = client.scrapeDB
scrape_results = db.scrape_results.find()
db.scrape_results.insert_one(scrape())

@app.route("/")
def home():
    final_data = scrape_results
    return render_template('index.html',final_data=final_data)
    

if __name__ == "__main__":
    app.run(debug=True)


#'headline_title': title,
#'headline_article': article,
#'featured_img': featured_image_url,
#'hemispheres': hemi_images