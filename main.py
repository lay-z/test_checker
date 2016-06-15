from selenium import webdriver
from config import (DRIVING_LICENSE_NUMBER, 
    APPLICATION_REFERENCE_NUMBER, TWILIO_SID, TWILIO_AUTH_KEY)
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient


class TestFinder():
    def __init__(self, driver=webdriver.PhantomJS()):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1080,800)
        self.twilio_client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_KEY)

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

        # Place in credentials
        print("Place in credentials")
        self.input("driving-licence-number", DRIVING_LICENSE_NUMBER)
        self.input("application-reference-number", APPLICATION_REFERENCE_NUMBER)

        self.input("booking-login")

        # TODO check credentials are right? after loading page

        # Change the date
        print("clickingo on changing date")
        self.input("date-time-change")

        # Get the earliest dates
        print("Getting the earliest dates")
        self.input("test-choice-earliest")
        self.input("driving-licence-submit")

        times = self.scrape(self.driver.page_source)
        print(times)

        self.driver.close()


if __name__ == '__main__':
    tester = TestFinder()
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
    #     tester.driver.close()
    tester.send_message("Testing")

    # with open('test_html/available_times.html') as f:
    #     print(tester.scrape(f.read()))
