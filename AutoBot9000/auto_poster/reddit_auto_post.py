import selenium
import random
import keyboard
import pyautogui as pyg
import time
import env 
#Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

#WebDriver Wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


option=webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", { 
"profile.default_content_setting_values.notifications": 2 
})

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=option)


driver.set_window_size(1920, 1080)

# YOUR INPUTS, these all come from the env file 

variables= env.Variables() 
username= variables.username
password= variables.password
website= variables.website
your_subreddit= variables.your_subreddit
title =  variables.title

subreddits_to_crosspost_list= ['memes','funny','catmemes']
#-------


def random_wait():
    #Random wait time from 0-2 Seconds
    wait_time=random.random()*2

    time.sleep(wait_time)

def log_in_website(username,password,website):
    
    #wait
    driver.implicitly_wait(15)
    driver.get(website)

    driver.maximize_window()

    log_in_initiate = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('a._3Wg53T10KuuPmyWOMWsY2F._2iuoyPiKHN3kfOoeIQalDT._2tU8R9NTqhvBrhoNAXWWcP.HNozj_dKjQZ59ZsfEegz8._2nelDm85zKKmuD94NequP0'))) 

    random_wait()
    log_in_initiate.click()

    random_wait()
    login_iframe = driver.find_element(By.CSS_SELECTOR, "iframe._25r3t_lrPF3M6zD2YkWvZU")
    driver.switch_to.frame(login_iframe)

    random_wait()
    log_in_username= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.NAME, "username")))
    log_in_username.send_keys(username)

    random_wait()
    log_in_password= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.NAME, "password")))
    log_in_password.send_keys(password)

    random_wait()
    log_in_button= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('button.AnimatedForm__submitButton.m-full-width')))
    log_in_button.click()

    time.sleep(10)

    







def post_meme_to_reddit(your_subreddit,title,folder_index):
    
    #folder_index_auto_set_to_0 right now
    folder_index=0
    
    #go to the subreddit
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element(By.NAME, "q")))

    driver.get('https://www.reddit.com/'+your_subreddit+'/')
    keyboard.press_and_release('esc')
    random_wait()
    create_post_intialize=WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.NAME, "createPost")))
    create_post_intialize.click()

    #scroll up to avoid intro message
    random_wait()
    time.sleep(5)
    scroll_to = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div")
    driver.execute_script("return arguments[0].scrollIntoView();", scroll_to)
    time.sleep(2)

    random_wait()
    #go to the meme submission category
    images_video_button =WebDriverWait(driver, 50).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('i._3WIAbYQQdSmuuFLDSfhn5_.icon.icon-image_post')))
    images_video_button.click()

    random_wait()
    #give it a title
    title_input=WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector("textarea.PqYQ3WC15KaceZuKcFI02._1ec_Oj5SWdypd8L-VELKg-")))  
    title_input.send_keys(title)

    random_wait()
    #click upload
    upload_button= WebDriverWait(driver, 50).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('button._3O09Fh0CTb1KXH9g--pyTm._2iuoyPiKHN3kfOoeIQalDT._2tU8R9NTqhvBrhoNAXWWcP.HNozj_dKjQZ59ZsfEegz8')))
    upload_button.click()

    #must wait for finder to load
    time.sleep(7)
    
    #files must be in a folder at the top of your finder when it is opened
    keyboard.press_and_release('right')
    random_wait()
    keyboard.press_and_release('right')
    time.sleep(2.5)
    #for i in range(folder_index):
    #    keyboard.press_and_release('down')
    keyboard.press_and_release('enter')

    post_button= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('button._18Bo5Wuo3tMV-RDB8-kh8Z._1_Xn_Na9NfUSd_yoc1w2Eb._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8')))
    post_button.click()



def cross_posts(x_sub_list):
    time.sleep(2.5)
    random_wait()
    for x_sub in x_sub_list:
    
        random_wait()
        share_button=WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('button.kU8ebCMnbXfjCWfqn0WPb')))
        share_button.click()

        random_wait()
        cross_post_button= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('i._1m76BHzDzRsM1te7HBxUqd.icon.icon-crosspost')))
        cross_post_button.click()

        time.sleep(4.5)
        random_wait()
        #switch tabs
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(4.5)
        choose_community_button= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('input._1MHSX9NVr4C2QxH2dMcg4M')))
        choose_community_button.send_keys(x_sub)
        
        time.sleep(2.5)
        random_div= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('div._3M6BmdyQcCEQZu-MylN14')))
        random_div.click()
        
        random_wait()
        post_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div[1]/button")
        driver.execute_script("return arguments[0].scrollIntoView();", post_button)
        
        time.sleep(3.5)
        random_wait()
        post_button= WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element_by_css_selector('button._18Bo5Wuo3tMV-RDB8-kh8Z._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8')))
        post_button.click()

        



def automated_cross_posts(title,folder_indices,x_sub_list):
    """
    str + list + list --> None
    """

    log_in_website(username,password,website)

    for folder_index in folder_indices:
        #run through cross posting at folder index to all subreddits
        post_meme_to_reddit(your_subreddit,title,folder_index)

        cross_posts(x_sub_list)
        #make sure last post loads
        time.sleep(10)
    #close driver
    driver.close()

if name == "__main__":
    automated_cross_posts(title,1,your_subreddit)

