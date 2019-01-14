from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

# Create your tests here.

class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1 + 1, 2)

		
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_corrent_html(self):
		request = HttpRequest()
		response = home_page(request)
		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>', html)
		self.assertTrue(html.endswith('</html>'))

	def test_home_page_return_corrent_html2(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)





