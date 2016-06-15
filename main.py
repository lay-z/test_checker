from selenium import webdriver
from config import (DRIVING_LICENSE_NUMBER, 
    APPLICATION_REFERENCE_NUMBER, TWILIO_SID, TWILIO_AUTH_KEY)
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient


class TestFinder():
    def __init__(self, user, driver=webdriver.PhantomJS(), debug=False):
        self.driver = driver
        self.user = user
        self.DEBUG = debug
        self.twilio_client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_KEY)

        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1080, 800)

    def send_message(self, txt):
        response = self.twilio_client.messages.create(body=txt,
            to="+447528149491",
            from_="+447481339875")

        print(response)

    def input(self, id, text=None):
        # Wait a second to make it more human
        sleep(1)
        if text:
            self.driver.find_element_by_id(id).send_keys(text)
        else:
            self.driver.find_element_by_id(id).click()

    def scrape(self, html):
        """
        extracts out available test times
        """
        times = []
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find("ul", "button-board").find_all("a")
        for link in links:
            times.append({
                "datetime": datetime.strptime(link.span.text, "%A %d %B %Y %H:%M%p"),
                "link": link["href"]
            })

        return times

    def main(self):
        self.driver.get("https://driverpracticaltest.direct.gov.uk/login")

        self.login()

        self.select_date_change_on_view_booking()
        # Get the earliest dates

        times = self.scrape(self.driver.page_source)
        if self.DEBUG:
            print(times)

    def login(self):
        if self.DEBUG:
            print("Place in credentials")

        # Place in credentials
        self.input("driving-licence-number", self.user["license_number"])
        self.input("application-reference-number", self.user["application_reference"])

        self.input("booking-login")
        # TODO check credentials are right? after loading page

    def select_date_change_on_view_booking(self):
        # Change the date
        if self.DEBUG:
            print("clickingo on changing date")

        self.input("date-time-change")

    def select_earliest_available_test_date(self):
        if self.DEBUG:
            print("selecting earliest dates")

        self.input("test-choice-earliest")
        self.input("driving-licence-submit")

    def close_session(self):
        self.driver.close()

    def save_driver_state(self):
        time = datetime.now()
        self.driver.save_screenshot('error_images/{}.png'.format(time))
        with open('error_images/{}.html'.format(time), 'w+') as file:
            file.write(self.driver.page_source.encode('utf8'))

if __name__ == '__main__':
    user = {
        "license_number": DRIVING_LICENSE_NUMBER,
        "application_reference": APPLICATION_REFERENCE_NUMBER,
        "phone_number": "+447528149491",
        "last_acceptable_date": datetime(2016, 8, 20)
    }
    tester = TestFinder(user)
    # try:
    #     tester.main()
    # except Exception as e:
    #     print("Exception occured!")
    #     print(e)
    #     time = datetime.now()
    #     tester.driver.save_screenshot('error_images/{}.png'.format(time))
    #     with open('error_images/{}.html'.format(time), 'w+') as error_file:
    #         error_file.write(tester.driver.page_source.encode('utf8'))
    #     tester.driver.save_screenshot('test.png')
    #     tester.close_session()
    tester.send_message("Testing")

    # with open('test_html/available_times.html') as f:
    #     print(tester.scrape(f.read()))
