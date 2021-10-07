from selenium import webdriver
from selenium.webdriver.common.by import By

class SW_locators:
    class SW_Advanced_Flight_Search:
        Departure_Location = (By.ID, "originationAirportCode")
        Arrival_Location = (By.ID, "destinationAirportCode")
        Departure_Date = (By.ID, "departureDate")
        Return_Date = (By.ID,"returnDate")
        Round_Trip_Checkbox = ()
        One_Way_Checkbox = ()
        Search_Button = (By.ID, "form-mixin--submit-button")