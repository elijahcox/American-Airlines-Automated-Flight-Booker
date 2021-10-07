import locators, functions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys, time

southwest_start_url = "https://www.southwest.com/air/booking/index.html?int=HOME-BOOKING-WIDGET-ADVANCED-AIR"

options = Options()
options.headless = True
cdriver = webdriver.Chrome('../chromedriver', options = options)
arglist = sys.argv

def print_usage():
    print("Usage: ")
    return    

if __name__ == "__main__":
    cdriver.get(southwest_start_url)
    