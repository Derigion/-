from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os



def start_chrome():
    driver = webdriver.Chrome(executable_path=r'C:\Users\MECHREVO\AppData\Local\Programs\Python\Python38\chromedriver.exe')
    driver.start_client()
    return driver

#scroll down the Sina web to show all cards
def scroll_down():
    html = driver1.find_element_by_tag_name('html')

    for i in range(15):
        html.send_keys(Keys.END)
        time.sleep(0.5)

def find_cards_info():
    cards_sel = 'div.WB_feed_detail'
    text_sel = 'div.WB_text.W_f14'
    time_sel = 'div.WB_from.S_txt2'
    link_sel = 'div.WB_from.S_txt2 > a:nth-child(1)'

    cards = driver1.find_elements_by_css_selector(cards_sel)
    info_list = []
    for card in cards:
        text = card.find_element_by_css_selector(text_sel).text
        time = card.find_element_by_css_selector(time_sel).text
        link = baseUrl + card.find_element_by_css_selector(link_sel).get_attribute('name')


        info_list.append([text,time,link])

    return info_list

def save(info_list,name):
    full_path = './' + name + '.csv'
    if os.path.exists(full_path):
        with open(full_path,'a') as f:
            writer = csv.writer(f)
            try:
                writer.writerows(info_list)
            except UnicodeEncodeError:
                pass
    else:
        with open(full_path,'w+') as f:
            writer = csv.writer(f)
            try:
                writer.writerows(info_list)
            except UnicodeEncodeError:
                pass



def find_next():
    next_sel = 'a.page.next'
    next_page = driver1.find_elements_by_css_selector(next_sel)
    if next_page:
        return next_page[0].get_attribute('href')


def run_crawler(url,name):
    driver1.get(url)
    time.sleep(3)
    scroll_down()
    time.sleep(3)
    info_list = find_cards_info()
    save(info_list,name)
    next_page = find_next()
    if next_page:
        run_crawler(next_page,name)

formatURL = "https://weibo.com/rmrb?start_time=2020-03-10&end_time=2020-03-16&is_search=1&is_searchadv=1#_0"
baseUrl = "https://m.weibo.cn/detail/"
driver1 = start_chrome()
input()
run_crawler(formatURL,'2020-03-10-~2020-05-31')