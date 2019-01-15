from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template import RequestContext

import re

from lists.models import Item


from lists.views import home_page

# Create your tests here.

class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1 + 1, 2)

		
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_return_corrent_html(self):
		request = HttpRequest()
		response = home_page(request)
		html = response.content.decode()
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>', html)
		self.assertTrue(html.endswith('</html>'))

	def test_home_page_return_corrent_html2(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html', request=request)
		# self.assertEqual(response.content.decode(), expected_html)
		self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))

	def test_home_page_can_save_a_post_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)
		self.assertIn('A new list item', response.content.decode())
		expected_html = render_to_string(
			'home.html',
			{'new_item_text': 'A new list item'},
			request=request
		)
		"""
		self.assertEqual(response.content.decode(), expected_html)
		测试不通过
		解决方案有2种
		1、将django降级到1.8,并且
		render_to_string函数中添加request=request参数
		2、删除csrfmiddlewaretoken相关信息
		"""
		# self.assertEqual(response.content.decode(), expected_html)
		self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))



def remove_csrf_tag(text):
    """Remove csrf tag from TEXT
	因为 request 的 CSRF 和 从 django 使用类似 render 函数 load 的 CSRF 是不同的。
	其中 request 是独立的一个 HTTP 过程，是单元测试模拟用户 request，用户预期会看到的 response 内容。它经过 views 那边的 function 处理（比如 index function）。
	而测试直接使用类似 render 函数（比如 render_to_string() 函数）没有经过 index() function 的处理，（一般我们直接创建一些数据库内容，然后直接使用，不过在下面的 Example 中没有涉及到数据库而已），直接 load template 来渲染生成 HTML，
	将上述的 response 提取 HTML 部分，和不经过 HTTP（index function）的内部直接使用 render_to_string() 得到的 HTML 对比，就能得出 index function 工作是不是正常的（能不能成功渲染预期的页面内容）。
	但是正如上面所言，两个 HTML 是两次生成的，所以 CSRF 也会不同。因此 CSRF 在对比 HTML 时应该被排除掉。（还有一些空白符有潜在的可能性造成不一致，所以也通过 replace() 函数直接删除掉）。
	去除 HTML 中的 CSRF line 的 function：
    """
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)


class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')





