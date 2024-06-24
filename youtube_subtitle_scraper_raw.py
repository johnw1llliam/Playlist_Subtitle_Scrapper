from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import time
import os
import re
import shutil

# LOADING SELENIUM
playlist_link = input("Insert playlist link: ")
print("Loading...")
options = uc.ChromeOptions()
options.add_argument("--enable-javascript")
# Change the chrome profile path here to your chrome profile path
chrome_profile_path = r"CHROME_PROFILE_PATH"
options.add_argument(f"user-data-dir={chrome_profile_path}")
# Change the chromedriver path here to your chromedriver path
driver = uc.Chrome(options=options, executable_path=r'CHROMEDRIVER_PATH')
driver.implicitly_wait(10)

# GET VIDEO LINKS
driver.get("https://cable.ayra.ch/ytdl/playlist.php")
form = driver.find_element(By.XPATH, '/html/body/div/form/div[1]/input')
form.send_keys(playlist_link)
api_mode_button = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/label/input')
api_mode_button.click()
get_url_button = driver.find_element(By.XPATH, '/html/body/div/form/div[4]/input')
get_url_button.click()
links = driver.find_element(By.XPATH, '/html/body/pre')
links = links.text
video_links = links.split()

# GET VIDEO SUBTITLES
driver.get("https://downsub.com/")
for link in video_links:
    form = driver.find_element(By.XPATH, '//*[@id="input-34"]')
    form.send_keys(link)
    download_button = driver.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div/div[2]/form/div/div[2]/button')
    download_button.click()
    try:
        download_button = driver.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/button[2]')
        download_button.click()
        form = driver.find_element(By.XPATH, '//*[@id="input-34"]')
        form.send_keys(Keys.CONTROL + "a")
        form.send_keys(Keys.DELETE)
        time.sleep(4)
    except NoSuchElementException:
        form = driver.find_element(By.XPATH, '//*[@id="input-34"]')
        form.send_keys(Keys.CONTROL + "a")
        form.send_keys(Keys.DELETE)
        time.sleep(4)

# CLEAN SUBTITLE FORMAT AND ADD PROMPT
# Change the download directory here to your download directory 
directory = r'DOWNLOAD_DIRECTORY'
current_working_directory = os.getcwd()
noise_patterns = [r'\[English \(auto-generated\)\]', r'\[DownSub\.com\]']
prompts_directory = os.path.join(current_working_directory, 'prompts')

if not os.path.exists(prompts_directory):
    os.makedirs(prompts_directory)

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        lines = [line for line in lines if line.strip() != '']

        clean_name = filename
        for pattern in noise_patterns:
            clean_name = re.sub(pattern, '', clean_name)

        clean_name = clean_name.replace('.txt', '').strip()

        # Enter your desired prompt here
        prompt = (
            "ENTER_PROMPT_HERE"
        )
    
        lines.insert(0, prompt)
        
        with open(file_path, 'w') as file:
            file.writelines(lines)

        new_file_path = os.path.join(prompts_directory, filename)
        shutil.move(file_path, new_file_path)


