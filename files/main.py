from locators import SW_locators
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys, argparse, functions
from time import sleep
from datetime import datetime

southwest_start_url = "https://www.southwest.com/air/booking/index.html?int=HOME-BOOKING-WIDGET-ADVANCED-AIR"

options = Options()
options.headless = False
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
cdriver = webdriver.Chrome('../chromedriver', options = options)
cdriver.maximize_window()
cdriver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'})
cdriver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
cdriver_wait = WebDriverWait(cdriver, 10)

parser = argparse.ArgumentParser(description='This is a CL tool to automate the booking of flights through Southwest Airlines.')
parser.add_argument("DEPART", help = "Enter the three letter airport code for departure location",type=str)
parser.add_argument("ARRIVAL", help = "Enter the three letter airport code for arrival location",type=str)
parser.add_argument("DEPART_DATE", help = "Enter the departure date in the format MM/DD",type=str)
#parser.add_argument("ARRIVAL DATE", help = "Enter the three letter airport code for arrival location")
args = parser.parse_args()

def type_slow(to_enter,element):
    for i in range(0,len(to_enter)):
        element.send_keys(to_enter[i])
        sleep(.15)

if __name__ == "__main__":
    #1. Parse CL input for commands
    depart = args.DEPART
    arrival = args.ARRIVAL
    dept_Date = args.DEPART_DATE

    #2. Sanitize inputs such as Depart and Arrival Code, ETC.
    assert(len(depart) == len(arrival) == 3)
    assert(len(dept_Date) == 5) #cur_time = datetime.today().strftime('%m-%d') - TODO: implement departure date check, within 5 months of cur time

    #3. Open the start url
    cdriver.get(southwest_start_url)

    #click one way
    cdriver_wait.until(EC.element_to_be_clickable(SW_locators.One_Way_Checkbox))
    element = cdriver.find_element_by_xpath(SW_locators.One_Way_Checkbox[1])
    element.click()

    #enter depart airport code
    cdriver_wait.until(EC.element_to_be_clickable(SW_locators.Departure_Location))
    element = cdriver.find_element_by_id(SW_locators.Departure_Location[1])
    type_slow(depart,element)
    element = cdriver.find_element_by_xpath("//button[contains(.,\"" + depart + "\")]").click()

    #enter arrival airport code
    cdriver_wait.until(EC.element_to_be_clickable(SW_locators.Arrival_Location))
    element = cdriver.find_element_by_id(SW_locators.Arrival_Location[1])
    type_slow(arrival,element)
    element = cdriver.find_element_by_xpath("//button[contains(.,\"" + arrival + "\")]").click()

    #enter depart date
    cdriver_wait.until(EC.element_to_be_clickable(SW_locators.Departure_Date))
    element = cdriver.find_element_by_id(SW_locators.Departure_Date[1])
    element.click()
    element.send_keys(Keys.DELETE + dept_Date + Keys.ESCAPE)

    #4click search
    element = cdriver.find_element_by_id(SW_locators.Search_Button[1]).click()
    sleep(5)
    
    cdriver.close()