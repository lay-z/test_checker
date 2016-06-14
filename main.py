from selenium import webdriver
from config import DRIVING_LICENSE_NUMBER, APPLICATION_REFERENCE_NUMBER
from time import sleep


def run(function):
    # Wait a second make it a bit more userlike
    sleep(1)
    function()


def main():
    driver = webdriver.PhantomJS()
    driver.get("https://www.gov.uk/change-driving-test")

    # Place in credentials
    run(lambda x: driver.find_element_by_id("driving-licence-number")
        .send_keys(DRIVING_LICENSE_NUMBER))
    run(lambda x: driver.find_element_by_id("application-reference-number")
        .send_keys(APPLICATION_REFERENCE_NUMBER))

    run(lambda x: driver.find_element_by_id("booking-login")
        .click())
