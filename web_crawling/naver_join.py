#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# In[27]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select


# In[10]:


driver = webdriver.Chrome('chromedriver')
driver.get('https://naver.com')


# In[11]:


# 회원가입 버튼 가져와서 클릭
a_tag = driver.find_element_by_css_selector('#account > div > div > a')
a_tag.click()


# In[13]:


# 약관동의 체크박스
checkbox_tag = driver.find_element_by_css_selector('#join_form > div.terms_p > p > span > label')
checkbox_tag.click()


# In[15]:


# 동의
agree_btn = driver.find_element_by_css_selector('#btnAgree')
agree_btn.click()


# In[22]:


# id 입력
input_id = driver.find_element_by_css_selector('#id')
input_id.send_keys('wonca15') # Endter

input_pswd = driver.find_element_by_css_selector('#pswd1')
input_pswd.send_keys('Tmdgus553#')
input_pswd2 = driver.find_element_by_css_selector('#pswd2')
input_pswd2.send_keys('Tmdgus553#')

name = driver.find_element_by_css_selector('#name')
name.send_keys('백승현')

#생년월
year = driver.find_element_by_css_selector('#yy')
year.send_keys('1991')

month = driver.find_element_by_css_selector('#mm')
# 객체화
select_tag = Select(month)
select_tag.select_by_value('02')

year = driver.find_element_by_css_selector('#dd')
year.send_keys('10')

# 성별
gender = driver.find_element_by_css_selector('#gender')
# 객체화
gender_tag = Select(gender)
gender_tag.select_by_value('0')

# email
email = driver.find_element_by_css_selector('#email')
email.send_keys('wonca14@ajou.ac.kr')

pn = driver.find_element_by_css_selector('#phoneNo')
pn.send_keys('01028374875')

# 인증번호 받기
cert_btn = driver.find_element_by_css_selector('#btnSend')
cert_btn.click()

sns_code = input('인증번호를 입력해주세요')
auth_no = driver.find_element_by_css_selector('#authNo')
auth_no.send_keys(sns_code)

# 가입 확인 버튼
join_btn = driver.find_element_by_css_selector('#btnJoin')
join_btn.click()

