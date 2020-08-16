#!/usr/bin/env python
# coding: utf-8

# # 웹페이지 특징 파악
# 1. 140자 평점데이터는 iframe 을 통해 출력된다.
# 2. 요청할 페이지의 소스에 데이터가 들어있다.

# In[261]:


# lib
import requests # get url respoonse
import bs4 # response to bs4 object
import time # delay 1 sec for each page
import pandas as pd # data to csv

import matplotlib.pyplot as plt
import seaborn as sb
import re


# In[317]:


# 데이터 프레임을 처음 저장하는지 확인하기 위한 flag


# In[264]:


# url 받아서 bs4 객체를 반환하는 함수
# xlml 파서를 쓰면 tag 방식을 쓰는 모든 문서 타입에 적용할 수 있다.
def requestPage(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    return soup

# 필요한 정보를 가져온다.
def getResult(soup):
    
    reple_list = []
    score_list = []
    up_list = []
    down_list = []

    li_list = soup.select('div.score_result>ul>li')
    
    for li_tag in li_list:
        star_score_tag = li_tag.select('div.star_score>em')
        star_score = star_score_tag[0].text.strip()
        score_reple_tag = li_tag.select('div.score_reple>p')
        score_reple = score_reple_tag[0].text.strip()
        up_vote_tag = li_tag.select('div.btn_area>strong:nth-child(2) > span')
        up_vote = up_vote_tag[0].text.strip()
        down_vote_tag = li_tag.select('div.btn_area> strong:nth-child(4)> span')
        down_vote = down_vote_tag[0].text.strip()
        
        score_list.append(star_score)
        reple_list.append(score_reple) 
        up_list.append(up_vote)
        down_list.append(down_vote)
        
    return score_list,reple_list,up_list,down_list


# In[270]:


# 전체 페이지 개수를 반환하는 함수
def getPageCnt(movie_code):

    #접속할 페이지 주소
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,'lxml')
    cnt = soup.select('div.score_total>strong.total>em')[0].text
    cnt = int(re.sub(r',','',cnt))
    
    # 한 페이지당 댓글이 10개다.
    if cnt%10 > 0:
        cnt = cnt +1
    return cnt//10


# In[273]:


movie_list =['156464','109906']


# In[315]:


def getMovieCode():

    # 영화코드를 담을 리스트
    movie_code_list = []
    
    # 크롤링 페이지 설정
    url = 'https://movie.naver.com/movie/running/current.nhn?order=reserve'
    soup = requestPage(url)
    a = soup.select('ul.lst_detail_t1 li>div.thumb>a')

    for li in a:
        movie_code = (li.attrs['href'].strip().split('=')[1])
        movie_code_list.append(movie_code)

    return movie_code_list

flag = False

# 가져올 영화 코드 리스트
# movie_list =['156464','109906']
moive_list = getMovieCode()
movie_list = movie_list[:3]

# 접속할 페이지 주소 : 소스보기 -> iframe 검색 ->src, 영화 캡틴마블(2019) 영화 평점 데이터
# site = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=132623&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'

for movie_code in movie_list:

    # 전체 페이지수를 가져온다.
    tot_page_cnt = getPageCnt(movie_code)
    
    print(f'{movie_code} 데이터 수집 시작')
    print('-'*80)
    
    for idx in range(5):
        
        print(f'{idx+1}/{5}')

        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={idx+1}'

        score_list, reple_list,up_list,down_list = getResult(requestPage(url))
        total_list = list(zip(score_list, reple_list,up_list,down_list))
        df = pd.DataFrame(total_list)

        if flag == False: 
            df.columns = ['score','reple','up_vote','down_vote']
            df.to_csv('naver_satar_data.csv',index = False, encoding = 'utf-8-sig') # mode a : 누적
            flag = True
        else :
            df.to_csv('naver_satar_data.csv',index = False, encoding = 'utf-8-sig',mode = 'a',header = False) # mode a : 누적
        time.sleep(1)

    print('-'*80)
print('데이터 수집 완료')






