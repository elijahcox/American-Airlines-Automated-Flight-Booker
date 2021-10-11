from locators import SW_locators
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os, sys, argparse, random
from time import sleep

southwest_start_url = "https://www.southwest.com/air/booking/index.html?int=HOME-BOOKING-WIDGET-ADVANCED-AIR"
parser = argparse.ArgumentParser(description='This is a CL tool to automate the booking of flights through Southwest Airlines.')
parser.add_argument("DEPART_IATA", help = "Enter the three letter airport code for departure location",type=str)
parser.add_argument("ARRIVAL_IATA", help = "Enter the three letter airport code for arrival location",type=str)
parser.add_argument("DEPART_DATE", help = "Enter the departure date in the format MM/DD",type=str)
parser.add_argument("NUM_PASSENGERS", help = "Enter the number of adult passengers for this flight",type=int)
parser.add_argument("TIME_OF_DAY", help = "Enter a number from 1-4 corresponding to the desired time of day. [1]-Anytime, [2]-Before Noon, [3]-Noon - 6PM, [4]-After 6PM" ,type=int)
parser.add_argument("FLIGHT_TYPE", help = "Enter a single character corresponding to the ticket type: [1]-Business Select, [2]-Anytime, [3]-Wanna Get Away",type=int)
parser.add_argument("MAX_PRICE", help = "Enter the maximum ticket price",type=int)
args = parser.parse_args()
options = Options()
options.headless = False
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("detach", True)
cdriver = webdriver.Chrome('../chromedriver', options = options)
cdriver.maximize_window()
cdriver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'})
cdriver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
cdriver_wait = WebDriverWait(cdriver, 10)

def type_data(to_enter,element):
    for i in range(0,len(to_enter)):
        element.send_keys(to_enter[i])
        sleep_number = .10 + .01*random.randint(1,10)
        sleep(sleep_number)

def load_element(locator):
    cdriver_wait.until(EC.element_to_be_clickable(locator))#wait for page to load

def click_one_way():
    cdriver.find_element_by_xpath(SW_locators.One_Way_Checkbox[1]).click()

def enter_iata(locator, iata_to_enter):
    element = cdriver.find_element_by_id(locator)
    type_data(iata_to_enter,element)
    cdriver.find_element_by_xpath("//button[contains(.,\"" + iata_to_enter + "\")]").click()

def enter_time_of_day():
    cdriver.find_element_by_id(SW_locators.Departure_Time[1]).click()
    cdriver.find_element_by_xpath("//button[contains(.,\"" + time_of_day + "\")]").click()

def enter_passengers():
    cdriver.find_element_by_id(SW_locators.Passenger_Count[1]).click()
    cdriver.find_element_by_xpath("//button[contains(.,\"" + str(args.NUM_PASSENGERS) + "\")]").click()

def enter_departure():
    element = cdriver.find_element_by_id(SW_locators.Departure_Date[1])#enter depart date
    element.click()
    element.send_keys(Keys.DELETE)
    type_data(args.DEPART_DATE,element)

def get_lowest_price():#returns a webdriver element pointing to the lowest price ticket
    i = 1
    min_price = args.MAX_PRICE + 1
    min_price_element = ''
    cur_price = ''
    builder = "air-booking-fares-0-" #builder += str(i)
    elements = cdriver.find_elements_by_id(builder + str(i)) #get first row of prices
    while len(elements) > 0:
        element = elements[0].find_element_by_xpath("//div[@id=\"" + builder + str(i) + "\"]/div[" + str(args.FLIGHT_TYPE) + "]/button")
        if element.text[0] == '$':
            err_check = element.text.find('\n')
            if err_check != -1: #check for n left
                cur_price = int(element.text[1:err_check])
            else:
                cur_price = int(element.text[1:])
                
            if  cur_price < min_price:
                min_price = cur_price
                min_price_element = element
        i+=1
        elements = cdriver.find_elements_by_id(builder + str(i))
    return min_price_element

if __name__ == "__main__":
    time_of_day = ''
    if args.TIME_OF_DAY == 1:
        time_of_day = "All day"
    elif args.TIME_OF_DAY == 2:
        time_of_day = "Before noon"
    elif args.TIME_OF_DAY == 3:
        time_of_day = "Noon - 6pm"
    elif args.TIME_OF_DAY == 4:
        time_of_day = "After 6pm"

    assert(len(args.DEPART_IATA) == len(args.ARRIVAL_IATA) == 3) #Sanitize inputs such as Depart and Arrival Code, ETC.
    assert(len(args.DEPART_DATE) == 5)
    assert(args.NUM_PASSENGERS >= 1 and args.NUM_PASSENGERS <= 8)
    assert(time_of_day != '')
    assert(args.FLIGHT_TYPE >= 1 and args.FLIGHT_TYPE <= 3)
    assert(args.MAX_PRICE > 0)
    
    cdriver.get(southwest_start_url)#Open the start url
    load_element(SW_locators.One_Way_Checkbox)#wait for search bar to load
    click_one_way() #click one way option
    enter_iata(SW_locators.Departure_Location[1],args.DEPART_IATA) #enter depart airport code
    enter_iata(SW_locators.Arrival_Location[1],args.ARRIVAL_IATA)#enter arrival airport code
    enter_time_of_day() #enter time of day
    enter_passengers() #enter number of passengers
    enter_departure() #enter departure date
    cdriver.find_element_by_id(SW_locators.Search_Button[1]).click()#click search
    load_element(SW_locators.Southwest_Logo)#wait for page to load
    min_price_element = get_lowest_price()
    try:
        min_price_element.location_once_scrolled_into_view
        min_price_element.click()
    except AttributeError:
        print("Could not find a cheap enough ticket for the specified price")
        exit()

    load_element(SW_locators.Book_Flight_Button)
    cdriver.find_element_by_id(SW_locators.Book_Flight_Button[1]).click()
    sleep(1)
    load_element(SW_locators.Southwest_Logo)
    
    cont = cdriver.find_element_by_xpath(SW_locators.Continue_Button[1])
    cont.location_once_scrolled_into_view
    cont.click()