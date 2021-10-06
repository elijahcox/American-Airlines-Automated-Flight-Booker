#main file used to take in input
import locators, functions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

opt = Options()
opt.headless = True
cdriver = webdriver.Chrome('../chromedriver', options = opt)
arglist = sys.argv
arglen = len(arglist)


def __main__():
    #do main operations