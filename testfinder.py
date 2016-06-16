from selenium import webdriver
from config import DRIVING_LICENSE_NUMBER, APPLICATION_REFERENCE_NUMBER
from config import TWILIO_SID, TWILIO_AUTH_KEY
from time import sleep
from datetime import datetime, time
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient


class TestFinder():
    def __init__(
            self, user, driver=webdriver.PhantomJS(),
            twilio=TwilioRestClient(TWILIO_SID, TWILIO_AUTH_KEY),
            debug=False):
        self.driver = driver
        self.user = user
        self.DEBUG = debug
        self.twilio_client = twilio

        if driver:
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
                "datetime": datetime.strptime(link.span.text,
                                              "%A %d %B %Y %I:%M%p"),
                "link": link["href"]
            })

        return times

    def filter_times(self, times):
        # Filter out days that are less than selected date (IF there is one)
        before_date = self.user.get("before_date", times[-1]["datetime"])
        # default to Set early time (4 in the morning)
        start_time = self.user.get("start_time", time(4, 0))
        # Set late time (11 night)
        end_time = self.user.get("end_time", time(23, 0))
        return_times = []

        for t in times:
            if t["datetime"] > before_date:
                break

            if (t["datetime"].time() > start_time and
                    t["datetime"].time() < end_time):
                # if time is between allocated times then we can add it
                return_times.append(t)

        return return_times

    def format_times(self, times):
        """
        Converts potential times into textable option
        """
        message = "Available Times:\n"
        i = 0
        while len(message) < 140:
            message += "{}) {}\n".format(i, times[i]["datetime"]
                                         .strftime("%a %d %b %H:%M"))
            i += 1

        return message

    def main(self):
        self.driver.get("https://driverpracticaltest.direct.gov.uk/login")

        self.login()

        self.select_date_change_on_view_booking()

        # Get the earliest dates
        self.select_earliest_available_test_date()

        times = self.scrape(self.driver.page_source)

        times = self.filter_times(times)
        if self.DEBUG:
            print(times)

        if times:
            m = self.format_times(times)
            self.send_message(m)


    def login(self):
        if self.DEBUG:
            print("Place in credentials")

        # Place in credentials
        self.input("driving-licence-number", self.user["license_number"])
        self.input(
            "application-reference-number", self.user["application_reference"])

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
        "before_date": datetime(2016, 7, 01),
        "start_time": time(10),
        "end_time": time(12)
    }
    tester = TestFinder(user, debug=True)
    try:
        tester.main()
    except Exception as e:
        print(e)
        tester.save_driver_state()
    finally:
        tester.close_session()
    # tester.send_message("Testing")

    # with open('test_html/available_times.html') as f:
    #     print(tester.scrape(f.read()))
