from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randint
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pycurl
from io import BytesIO
from lxml import html
import warnings, pickle, os, openai, re, datetime, json, requests
from selenium.webdriver.common.keys import Keys
import os
import requests
import random

# api-endpoint
URL = "https://script.google.com/macros/s/AKfycby7yBG9QtwQQdgSEepvs8hh1HSVoTbAQ3RwD-DCom4L5xAnGZvdzUpek_Oj73gb2ZHRTg/exec?action=getRows"
r = requests.get(url = URL)

# extracting data in json format



if os.path.exists("followers.txt"):
  os.remove("followers.txt")
global proxy_host, proxy_pass, proxy_user, proxy_port, queue, i, good_leads_counter, duplicates

i=0
queue=[]
good_leads_counter=0
duplicates = r.json()['data']
newleads = []

## Proxy config ##
proxy_user = "7ac9f92924a78ee2c13a"
proxy_pass = "bfa123ba2c1b8118~k5ixWEYjP57"
proxy_host = "103.14.27.67"
proxy_port = "823"

## Instagram creds ##
ig_login_username1="shaurya.pal.2007"
ig_login_password1="Rekha@1980"
ig_login_username2='shauryapal.07'
ig_login_password2='Tech@2023'

## API KEY ##
openai.api_key = "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"

# USER_TO_SEARCH = input("Enter profile name: ")

# queue.append(USER_TO_SEARCH)

def sanitize_username(username):
    return re.sub(r'[^\w\-_\. ]', '_', username)

def scrape(usr, username, password):

        TIMEOUT = 30

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        options.add_argument("--headless")
        options.headless = True
        mobile_emulation = {
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        bot = webdriver.Chrome(options=options)

        bot.get('https://www.instagram.com/accounts/login/')

        time.sleep(1)

        #Remove cookies pop-up IF it comes 
        try:
            element = bot.find_element(By.XPATH,"/html/body/div[4]/div/div/div[3]/div[2]/button")
            element.click()
            
        except NoSuchElementException:
            print("")


        # Generate a cookie file name based on username
        cookie_file = sanitize_username(username) + ".pkl"

        # Check if cookies already exist
        if os.path.exists(cookie_file):
            with open(cookie_file, "rb") as file:
                cookies = pickle.load(file)

            bot.delete_all_cookies()
            print("Deleted all cookies")
            for cookie in cookies:
                cookie['domain'] = '.instagram.com'
                try:
                    bot.add_cookie(cookie)
                except:
                    pass

            bot.refresh()
            print(f"[+] Cookies loaded for {username}")

        else:
            # If cookies do not exist, log in to save them
            print(f"[*] Logging in as {username}", flush=True)
            bot.get("https://www.instagram.com/accounts/login")
            
            username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            
            # Click login button
            WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            
            time.sleep(random.randint(7,10))
            
            # Save cookies
            cookies = bot.get_cookies()
            with open(cookie_file, "wb") as file:
                pickle.dump(cookies, file)

            print(f"[+] Cookies saved for {username}")



        bot.get('https://www.instagram.com/{}/'.format(usr))

        time.sleep(4)

        try:
            WebDriverWait(bot, TIMEOUT).until(
                EC.presence_of_element_located((
                    By.XPATH, "//a[contains(@href, '/following')]"))).click()
        
        except:
            bot.quit()
            scrape(random.choice(r.json()['data']), ig_login_username1, ig_login_password1)
            return

        time.sleep(3)

        print('Scraping...')

        users = set()

        end_of_scroll_region = False
        last_position = 1

        while end_of_scroll_region == False:

            curr_position = bot.execute_script("return window.pageYOffset;")
            print(curr_position)

            if curr_position == last_position:
                print("Reached page end!")
                end_of_scroll_region = True
            else:
                ActionChains(bot).send_keys(Keys.END).perform()
                time.sleep(randint(1,3))
                ActionChains(bot).send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(randint(3,10))

            last_position = curr_position
        

        #for _ in range(round(user_input // 20)):


        followers = bot.find_elements(By.XPATH,
        "//a[contains(@href, '/')]")

        # Getting url from href attribute
        for i in followers:
            if i.get_attribute('href'):
                users.add(i.get_attribute('href').split("/")[3])
            else:
                continue

       
        with open('followers.txt', 'w') as file:
            file.write('\n'.join(users) + "\n")

        print('[+] Followers saved as followers.txt file!')
        
        bot.back()

while i < 99999999:
    print(newleads)
    try:
        profile = random.choice(r.json()['data'])
    except:
        print("\nDone!")
        sys.exit(0)
    
    print(f"###### Processing profile: {profile} ######")

    if random.random() < 0.5:
        scrape(profile, ig_login_username1, ig_login_password1)
    else:
        scrape(profile, ig_login_username2, ig_login_password2)


    # Execute below function for fetching bio from 9 different browsers, checking eligiblity and adding as good/bad lead.
    with open("followers.txt", "r+") as file:
        lines = file.readlines()

    users_to_bio = []

    for l in lines:
        username = l.replace('\n', "")
        #print(username)
        users_to_bio.append(username)

    users_to_bio.pop(0)
    users_to_bio = list(set(users_to_bio))

    users_to_bio = [item for item in users_to_bio if "?xmt" not in item]

    try:
        users_to_bio.remove("blog")
    except:
        pass
    try:
        users_to_bio.remove("explore")
    except:
        pass
    try:
        users_to_bio.remove("docs")
    except:
        pass
    try:
        users_to_bio.remove("shauryapal.07")
    except:
        pass
    try:
        users_to_bio.remove("?xmt=AQGz-YKVXIJJhojpYfbT_SbPKZRxW-CnaLmU-N8H-fq4nTY")
    except:
        pass
    try:
        users_to_bio.remove("legal")
    except:
        pass
    try:
        users_to_bio.remove("direct")
    except:
        pass
    try:
        users_to_bio.remove("reels")
    except:
        pass
    try:
        users_to_bio.remove("about-us")
    except:
        pass
    try:
        users_to_bio.remove("accounts")
    except:
        pass

    # Function to process one user's Instagram page
    def fetch_bio(user):
        global proxy_host, proxy_pass, proxy_user, proxy_port, good_leads_counter, duplicates

        if user in duplicates:
            print("[*] Duplicate Lead, Passing on")
            return
        
        # proxy_address = f"http://{proxy_user}:{proxy_pass}@gate.smartproxy.com:7000"
        proxy_address  = f"7ac9f92924a78ee2c13a:bfa123ba2c1b8118@gw.dataimpulse.com:823"

        my_headers = {
            "Content-Type": "application/json",
        }
        
        try:
            # Visit Instagram page
            url = f"https://imginn.com/{user}/"

            curl = pycurl.Curl()
            curl.setopt(curl.URL, url)
            curl.setopt(curl.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
            curl.setopt(curl.PROXY, proxy_address)
            buffer = BytesIO()
            curl.setopt(curl.WRITEDATA, buffer)

            curl.perform()
            curl.close()
            response_text = buffer.getvalue().decode('utf-8')
            tree = html.fromstring(response_text)
            #print("\n\n")
            #input(response_text)
            bio_text = tree.xpath("//div[@class='bio']/text()")
            username_of_user = tree.xpath("//h1/text()")
            is_private = tree.xpath("//div[@class='error']/text()")
            #print(is_private[0].strip())

            try:
                if 'private' in is_private[0].strip():
                    print("[*] Skipping private account.")
                    return
            except:
                pass

            #print("Full without index: ", bio_text)

            if bio_text:
                print(f"[+] Bio of {user}:", bio_text[0].strip())
                bio_text = 'Profile name: ' + username_of_user[0].strip() + '\nBio: ' + bio_text[0].strip()
            else:
                print(f"[-] Bio not found for user: {user}")
                return


            openai.api_key = "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"


            def chat_with_gpt(prompt):
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": """Conditions
Is this profile owned by a male?
Is this an ONLINE coach?
Is this a weight/fat loss or weight gain or muscle building or nutrition coach?
This should not be a performance,  conditioning, wellness, life, S&C, jiu jitsu, MMA, martial arts, Muay Thai, Weightlifting or strength coach.
Is this person from America or Canada?
Respond in JSON format with 'fitness_coach' as true if all conditions are true, otherwise false
"""},
                        {"role": "user", "content": prompt}
                    ]
                )

                return response.choices[0].message.content.strip()

            if  "fitness" in str(bio_text).lower() or "health" in str(bio_text).lower() or "physical" in str(bio_text).lower() or "physique" in str(bio_text).lower() or "weight" in str(bio_text).lower() or "fat" in str(bio_text).lower()or "trainer" in str(bio_text).lower()or "1-1" in str(bio_text).lower()or "nutrition" in str(bio_text).lower()or "ifbb" in str(bio_text).lower():
                if "coach" in str(bio_text).lower() and ("online" in str(bio_text).lower() or "dm" in str(bio_text).lower()) and "business" not in str(bio_text).lower()  and "design" not in str(bio_text).lower() and "ads" not in str(bio_text).lower() and "market" not in str(bio_text).lower()and "female" not in str(bio_text).lower()and "woman" not in str(bio_text).lower()and "women" not in str(bio_text).lower()and "girl" not in str(bio_text).lower():
                    duplicates.append(user)
                    newleads.append(user)
                    data = {
                        "data": user,
                        "action": "add-good-lead"
                    }

                    raw = json.dumps(data)          
                    requests.post("https://script.google.com/macros/s/AKfycbzy_13Gohe81gvV-_o1u_bSA8zm3lKrAzScnhmWmd-Va123yY2XxkBE-NwG7MFZcWZNiA/exec", headers=my_headers, data=raw)

                    good_leads_counter +=1
                    if good_leads_counter % 50 == 0:
                        print("\n[*]Sleeping for 1 hour")
                        time.sleep(3600)
        except Exception as e:
            print(user, f"Error: {e}")
            print(bio_text)
            return
            
    # Main function to run the scraping in parallel
    def scrape_bios_concurrently(users, num_threads=4):
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
        
        bios = {}
        
        # Using ThreadPoolExecutor to run tasks in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit each user to be processed in parallel
            try:
                futures = {executor.submit(fetch_bio, user): user for user in users}
            except Exception as e:
                print(e)    

    # Example usage
    resulting_bios = scrape_bios_concurrently(users_to_bio)
    print("This is queue now:")
    print(queue)

    if profile in queue:
        queue.remove(profile)

print(newleads)