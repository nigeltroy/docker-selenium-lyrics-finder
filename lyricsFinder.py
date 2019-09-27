from selenium import webdriver
import sys
from flask import Flask, request, render_template
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

def retrieveLyrics(songName = 0):
    try:
        if not songName:
            url = 'https://www.google.com/search?q=' + '+'.join(sys.argv[1:]) + '+lyrics'
        else:
            url = 'https://www.google.com/search?q=' + songName.replace(' ', '+') + '+lyrics'

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

        name = driver.find_element_by_xpath("//div[@class='kno-ecr-pt kno-fb-ctx PZPZlf gsmt']").text
        author = driver.find_element_by_xpath("//div[@class='wwUB2c kno-fb-ctx PZPZlf']").text

        '''if not songName:
            name = [i.capitalize() for i in sys.argv[1:]]
        else:
            name = [i.capitalize() for i in songName.split(" ")]'''
    except:
        lyrics = ["Try another input: perhaps your song is too obscure?"]
        name = "No input/no lyrics found"
        author = ""
    
    return [name, lyrics, author]

app = Flask(__name__)

@app.route("/inputSong", methods=["POST"])
def inputSong():
    lyricsIn = request.form['song']
    ans = retrieveLyrics(lyricsIn)
    return render_template('main.html', nam=ans[0], lyr=ans[1], aut=ans[2])

@app.route("/")
def lyricsPrint():
    return render_template('main.html', nam=retrieveLyrics()[0], lyr=retrieveLyrics()[1], aut=retrieveLyrics()[2])

if __name__ == "__main__":
    app.run(host='0.0.0.0')