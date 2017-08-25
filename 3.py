#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
driver.get('https://www.baidu.com/')
assert "百度" in driver.title
elem = driver.find_element_by_name("wd")
elem.send_keys("python")
elem.send_keys(Keys.RETURN)
#print(driver.page_source)
#print(driver.title)
#driver.quit()
