from selenium import webdriver
from selenium.webdriver.common.by import By

class SW_locators:
    Departure_Location = (By.ID, "originationAirportCode")
    Arrival_Location = (By.ID, "destinationAirportCode")
    Departure_Date = (By.ID, "departureDate")
    Return_Date = (By.ID,"returnDate")
    Round_Trip_Checkbox = (By.XPATH, "//span[contains(.,'Round trip')]")
    One_Way_Checkbox = (By.XPATH, "//li[2]/label/input") #need better locator
    Search_Button = (By.ID, "form-mixin--submit-button")
    Passenger_Count = (By.ID, "adultPassengersCount")
    Departure_Time = (By.ID, "departureTimeOfDay")
    Southwest_Logo = (By.CSS_SELECTOR, ".header-booking--logo")
    Book_Flight_Button = (By.ID, "air-booking-product-1")
    Continue_Button = (By.XPATH, "//button[contains(.,'Continue')]")