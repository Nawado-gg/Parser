'''
КОГДА ИЗМЕНЯЕТЕ XPath смотрите, чтобы шаблон совпадал с исходным кодом 
(последовательность тегов не должна отличаться)
МОГУТ БЫТЬ СИТУАЦИИ КОГДА НУЖНО УДАЛИТЬ ИНДЕКС, ПОДСТАВИТЬ ПЕРЕМЕННУЮ ИЛИ УДАЛИТЬ ВЕСЬ ТЕГ


ТАК ЖЕ НАСТРОЙТЕ ВРЕМЯ time.sleep(n) ПОД СЕБЯ
'''


#Спартак

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

#Указать путь к Хром драйверу на вашем компе
browser = webdriver.Chrome('/usr/bin/chromedriver')
browser.get('https://platform.wyscout.com/app/?')
browser.maximize_window()
browser.implicitly_wait(10)

username = browser.find_element_by_id('login_username')
username.send_keys('login') #Ввести свой логин

password = browser.find_element_by_id('login_password')
password.send_keys('password') #Ввести свой пароль
password.send_keys(Keys.RETURN)
time.sleep(5)

action = webdriver.ActionChains(browser)

#Указать Xpath страны
country = browser.find_element_by_xpath('//*[@id="detail_0_home_navy"]/div[1]/div/div[69]/div/div[1]/img')
action.move_to_element(country)
country.click()
time.sleep(2)

#Указать Xpath лиги
league = browser.find_element_by_xpath('//*[@id="detail_0_area_navy_0"]/div/div/div[3]/div/div[1]/img')
league.click()
time.sleep(4)

#Добавить, если есть выбор региона
region = browser.find_element_by_xpath('//*[@id="detail_0_competition_navy_0"]/div[1]/div/div[1]/div/div[1]/span')
region.click()
time.sleep(2)

#Указать Xpath лиги
team = browser.find_element_by_xpath('//*[@id="detail_0_competition_navy_1"]/div[1]/div/div[2]/div/div[1]/img')
team.click()
time.sleep(2)
#Не трогать
stats = browser.find_element_by_xpath('//*[@id="detail_0_team_tab_stats"]')
stats.click()
time.sleep(2)
#Не трогать
dropdown_type = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[2]/div[1]/div[1]/div')
dropdown_type.click()
#Не трогать
dropdown_type_update = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[5]')
dropdown_type_update.click()
time.sleep(2)
'''
#Не трогать
dropdown_season = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[1]/div[2]/div/div')
dropdown_season.click()
#Последний тег этой строки изменяет сезон (руками поменять цифу в последнем div)
dropdown_season_update = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]')
dropdown_season_update.click()
time.sleep(2)
'''

#Не трогать
header1 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr[1]')
header2 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr[2]')
header3 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]/div[1]')
header4 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[1]')
#Не трогать
browser.execute_script("arguments[0].style.visibility='hidden'", header1)
browser.execute_script("arguments[0].style.visibility='hidden'", header2)
browser.execute_script("arguments[0].style.display='none'", header3)
browser.execute_script("arguments[0].style.display='none'", header4)



#Начинается парсинг
#Указывается номер игры с которой нужно грузить (первая игра = 3, дальше счет через одну (вторая игра = 5, четвертая игра = 9))
game_counter = 3

#Используется, если выгрузка сломалась и нужно начинать с середины
if game_counter > 12:
    string_index = 3
    for string_index in range(string_index, game_counter):
        transport_element = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(string_index)+']/td[4]/span/em')
        browser.execute_script("arguments[0].scrollIntoView();", transport_element)
        string_index += 1
        

while game_counter <= 100:
    #Указать Xpath Игры (можно указать по первой выгружаемой схемы)
    game = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td[4]/span/em')
    browser.implicitly_wait(3)
    browser.execute_script("arguments[0].scrollIntoView();", game)
    action = webdriver.ActionChains(browser)
    action.move_to_element(game)
    #action = webdriver.ActionChains(browser)
    #Указать название игры и дату (важно заменить поля Tr и Td на переменные (по примеру как было в исходном присланном файле))
    game_name_1 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td[1]/div[1]').text
    game_name_2 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td[1]/div[2]').text
    game_name_1 = game_name_1.replace(":", "-")
    game_name_2 = game_name_2.replace(":", "-")
    
    scheme_counter = 5
    while scheme_counter <= 11:
        #Указать Xpath Схемы
        #(важно заменить поля Tr и Td на переменные (по примеру как было в исходном присланном файле))
        scheme = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/span/em')
        browser.execute_script("arguments[0].scrollIntoView();", scheme)
        browser.implicitly_wait(3)        
        browser.execute_script("arguments[0].click();", scheme)
        
        time.sleep(2)
        
        player_counter = 1
        #Указать Xpath кружочка с игроком
        #(важно заменить поля Tr и Td на переменные (по примеру как было в исходном присланном файле))
        #Смотрите что копируете дальше, если в исходном файле теги Tr, Td и div заменялись с константы на переменную то делайте по аналогии
        players_count = len(browser.find_elements_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div'))
        
        data_table = []
        while player_counter <= players_count:
            browser.implicitly_wait(3)
            #Xpath с кружком игрока на схеме (в конце важно заменить значение div с константы на переменную)
            player = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[' + str(player_counter) + ']')
            browser.execute_script("arguments[0].click();", player)

            passes_counter = 1
            browser.implicitly_wait(3)
            # то же самое что у переменной palyer, только нужно удалить последний div
            passes_count = len(browser.find_elements_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div'))
            
            
            while passes_counter <= passes_count:
                browser.implicitly_wait(3)
                # Из схемы указывается Xpath двух игроков и их пасы
                name_1 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div['+str(passes_counter)+']/div[2]/p[1]')
                name_2 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div['+str(passes_counter)+']/div[2]/p[2]')
                passed_1 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div['+str(passes_counter)+']/div[3]/p[1]')
                passed_2 = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div['+str(passes_counter)+']/div[3]/p[2]')
                q = (name_1.text, name_2.text, passed_1.text, passed_2.text)
                data_table.append(q)
                passes_counter += 1
                
            browser.implicitly_wait(3)
            #Такой же путь как и выше у переменной player
            player = browser.find_element_by_xpath('//*[@id="detail_0_team_stats"]/div/div/div/main/div[3]/div[2]/div/table/tbody/tr['+str(game_counter)+']/td['+str(scheme_counter)+']/div[2]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[' + str(player_counter) + ']')
            browser.execute_script("arguments[0].click();", player)
            player_counter += 1
            
            

        globals()['df_%s%s' % (game_counter, scheme_counter)] = pd.DataFrame(data_table)
        # Изменить путь к файлу (df_[%s][%s]%s.csv - эту часть не менять)
        pd.DataFrame(data_table).to_csv(r'/home/gleb/Desktop/data_PFL/Ararat/passes/df_[%s][%s]%s.csv' % (game_name_1, game_name_2, scheme_counter-4))
        browser.implicitly_wait(3)
        browser.execute_script("arguments[0].click();", scheme)
        scheme_counter += 1

    game_counter += 2
