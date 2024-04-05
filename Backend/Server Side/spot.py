from pickle import GET
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

import sys
import time
from datetime import datetime,timedelta
import threading

options = webdriver.FirefoxOptions()
user_agent = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
options.add_argument(user_agent) 

options.add_argument('--headless')
options.add_argument('--log-level')
options.add_argument('--disable-application-cache')

service = Service('geckodriver.exe')

extension1 = "uBlock0_1.54.1b1.xpi"
driver = webdriver.Firefox(service=service,options=options)

def stream(name):
    url = f"https://music.youtube.com/search?q={name}"
    driver.install_addon(extension1, temporary=True)
    driver.get(url)
    driver.implicitly_wait(2)
    
    try:
        element = driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-card-shelf-renderer/div/div[2]/div[1]/div/div[2]/div[2]/yt-button-renderer[1]/yt-button-shape/button')
        shuffle = driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-card-shelf-renderer/div/div[3]/ytmusic-responsive-list-item-renderer[1]/div[2]/div[1]/yt-formatted-string/a')
        element_text = element.text
        
        if element_text == "Play":
            element.click()
        elif element_text == "Shuffle":
            shuffle.click()
        else:
            print("Couldn't Find the song")
    except NoSuchElementException as e:
        exception = driver.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]/div[2]/div[1]/yt-formatted-string/a')
        exception.click()
        
    except Exception as e:
        print(f"Error occurred: {e}")

def pause_and_play():
    pause_video = driver.find_element(By.XPATH,'/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]')
    driver.implicitly_wait(1) 
    pause_video.click()

def get_time(play_hits=False):
    stop_flag = False
    while not stop_flag:
        try:
            total_time_element = driver.find_element(By.XPATH, '//*[@id="left-controls"]/span')
            total_time_text = total_time_element.text
            
            time_parts = total_time_text.split('/')
            if len(time_parts) == 2:
                current_time, total_duration = map(str.strip, time_parts)  

                current_time_obj = datetime.strptime(current_time, '%M:%S')
                total_duration_obj = datetime.strptime(total_duration, '%M:%S')
                
                if current_time_obj == (total_duration_obj - timedelta(seconds=1)):
                    stop_flag = True
            if stop_flag:
                if not play_hits:
                    stop()
                break
            
        except NoSuchElementException:
            sys.stdout.write("\rTime element not found.")
            sys.stdout.flush()
        
        except StaleElementReferenceException:
            sys.stdout.write("\rStale element reference. Re-locating the element.")
            sys.stdout.flush()
            continue
        
        except Exception as e:
            print(f"Error occurred: {e}")


def resume_play():
    pause_video = driver.find_element(By.XPATH,'/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]')
    driver.implicitly_wait(1) 
    pause_video.click()

def stop():
    try:
        pause_button = driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]')
        if pause_button.is_displayed():
            pause_button.click()
    except Exception as e:
        print(f"Error occurred while stopping playback: {e}")

def playhits(artist_name):
    try:
        url = f"https://music.youtube.com/search?q={artist_name}"
        driver.get(url)
        driver.implicitly_wait(3) 
        radio_button = driver.find_element(By.XPATH, '//*[@id="actions"]/yt-button-renderer[1]/yt-button-shape/button')
        radio_button.click()

        get_time(play_hits=True)
        
    except Exception as e:
        print(f"Error occurred while playing hits of {artist_name}: {e}")


if __name__ == "__main__": 
        print("Enter the name of song") 
        while True: 
            uinput = str(input()) 
            if uinput.split(" ", 1)[0] == "play": 
                if uinput.startswith("play the hits of"):
                    artist_name = uinput.split("play the hits of ", 1)[1] 
                    playhits(artist_name)
                else:
                    songName = uinput.split(" ", 1)[1] 
                    stream(songName)
            elif uinput == "pause": 
                pause_and_play();
            elif uinput == "resume":
                resume_play();
            elif uinput == "stop": 
                stop()
                
            else: 
              print("invalid command")
            time_thread = threading.Thread(target=get_time)
            time_thread.start()