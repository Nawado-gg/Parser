'''
КОГДА ИЗМЕНЯЕТЕ XPath смотрите, чтобы шаблон совпадал с исходным кодом 
(последовательность тегов не должна отличаться)
МОГУТ БЫТЬ СИТУАЦИИ КОГДА НУЖНО УДАЛИТЬ ИНДЕКС, ПОДСТАВИТЬ ПЕРЕМЕННУЮ ИЛИ УДАЛИТЬ ВЕСЬ ТЕГ
'''

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import numpy as np

browser = webdriver.Chrome(executable_path = r'/usr/bin/chromedriver')
browser.get('https://platform.wyscout.com/app/?')
browser.maximize_window()
browser.implicitly_wait(10)


#Need to fill all fields
username = browser.find_element_by_id('login_username')
username.send_keys('login')

password = browser.find_element_by_id('login_password')
password.send_keys('password')

password.send_keys(Keys.RETURN)
time.sleep(4)
country = browser.find_element_by_xpath('//*[@id="detail_0_home_navy"]/div[1]/div/div[69]/div/div[1]')
country.click()
time.sleep(2)
league = browser.find_element_by_xpath('//*[@id="detail_0_area_navy_0"]/div/div/div[3]/div/div[1]/img')
league.click()
time.sleep(2)
#Добавить, если есть выбор региона
region = browser.find_element_by_xpath('//*[@id="detail_0_competition_navy_0"]/div[1]/div/div[1]/div/div[1]/span')
region.click()
time.sleep(2)
team = browser.find_element_by_xpath('//*[@id="detail_0_competition_navy_0"]/div[1]/div/div[1]/div/div[1]/img')
team.click()
time.sleep(2)
stats = browser.find_element_by_xpath('//*[@id="detail_0_team_tab_stats"]')
stats.click()
time.sleep(2)

dropdown_type = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[2]/div[1]/div[1]/div')
dropdown_type.click()

dropdown_type_update = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]')
dropdown_type_update.click()
time.sleep(2)

'''
dropdown_season = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[1]/div[2]/div/div')
dropdown_season.click()
dropdown_season_update = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]')
dropdown_season_update.click()
time.sleep(2)
'''

header1 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr[1]')
header2 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr[2]')
header3 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[1]')
header4 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]')

browser.execute_script("arguments[0].style.visibility='hidden'", header1)
browser.execute_script("arguments[0].style.visibility='hidden'", header2)
browser.execute_script("arguments[0].style.display='none'", header3)
browser.execute_script("arguments[0].style.display='none'", header4)


game_counter = 3

#Используется, если выгрузка сломалась и нужно начинать с середины
if game_counter > 12:
    string_index = 3
    for string_index in range(string_index, game_counter):
        transport_element = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(string_index)+']/td[4]/span/em')
        browser.execute_script("arguments[0].scrollIntoView();", transport_element)
        string_index += 1
        
while game_counter <= 100:
    game = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']')
    browser.implicitly_wait(10)
    browser.execute_script("arguments[0].scrollIntoView();", game)
    action = webdriver.ActionChains(browser)
    action.move_to_element(game)

    game_name_1 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td[1]/div[1]').text                                          
    game_name_2 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td[1]/div[2]').text
    game_name_1 = game_name_1.replace(":", "-")
    game_name_2 = game_name_2.replace(":", "-")

    scheme_counter = 12
    
    
    while scheme_counter <= 13:
        scheme = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/span/em')                                              
        browser.execute_script("arguments[0].scrollIntoView();", scheme)
        browser.implicitly_wait(10)
        browser.execute_script("arguments[0].click();", scheme)
        
        time.sleep(2)

        data_table = []

        rows_counter = 1
        browser.implicitly_wait(10)
        
        rows_count = len(browser.find_elements_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div'))
                                                        
        while rows_counter <= rows_count:
            browser.implicitly_wait(10)
            
            name = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div['+str(rows_counter)+']/div[2]')                                   
            #Подставить Xpath значения из схемы (подставить переменные как в исходном файле)
            abs_val = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div['+str(rows_counter)+']/div[3]')                                   
            s = abs_val.text
            val = np.asarray(s.split('\n'))
            q = (name.text, val[0], val[1])
            data_table.append(q)
            rows_counter += 1

        globals()['df_%s%s' % (game_counter, scheme_counter)] = pd.DataFrame(data_table)
        pd.DataFrame(data_table).to_csv(r'/home/gleb/Desktop/data_FNL/Armavir/attacking/df_[%s][%s]%s.csv' % (game_name_1, game_name_2, scheme_counter-11))
        browser.implicitly_wait(10)
        browser.execute_script("arguments[0].click();", scheme)
        scheme_counter += 1

    game_counter += 2
