from pickle import GET
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

import sys
import time
from datetime import datetime,timedelta
import threading
from ytmusicapi import YTMusic

ytmusic = YTMusic()
options = webdriver.FirefoxOptions()
user_agent = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
options.add_argument(user_agent) 

options.add_argument('--headless')
options.add_argument('--log-level')
options.add_argument('--disable-application-cache')

service = Service('geckodriver.exe')

extension1 = "uBlock0_1.54.1b1.xpi"
driver = webdriver.Firefox(service=service,options=options)
loop_single = False

def stream(name):
    url = f"https://music.youtube.com/watch?v={name}"
    driver.install_addon(extension1, temporary=True)
    driver.get(url)
    driver.implicitly_wait(5)
    ripple = driver.find_element(By.XPATH,'//*[@id="ink"]')
    if(ripple):
        print("LOADER")
    driver.implicitly_wait(7)
    play_video = driver.find_element(By.XPATH,'//*[@id="play-pause-button"]')
    driver.implicitly_wait(5) 
    play_video.click()

def stream_album(name):
    try:
        url = f"https://music.youtube.com/playlist?list={name}"
        driver.install_addon(extension1, temporary=True)
        driver.get(url)
        driver.implicitly_wait(5)
        play_video = driver.find_element(By.XPATH,'//*[@id="top-level-buttons"]/yt-button-renderer/yt-button-shape')
        driver.implicitly_wait(5) 
        play_video.click()
    except:
        print("404 NOT FOUND")

def pause_and_play():
    pause_video = driver.find_element(By.XPATH,'/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]')
    driver.implicitly_wait(1) 
    pause_video.click()

def loop():
    repeat_video = driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[3]/div/tp-yt-paper-icon-button[2]')
    driver.implicitly_wait(1)
    loop_single = True
    for _ in range(2):
        repeat_video.click()

def stop_loop():
    repeat_video = driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[3]/div/tp-yt-paper-icon-button[2]')
    driver.implicitly_wait(1)
    loop_single = False
    repeat_video.click()

def next_song():
    next_song = driver.find_element(By.XPATH,'/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div[1]/tp-yt-paper-icon-button[5]')
    driver.implicitly_wait(1)
    next_song.click()


def get_time(play_hits=False,play_album = False):
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
                if not play_hits or not play_album and not loop_single:
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
                    search_results = ytmusic.search(songName)
                    for result in search_results:
                        if result.get('resultType') == 'song':
                            videoid = result.get('videoId')
                            song_name = result.get('title')
                            artists = [artist.get('name') for artist in result.get('artists', []) if artist.get('name') != 'Song']
                            album_name = result.get('album', {}).get('name')
                            thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')

                            print('videoId: ',videoid)
                            print('Song Name:', song_name)
                            print('Artist(s):', ', '.join(artists))
                            print('Album:', album_name)
                            print('Thumbnail URL:', thumbnail_url)
                            print()
                            stream(videoid)
                            break


                        if result.get('resultType') == 'album':
                            album_name = result.get('title')
                            album_artists = [artist.get('name') for artist in result.get('artists', []) if artist.get('name') != 'Album']
                            album_thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')
                            album_browse_id = result.get('browseId')
                            album_id = ytmusic.get_album(album_browse_id)
                            x = album_id.get('audioPlaylistId')

                            print('Album Name:', album_name)
                            print('Album Artist(s):', ', '.join(album_artists))
                            print('Album Thumbnail URL:', album_thumbnail_url)
                            print('Album ID', x)
                            print()
                            stream_album(x)
                            break
            elif uinput == "pause": 
                pause_and_play()
            elif uinput == "resume":
                resume_play()
            elif uinput == "loop":
                loop()
            elif uinput == "stop loop":
                stop_loop()
            elif uinput == "next song":
                next_song()
            elif uinput == "stop": 
                stop()
                
            else: 
              print("invalid command")
            time_thread = threading.Thread(target=get_time)
            time_thread.start()