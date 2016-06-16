from unittest import TestCase
from testfinder import TestFinder
from datetime import datetime, time


class TestFilterTimes(TestCase):

	def setUp(self):
		u = {"before_date": datetime(2016, 9, 14)}
		self.t = TestFinder(u, None, None, debug=True)
		self.times = [	
			{'datetime': datetime(2016, 9, 13, 13, 25)},
			{'datetime': datetime(2016, 9, 13, 13, 45)},
			{'datetime': datetime(2016, 9, 13, 14, 22)},
			{'datetime': datetime(2016, 9, 13, 14, 42)},
			{'datetime': datetime(2016, 9, 14, 13, 25)},
			{'datetime': datetime(2016, 9, 14, 13, 45)},
			{'datetime': datetime(2016, 9, 14, 14, 22)},
			{'datetime': datetime(2016, 9, 14, 14, 42)},
			{'datetime': datetime(2016, 9, 15, 10, 4)},
			{'datetime': datetime(2016, 9, 15, 10, 24)},
			{'datetime': datetime(2016, 9, 15, 11, 1)},
			{'datetime': datetime(2016, 9, 15, 11, 21)},
			{'datetime': datetime(2016, 9, 15, 13, 25)},
			{'datetime': datetime(2016, 9, 15, 13, 45)},
			{'datetime': datetime(2016, 9, 15, 14, 22)},
			{'datetime': datetime(2016, 9, 15, 14, 42)},
			{'datetime': datetime(2016, 9, 16, 14, 22)},
			{'datetime': datetime(2016, 9, 16, 14, 42)},
			{'datetime': datetime(2016, 9, 19, 10, 4)},
			{'datetime': datetime(2016, 9, 19, 10, 24)}
		]

	def test_should_be_able_to_filter_available_dates(self):
		# when
		u = {"before_date": datetime(2016, 9, 15)}
		self.t.user = u
		filtered_times = self.t.filter_times(self.times)

		# then
		self.assertEqual(len(filtered_times), 8)
		self.assertEqual(filtered_times, self.times[:8])

	def test_should_not_find_any_acceptable_dates(self):
		# when
		u = {"before_date": datetime(2016, 9, 13)}
		self.t.user = u

		filtered_times = self.t.filter_times(self.times)

		# then
		self.assertEqual(len(filtered_times), 0)

	def test_should_not_find_any_acceptable_slots(self):
		self.t.user = {
			"start_time": time(10),
			"end_time": time(12)
		}	
		
		# when
		filtered_times = self.t.filter_times(self.times)

		# then
		self.assertEqual(len(filtered_times), 6)		

	def test_should_have_one_time_remaining(self):

		self.t.user = {
			"start_time": time(10),
			"end_time": time(13, 30),
			"before_date": datetime(2016, 9, 14)
		}
		
		# when
		filtered_times = self.t.filter_times(self.times)

		# then
		self.assertEqual(len(filtered_times), 1)		



class TestScrapeTimes(TestCase):
	def setUp(self):
		self.t = TestFinder(None, None, None, debug=True)

	def test_should_find_20_times(self):
		with open('tests/test_html/available_times.html') as test_html:
			times = self.t.scrape(test_html)


	def test_should_correct_convert_afternoon_times(self):
		with open('tests/test_html/available_times.html') as test_html:
			times = self.t.scrape(test_html)
			expected = datetime(2016, 9, 12, 14, 42)

			self.assertEqual(times[0]["datetime"], expected)

	def test_should_correct_convert_morning_times(self):
		with open('tests/test_html/available_times.html') as test_html:
			times = self.t.scrape(test_html)
			expected = datetime(2016, 9, 13, 11, 21)

			self.assertEqual(times[1]["datetime"], expected)



class TestFormatTimes(TestCase):
	def test_should_produce_message_of_less_that_160_characters(self):
		t = TestFinder(None, None, None, debug=True)
		times = [	
			{'datetime': datetime(2016, 9, 13, 13, 25)},
			{'datetime': datetime(2016, 9, 13, 13, 45)},
			{'datetime': datetime(2016, 9, 13, 14, 22)},
			{'datetime': datetime(2016, 9, 13, 14, 42)},
			{'datetime': datetime(2016, 9, 14, 13, 25)},
			{'datetime': datetime(2016, 9, 14, 13, 45)},
			{'datetime': datetime(2016, 9, 14, 14, 22)},
			{'datetime': datetime(2016, 9, 14, 14, 42)},
			{'datetime': datetime(2016, 9, 15, 10, 4)},
			{'datetime': datetime(2016, 9, 15, 10, 24)},
			{'datetime': datetime(2016, 9, 15, 11, 1)},
			{'datetime': datetime(2016, 9, 15, 11, 21)},
			{'datetime': datetime(2016, 9, 15, 13, 25)},
			{'datetime': datetime(2016, 9, 15, 13, 45)},
			{'datetime': datetime(2016, 9, 15, 14, 22)},
			{'datetime': datetime(2016, 9, 15, 14, 42)},
			{'datetime': datetime(2016, 9, 16, 14, 22)},
			{'datetime': datetime(2016, 9, 16, 14, 42)},
			{'datetime': datetime(2016, 9, 19, 10, 4)},
			{'datetime': datetime(2016, 9, 19, 10, 24)}
		]

		m = t.format_times(times)
		print(m)
		self.assertLessEqual(len(m), 160)
