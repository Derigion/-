from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

def start_chrome():
    driver = webdriver.Chrome(executable_path=r'C:\Users\MECHREVO\AppData\Local\Programs\Python\Python38\chromedriver.exe')
    driver.start_client()
    return driver

def scroll_down():
    html = driver.find_element_by_tag_name('html')

    for i in range(10):
        html.send_keys(Keys.END)
        time.sleep(0.5)

def find_info():
    info_list = []
    # 获取完整内容及时间
    cards_sel = 'div.card.m-panel.card9.f-weibo'
    text_sel = 'div.weibo-text'
    time_sel = 'span.time'

    card = driver.find_element_by_css_selector(cards_sel)
    text = card.find_element_by_css_selector(text_sel).text
    time = card.find_element_by_css_selector(time_sel).text
    #获取评论数
    lite_pages_sel = 'div.lite-page-tab'
    comment_num_sel = 'div.tab-item.cur'

    lite_page = driver.find_element_by_css_selector(lite_pages_sel)
    comment_num = lite_page.find_element_by_css_selector(comment_num_sel).text
    # 获取评论
    comments_sel = 'div.card.m-avatar-box.lite-page-list'
    comment_text_sel = 'h3'
    templist = [text, time,comment_num]

    comments = driver.find_elements_by_css_selector(comments_sel)

    for comment in comments:
        comment_text = comment.find_element_by_tag_name(comment_text_sel).text
        templist.append(comment_text)

    info_list.append(templist)

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

driver = start_chrome()
name = 'Comments 2020-03-10~2020-05-31'

with open('2020-03-10-~2020-05-31.csv','r') as f:
    reader = csv.reader(f)
    result = list(reader)
    for i in range (3157,len(result)):
        url = result[i][2]
        driver.get(url)
        time.sleep(1)
        info_list = find_info()
        save(info_list,name)



