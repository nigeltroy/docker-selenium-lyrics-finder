from selenium import webdriver
import sys
from flask import Flask
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

url = 'https://www.google.com/search?q=' + '+'.join(sys.argv[1:]) + '+lyrics'

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1420,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
driver.get(url)

expand_button = driver.find_element_by_xpath("//div[@class='vk_ard']")
expand_button.click() # simulate click to expand lyrics

lyrics = [i.text for i in driver.find_elements_by_xpath("//span[@jsname='YS01Ge']")]

app = Flask(__name__)

@app.route("/")
def lyricsPrint():
    html = "<h3>Lyrics of song: {name}</h3>" \
            "{lyr}"
    return html.format(name=' '.join([i.capitalize() for i in sys.argv[1:]]), lyr='<br>'.join(lyrics))

if __name__ == "__main__":
    app.run(host='0.0.0.0')