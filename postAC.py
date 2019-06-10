from bs4 import BeautifulSoup
import requests
import os
import sys
import datetime
from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

contestName = sys.argv[1]
print("AtCoder " + contestName.upper())

# コンテストサイト スクレイピング
url = "https://atcoder.jp/contests/" + contestName.lower()
instance = requests.get(url)
soup = BeautifulSoup(instance.text, 'lxml')
# コンテスト正式名
contestFullName = soup.select_one(
    "#navbar-collapse > ul:nth-child(1) > li > a"
).text

# コンテスト日時
contestDateTimeStr = soup.select_one(
    "#contest-nav-tabs > div > small.contest-duration > a:nth-child(1) > time"
).text
contestDateTime = dt.strptime(contestDateTimeStr, '%Y-%m-%d %H:%M:%S%z')

# post作成
today = datetime.date.today()
filePass = "post/" + \
    str(today.year) + "/" + str(today.month).zfill(2) + \
    "/" + contestName.lower()
fileName = contestFullName.replace(' ', '_') + "_参加記録.md"

os.system("hugo new " + filePass + "/" + fileName)

# 読み込み
md = open("content/" + filePass + "/" + fileName, "r")
data = md.readlines()
md.close()

# tags上書き
md = open("content/" + filePass + "/" + fileName, "w")
data[4] = "tags: [競技プログラミング, AtCoder]\n"
md.writelines(data)
md.close()

# レートグラフ取得
imgFileName = "ratingGraph.png"
# ブラウザのオプションを格納する変数
options = Options()
# Headlessモードを有効にする
options.set_headless(True)
# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)
# ブラウザでアクセスする
driver.get("https://atcoder.jp/users/heysan")
driver.set_window_size(1000, 1000)
element = driver.find_element_by_css_selector(
    "#main-container > div.row > div.col-sm-9 > div"
)
graphLocation = element.location
graphSize = element.size
# macのRetinaディスプレイだと、2倍のサイズでスクショが撮れる
graphBox = (
    graphLocation['x'] * 2,
    graphLocation['y'] * 2,
    graphLocation['x'] * 2 + graphSize['width'] * 2,
    graphLocation['y'] * 2 + graphSize['height'] * 2
)
driver.save_screenshot("content/" + filePass + "/" + imgFileName)
# ドライバーを終了
driver.close()
# クロップ
im = Image.open("content/" + filePass + "/" + imgFileName)
im = im.crop(graphBox)
im.save("content/" + filePass + "/" + imgFileName)

# テキスト追加
md = open("content/" + filePass + "/" + fileName, "a")
txt = "\n先日（" + dt.strftime(contestDateTime, '%Y/%m/%d') + "）、" + \
    "AtCoderで開催された[" + contestFullName + \
    "](" + url + ")に参加しました。" + \
    "\n\n<!--more-->\n\n![レートグラフ](" + imgFileName + ")\n\n\n---\n\n"
md.writelines(txt)
md.close()


# 問題一覧 スクレイピング
instance2 = requests.get(url + "/tasks")
soup2 = BeautifulSoup(instance2.text, 'lxml')
table = soup2.find("table")
rows = table.findAll("a")
links = []
for a in rows:
    links.append("https://atcoder.jp" + a.get("href"))
links = list(set(links))
links.sort()
# 各問題 スクレイピング
for problemURL in links:
    instance3 = requests.get(problemURL)
    soup3 = BeautifulSoup(instance3.text, 'lxml')
    Title = soup3.select_one(
        "#main-container > div.row > div:nth-child(2) > span")
    Point = soup3.select_one("#task-statement > span > span.lang-ja > p")
    TimeRestriction = soup3.select_one(
        "#main-container > div.row > div:nth-child(2) > p")
    Q = soup3.select_one(
        "#task-statement > span > span.lang-ja > div:nth-child(2) > section"
    )
    R = soup3.select_one(
        "#task-statement > span > span.lang-ja > div:nth-child(3) > section"
    )
    # テキスト追加
    md = open("content/" + filePass + "/" + fileName, "a")
    txt = "> ## " + Title.text + "\n"
    txt += "> " + Point.text + "\n"
    txt += "> " + TimeRestriction.text + "\n"
    txt += ">"

    strQ = str(Q)
    strQ = strQ.replace('<var>', '$')
    strQ = strQ.replace('</var>', '$')
    strQ = strQ.replace('<code>', '`')
    strQ = strQ.replace('</code>', '`')
    strQ = strQ.replace('<strong>', '**')
    strQ = strQ.replace('</strong>', '**')
    strQ = strQ.replace('_', '\\_')
    strQ = strQ.replace('<li>', '- ')
    strQ = strQ.replace('</li>', '')
    strQ = strQ.replace('<ul>', '\n')
    strQ = strQ.replace('</ul>', '')
    strQ = strQ.replace('<ol>', '\n')
    strQ = strQ.replace('</ol>', '')
    strQ = strQ.replace('<p>', '\n')
    strQ = strQ.replace('</p>', '\n')
    strQ = strQ.replace('<h3>', '### ')
    strQ = strQ.replace('</h3>', '\n ')
    strQ = strQ.replace('<section>', '')
    strQ = strQ.replace('</section>', '')
    strQ = strQ.replace('\n\n', '\n')
    strQ = strQ.replace('\n', '\n> ')
    txt += strQ

    strR = str(R)
    strR = strR.replace('<var>', '$')
    strR = strR.replace('</var>', '$')
    strR = strR.replace('<code>', '`')
    strR = strR.replace('</code>', '`')
    strR = strR.replace('<strong>', '**')
    strR = strR.replace('</strong>', '**')
    strR = strR.replace('_', '\\_')
    strR = strR.replace('<li>', '- ')
    strR = strR.replace('</li>', '')
    strR = strR.replace('<ul>', '\n')
    strR = strR.replace('</ul>', '')
    strR = strR.replace('<ol>', '\n')
    strR = strR.replace('</ol>', '')
    strR = strR.replace('<p>', '\n')
    strR = strR.replace('</p>', '\n')
    strR = strR.replace('<h3>', '### ')
    strR = strR.replace('</h3>', '\n ')
    strR = strR.replace('<section>', '')
    strR = strR.replace('</section>', '')
    strR = strR.replace('\n\n', '\n')
    strR = strR.replace('\n', '\n> ')
    txt += strR

    txt += "> <cite> [" + \
        contestName.upper() + " " + Title.text + \
        "](" + problemURL + ")</cite>\n"

    txt += "\n"
    txt += "\n"
    txt += "\n"
    txt += "\n---"
    txt += "\n"

    md.writelines(txt)
    md.close()
