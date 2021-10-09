from locators import SW_locators
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import sys, argparse, random
from time import sleep
from datetime import datetime

southwest_start_url = "https://www.southwest.com/air/booking/index.html?int=HOME-BOOKING-WIDGET-ADVANCED-AIR"

parser = argparse.ArgumentParser(description='This is a CL tool to automate the booking of flights through Southwest Airlines.')
parser.add_argument("DEPART_IATA", help = "Enter the three letter airport code for departure location",type=str)
parser.add_argument("ARRIVAL_IATA", help = "Enter the three letter airport code for arrival location",type=str)
parser.add_argument("DEPART_DATE", help = "Enter the departure date in the format MM/DD",type=str)
parser.add_argument("NUM_PASSENGERS", help = "Enter the number of adult passengers for this flight",type=int)
parser.add_argument("TIME_OF_DAY", help = "Enter a number from 1-4 corresponding to the desired time of day. [1]-Anytime, [2]-Before Noon, [3]-Noon - 6PM, [4]-After 6PM" ,type=int)
parser.add_argument("FLIGHT_TYPE", help = "Enter a single character corresponding to the ticket type: [B]-Business Select, [A]-Anytime, [W]-Wanna Get Away",type=str)
parser.add_argument("MAX_PRICE", help = "Enter the maximum ticket price",type=int)
args = parser.parse_args()

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

def type_slow(to_enter,element):
    for i in range(0,len(to_enter)):
        element.send_keys(to_enter[i])
        sleep_number = .10 + .01*random.randint(1,10)
        sleep(sleep_number)

if __name__ == "__main__":
    #1. Parse CL input for commands
    depart = args.DEPART_IATA
    arrival = args.ARRIVAL_IATA
    dept_Date = args.DEPART_DATE
    passengers = args.NUM_PASSENGERS
    time_of_day = ''
    flight_type = ''
    max_price = args.MAX_PRICE

    if args.TIME_OF_DAY == 1:
        time_of_day = "All day"
    elif args.TIME_OF_DAY == 2:
        time_of_day = "Before noon"
    elif args.TIME_OF_DAY == 3:
        time_of_day = "Noon - 6pm"
    elif args.TIME_OF_DAY == 4:
        time_of_day = "After 6pm"

    if args.FLIGHT_TYPE == 'B':
        flight_type = "Business Select"
    elif args.FLIGHT_TYPE == 'A':
        flight_type = "Anytime"
    elif args.FLIGHT_TYPE == 'W':
        flight_type = "Wanna Get Away"

    #2. Sanitize inputs such as Depart and Arrival Code, ETC.
    assert(len(depart) == len(arrival) == 3)
    assert(len(dept_Date) == 5) #cur_time = datetime.today().strftime('%m-%d') - TODO: implement departure date check, within 5 months of cur time
    assert(passengers >= 1 and passengers <= 8)
    assert(time_of_day != '')
    assert(flight_type != '')
    assert(max_price > 0)

    #3. Open the start url
    cdriver.get(southwest_start_url)

    #click one way
    cdriver_wait.until(EC.element_to_be_clickable(SW_locators.One_Way_Checkbox))
    cdriver.find_element_by_xpath(SW_locators.One_Way_Checkbox[1]).click()

    #enter depart airport code
    element = cdriver.find_element_by_id(SW_locators.Departure_Location[1])
    type_slow(depart,element)
    cdriver.find_element_by_xpath("//button[contains(.,\"" + depart + "\")]").click()

    #enter arrival airport code
    element = cdriver.find_element_by_id(SW_locators.Arrival_Location[1])
    type_slow(arrival,element)
    cdriver.find_element_by_xpath("//button[contains(.,\"" + arrival + "\")]").click()

    #enter depart date
    element = cdriver.find_element_by_id(SW_locators.Departure_Date[1])
    element.click()
    element.send_keys(Keys.DELETE)
    type_slow(dept_Date,element)

    #enter time of day
    cdriver.find_element_by_id(SW_locators.Departure_Time[1]).click()
    cdriver.find_element_by_xpath("//button[contains(.,\"" + time_of_day + "\")]").click()

    #enter number of passengers
    cdriver.find_element_by_id(SW_locators.Passenger_Count[1]).click()
    cdriver.find_element_by_xpath("//button[contains(.,\"" + str(passengers) + "\")]").click()

    #4click search
    element = cdriver.find_element_by_id(SW_locators.Search_Button[1]).click()
    #sleep(5)

    #wait for page to load
    cdriver_wait.until(EC.element_to_be_clickable(SW_locators.Southwest_Logo))

    #GET tuple OF PRICES for each row VIA ID=BOOING-FARES-0-1, 0-2, etc
    elements = cdriver.find_elements_by_id("air-booking-fares-0-1")
    #print((elements[0]).text) prints 3 prices
    '''
    While selenium can find air-booking-fares-0-X/ [0-2]:(1-3)

    //div[@id='air-booking-fares-0-1']/div[3]/button
    '''
    
    
    cdriver.close()