from typing import List

import re
import pandas as pd
from gazpacho import Soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from urllib.parse import quote

# 수집할 페이지의 범위를 지정
def define_crawling_page_num(wd, user_range):
    ## part 1 : 마지막 page number 구하기
    current_page_a_tags = wd.find_elements(By.XPATH, f"//*[@id='kakao_search']/div[2]/div[1]/a")
    last_a_element = current_page_a_tags[-1]
    
    if last_a_element.get_attribute('innerHTML') != '끝':
        last_page_number = int(last_a_element.get_attribute('innerHTML'))
    else:
        last_page_number = int(last_a_element.get_attribute('href').split('(')[-1].split(')')[0])

    # print(last_page_number)

    ## part 2 : 수집할 페이지의 범위를 지정
    if user_range > last_page_number:
        crawling_range = last_page_number
        print(f'Attention : your number({user_range}) is too big, so we define crawling page range {crawling_range}.')
    else:
        crawling_range = user_range
    return crawling_range

# 각 페이지별로 글들의 url, title 추출
def get_page_url_titles(soup)->List:
    target_page_table = soup.find('table', {'id' : 'kakao_seach_list'}, partial = False).find('tbody').find('tr', mode='all')

    return target_page_table

def click_next_page(wd, current_page_num):
    ## 다음페이지로 이동(current_page_num이 15의 배수일 경우, a tag의 첫 번째 element로 이동 후, 다음 버튼 클릭)
    if current_page_num % 15 != 0:
        wd.find_element(By.XPATH, f"//*[@id='kakao_search']/div[2]/div[1]/a[{current_page_num}]").click()
    else:
        wd.find_element(By.XPATH, f"//*[@id='kakao_search']/div[2]/div[1]/a[1]").click()
        wd.find_element(By.XPATH, f"//*[@id='kakao_search']/div[2]/div[1]/a[@class='sp_pagingicon page_next']").click()
    sleep(2)

    html = wd.page_source
    return html
    
# url 크롤링 -> 본문 및 댓글 사용하지 않을 예정....
# def crawling_url(wd, url):
#     tag_delete_pattern = re.compile('(<([^>]+)>)')
#     wd.get(url)
#     html = wd.page_source
#     soup = Soup(html)

#     content_value = soup.find('div', {'class' : 'write_div'}, partial=False)
#     print(f'content_value :  {content_value}')

#     content_html = content_value.html
#     content_text = str(re.sub(tag_delete_pattern, '', content_html)).strip()

#     print(f'crawling_url content :  {content_text}')
# url 크롤링 -> 본문 및 댓글 사용하지 않을 예정....

# keyword가 추출한 title 내에 있는지 없는지 확인
def checking_keyword_in_title(title, keyword):
    if str(keyword) in title:
        return True
    else:
        False

def crawling_target_keyword_datas(keyword, extract_range, base_url='https://gall.dcinside.com/board/lists/?id=baseball_new11&s_type=search_subject_memo&s_keyword=')->List[str]:
    ## part 1 : url형태로 encode
    keyword_encode = quote(keyword)
    target_url = base_url+keyword_encode

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('') ## user-agent 기입

    wd = webdriver.Chrome(options=options)
    wd.get(target_url)
    html = wd.page_source
    soup = Soup(html)

    #### 크롤링할 페이지 수 결정
    crawling_range = define_crawling_page_num(wd, extract_range)
    
    ### 제목 크롤링
    pattern = re.compile('(<([^>]+)>)')

    keyword_title_list = []

    for p in range(crawling_range):
        soup = Soup(html)
        target_page_tr_tags = get_page_url_titles(soup) # tr list 받음
        for i in range(len(target_page_tr_tags)):
            print(f'---------- {i} ----------')
            temp_tr_soup = target_page_tr_tags[i]
            temp_a_tag = temp_tr_soup.find('a')

            ### title 추출
            temp_title_tag = temp_a_tag.html
            print('--- temp_title_text ---')
            title_text = re.sub(pattern, '', temp_title_tag).strip()
            print(title_text)
            print()
            #############

            if checking_keyword_in_title(title_text, keyword):
                keyword_title_list.append(title_text)
        html = click_next_page(wd, p+1) # p+1 -> 1,2,3, ... ,crawling_range

    wd.quit()

    return keyword_title_list


if __name__== '__main__':
    keyword_title_list = crawling_target_keyword_datas(keyword='', extract_range=10)
    dc_crawling_title_dataframe = pd.DataFrame({'text' : [], 'label' : []})

    dc_crawling_title_dataframe['text'] = keyword_title_list
    dc_crawling_title_dataframe['label'] = [1] * len(keyword_title_list)

    print(dc_crawling_title_dataframe)

    ## 결과 저장
    dc_crawling_title_dataframe.to_csv('', sep = '\t', index = False)