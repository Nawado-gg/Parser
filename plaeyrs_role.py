import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import numpy as np


global login_username
login_username = 'bi.3.2015@yandex.ru'
global login_password
login_password = 'bld1997'
#Указать путь к Хром драйверу на вашем компе

path_to_driver = r'/usr/bin/chromedriver'

site = 'https://platform.wyscout.com/app/?'

#Указать номер страны (Россия = 69)
country_id = 70
country_xpath = '//*[@id="detail_0_home_navy"]/div[1]/div/div['+ str(country_id) +']/div/div[1]'

league_id = 2
league_xpath = '//*[@id="detail_0_area_navy_0"]/div/div/div['+ str(league_id) +']/div/div[1]'

region_id = 1 #Могут быть от 1 до 5
region_xpath = '//*[@id="detail_0_competition_navy_0"]/div[1]/div/div['+ str(region_id) +']/div/div[1]/span'

#Указать номер команды по WyScout
team_id = 2 #Начинается с 2-х для FNL
team_xpath = '//*[@id="detail_0_competition_navy_1"]/div[1]/div/div['+ str(team_id) + ']/div/div[1]/img'

path_to_save_dir = r'/home/gleb/Desktop/parser/Mordovia/attacking/'

#Переменные парсера

global game_counter
game_counter = 3





def path_to_stats():
    global browser
    global action
    browser = webdriver.Chrome(executable_path = path_to_driver)
    action = webdriver.ActionChains(browser)
    browser.get(site)
    browser.maximize_window()
    browser.implicitly_wait(10)

    username = browser.find_element_by_id('login_username')
    username.send_keys(str(login_username))

    password = browser.find_element_by_id('login_password')
    password.send_keys(str(login_password))
    password.send_keys(Keys.RETURN)
    time.sleep(4)
    
    country = browser.find_element_by_xpath(country_xpath)
    country.click()
    time.sleep(2)
    
    league = browser.find_element_by_xpath(league_xpath)
    league.click()
    time.sleep(2)

    
def parser():
    team_counter = 1
    team_count = len(browser.find_elements_by_xpath('//*[@id="detail_0_competition_navy_0"]/div[1]/div/div'))
    
    while team_counter <= team_count:
        team = browser.find_element_by_xpath('//*[@id="detail_0_competition_navy_0"]/div[1]/div/div[' + str(team_counter) + ']/div/div[1]/img')
        team.click()
        time.sleep(2)
        

        player_counter = 2
        error_count = 0
        while True:
            
            try:
                player = browser.find_element_by_xpath('//*[@id="detail_0_team_navy"]/div[1]/div/div[' + str(player_counter) +']')
                player.click()
                
                stats = browser.find_element_by_xpath('//*[@id="detail_0_player_tab_stats"]/a/span/span')
                
                stats.click()
                
                export = browser.find_element_by_xpath('//*[@id="detail_0_player_stats"]/div/div/div/main/div[3]/div[1]/div[2]/a')
                export.click()
                time.sleep(2)
                
                
                browser.back()
            except:
                error_count += 1
            player_counter += 1
            
            if error_count >= 4:
                break

        
        browser.back()
        team_counter += 1
        
        
def main():
    path_to_stats()
    parser()
    
main()
