from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import time

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		if self.browser:
			self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		time.sleep(3)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(3)

		table = self.browser.find_element_by_id('id_list_table')

		rows = table.find_elements_by_tag_name('tr')

		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])	

		# self.assertTrue(
		# 	any(row.text == '1: Buy peacock feathers' for row in rows),
		# 	'New to-do item did not appear in table -- its text was: \n%s' % (table.text, ),
		# )

		self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])	


		self.browser.quit()
		self.browser = webdriver.Firefox()

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('Buy peacock feathers', page_text)
		self.assertIn('make a fly', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox = self.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/list/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		



		self.fail("Finish the test!")

	# def test_layout_and_styling(self):
	# 	self.browser.get('self.live_server_url')
	# 	self.browser.set_window_size(1024, 768)

	# 	inputbox = self.browser.find_element_by_id('id_new_item')
	# 	self.assertAlmostEqual(
	# 		inputbox.location['x'] + input.size['width']/2,
	# 		512,
	# 		delta=5
	# 	)


