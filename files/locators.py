#class file of locators for expidition of automation
from selenium import webdriver
from selenium.webdriver.common.by import By


class SW_locators:
    class SW_Flight_Search_Bar:
        Departure_Location = (By.ID, "LandingAirBookingSearchForm_originationAirportCode")
        Arrival_Location = (By.ID, "LandingAirBookingSearchForm_destinationAirportCode")
        Departure_Date = (By.ID, "LandingAirBookingSearchForm_departureDate")
        Return_Date = (By.ID,"LandingAirBookingSearchForm_returnDate")
        One_Way_Checkbox = ()
        Round_Trip_Checkbox = ()