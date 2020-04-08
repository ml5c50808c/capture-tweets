from selenium import webdriver
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

# location = r'C:\파일경로' # 파일경로
# chromedriver = r'C:\크롬드라이버경로\chromedriver.exe' # 크롬 드라이버 경로
# id_ = 'comewithmesir' # 아이디

location = input('사진 저장할 파일경로 : ')
chromedriver = input('크롬 드라이버경로 : ')
id_ = input('아이디 : ')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(
    chromedriver, options=chrome_options)
driver.get('https://twitter.com/'+id_)

sleep(7)

top = driver.find_element_by_css_selector(
    'header.css-1dbjc4n.r-1g40b8q').size['height']
bottom = driver.get_window_size()['height']

articles = driver.find_elements_by_tag_name('article')

previous = []
while True:
    try:
        for article in articles:
            if article in previous:
                continue
            driver.execute_script(
                "window.scrollTo(0, "+str(article.location['y']-top)+");")
            try:
                elem = article.find_element_by_css_selector(
                    '.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0')
                description = elem.get_attribute('innerText')+' '+str(time())
            except NoSuchElementException:
                description = str(time())
            filename = ("".join(i for i in description if i not in ":;=+-_(){}[]*&^%$#@!<>/?\\|.,~`\n\"\'")
                        [:20]) if len(description) > 20 else description
            with open(location+'\\'+filename+'.png', "wb") as file:
                file.write(article.screenshot_as_png)
            previous.append(article)
            sleep(1)
    except StaleElementReferenceException:
        pass
    articles = driver.find_elements_by_tag_name('article')
