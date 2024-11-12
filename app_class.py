import re
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# class MaruMaru(Web):
#     def search_songs(self, song_name):
#         headers = {
#             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
#                         (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'}
#         form_data = {
#             'keyword': 'flos',
#             'KW': 'flos',
#             'SongType': '',
#             'Singer': '',
#             'FormatType': '' ,
#             'AvgScore': '',
#             'OrderBy': '',
#             'MySong': '',
#             'Page': '1'}
#         session = requests.Session()
#         driver = session.post("https://www.jpmarumaru.com/tw/jp-song-list.html", params = form_data, cookies = {'receive-cookie-deprecation':'1'}, headers=headers)
#         data = BeautifulSoup(driver.text, "html.parser")
#         pass
#         print(driver)

#     def search_lyrics(self, url):
#         pass

# class MusicLyrics(Web):
#     def search_songs(self, song_name):
#         driver = requests.get("https://www.musicenc.com/?search="+ song_name)
#         data = BeautifulSoup(driver.text, "html.parser")
#         self.urls = [d.find("a").get("dates") for d in data.find_all("li", limit=11)[1:]]
#         self.songs = [d.find("a").text.replace("\xa0"," ") for d in data.find_all("li", limit=11)[1:]]
#         self.singers = [d.find("span").text.replace("[","").replace("]","").replace("\xa0"," ") for d in data.find_all("li", limit=11)[1:]]

#     def search_lyrics(self, url):
#         driver = requests.get("https://www.musicenc.com/searchr/?token="+ url).content.decode('utf-8')
#         data = BeautifulSoup(driver, "html.parser")
#         lyric = str(data.find('div', {'class':'content'}))
#         lyric = re.search('(<div class="content"> )(.*)(</div>)', lyric).group(2)
#         lyric = re.sub('<br/>', '\n', lyric)
#         return lyric

class UtaMap():
    def search_songs(self, song_name):
        driver = requests.get("https://www.utamap.com/searchkasi.php?searchname=title&word="+ song_name +"&act=search&search_by_keyword=%8C%9F%26%23160%3B%26%23160%3B%26%23160%3B%8D%F5&sortname=1&pattern=1")
        data = BeautifulSoup(driver.text, "html.parser")
        data = data.find_all("tr", bgcolor="#ffffff", limit=10)
        urls = [d.find("a").get("href") for d in data]
        songs = [d.find("a").text for d in data]
        singers = [d.find("td", class_="ct120").text for d in data]
        data = [{'url': url, 'song': song, 'singer': singer} for url, song, singer in zip(urls, songs, singers)]
        return data

    def search_lyrics(self, url):
        driver = requests.get("https://www.utamap.com/"+url)
        data = BeautifulSoup(driver.text, "html.parser")
        lyric = str(data.find('td', {'class':'noprint kasi_honbun'}))
        lyric = re.sub('\n', '', lyric)
        lyric = re.search('(?<=style="padding-left:30px;">)(.*)(?=<!-- 歌詞 end -->)', lyric)
        if lyric != None:
            lyric = lyric.group()
            lyric = re.sub('<br/>', '\n', lyric).strip()
        else:
            lyric = "No Lyrics"
        return lyric

class UtaNet():
    def search_songs(self, song_name):
        driver = requests.get("https://www.uta-net.com/search/?Keyword="+ song_name +"&Aselect=2&Bselect=3")
        data = BeautifulSoup(driver.text, "html.parser")
        
        urls = [d.get("href") for d in data.find_all("a", class_="py-2 py-lg-0", limit=10)]
        songs = [d.text for d in data.find_all("span", class_="fw-bold songlist-title", limit=10)]
        singers = [d.text for d in data.find_all("span", class_="d-block d-lg-none utaidashi", limit=10)]
        data = [{'url': url, 'song': song, 'singer': singer} for url, song, singer in zip(urls, songs, singers)]
        return data

    def search_lyrics(self, url):
        driver = requests.get("https://www.uta-net.com/"+ url)
        data = BeautifulSoup(driver.text, "html.parser")
        lyric = str(data.find("div", {"id":"kashi_area"}))
        lyric = re.search('(?<=">)(.*)(?=</div>)', lyric)
        if lyric != None:
            lyric = lyric.group()
            lyric = re.sub('<br/>', '\n', lyric).strip()
        else:
            lyric = "No Lyrics"
        return lyric

class UtaTen():
    # 有平假名
    def search_songs(self, song_name):
        driver = requests.get("https://utaten.com/search?sort=popular_sort_asc&artist_name=&title="+ song_name +"&beginning=&body=&lyricist=&composer=&sub_title=&tag=&show_artists=1")
        data = BeautifulSoup(driver.text, "html.parser")
 
        urls = [d.find('a').get('href') for d in data.find_all("p", class_="searchResult__title", limit=10)]
        songs = [d.text.replace('\n','').strip() for d in data.find_all("p", class_="searchResult__title", limit=10)]
        singers = [d.text.replace('\n','').strip() for d in data.find_all("p", class_="searchResult__name", limit=10)]
        data = [{'url': url, 'song': song, 'singer': singer} for url, song, singer in zip(urls, songs, singers)]
        return data

    def search_lyrics(self, url):
        driver = requests.get("https://utaten.com/"+ url)
        data = BeautifulSoup(driver.text, "html.parser")
        lyric = str(data.find("div", class_="hiragana"))
        if lyric != None:
            lyric = re.sub('\n', '', lyric)
            lyric = re.search('(?<=<div class="hiragana">)(.*)(?=</div>)', lyric)
            lyric = lyric.group()
            lyric = re.sub('</span><span class="rt">','(', lyric)
            lyric = re.sub('</span></span>',')', lyric)
            lyric = re.sub('<span class="ruby"><span class="rb">','', lyric)
            lyric = re.sub(r'<br/>|</br>|<br>','\n', lyric).strip()
            pass
        else:
            lyric = "No Lyrics"
        return lyric
    
class KKBox():

    def __init__(self):
        ChromeDriverManager().install()
        chrome_options = Options()
        chrome_options.add_argument("--headless")#使用無頭模式
        chrome_options.add_argument("--disable-notifications")#關閉彈出視窗
        self.driver = webdriver.Chrome(options=chrome_options) # 透過webdriver-manager自動完成配置位置

    def search_songs(self, song_name):
        self.driver.get("https://www.kkbox.com/tw/tc/search?q="+ song_name)
        # 滾動頁面以便加載更多內容
        for _ in range(5):  # 可以根據需求調整滾動次數
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "song-li"))
            )
        # 等待直到內容完全加載
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "song-li"))
        )
        data = self.driver.find_elements(By.TAG_NAME, "song-li")
        urls = [d.find_element(By.CSS_SELECTOR, '[slot="song-name"]').get_attribute('href') for d in data]
        songs = [d.find_element(By.CSS_SELECTOR, '[slot="song-name"]').get_attribute('title') for d in data]
        singers = [d.find_element(By.CSS_SELECTOR, '[slot="artist-name"]').get_attribute('title') for d in data]
        data = [{'url': url, 'song': song, 'singer': singer} for url, song, singer in zip(urls, songs, singers)]
        return data

    def search_lyrics(self, url):
        self.driver.get(url)
        page_source = self.driver.page_source
        html_text = BeautifulSoup(page_source, "html.parser")
        lyric = html_text.find("div", class_="lyrics").find_all("p")[-1].text
        if lyric != None:
            return lyric
        else:
            lyric = "No Lyric"    
        return lyric



# app = KKBox()
# data = app.search_songs("初音")
# print(data)
# print(app.search_lyrics(data[0]['url']))