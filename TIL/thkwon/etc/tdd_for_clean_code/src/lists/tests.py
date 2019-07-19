from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.template.loader import render_to_string

from .views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # HttpRequest 객체를 생성해서 사용자가 어떤 요청을 브라우저에 보내는지 확인한다.
        # 이것을 home_page 뷰에 전달해서 응답을 취득한다. 이 객체는 HttpResponse라는 클래스의 인스턴스이다.
        # 응답내용이 특정 속성을 가지고 있는지 확인한다.

        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

        # # html 의 값이 처음에 <html> , 나중에 </html>인지를 확인한다.
        # # 그 중간에, To-Do lists라는 텍스트가 있는지도 확인한다.
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>', response.content)
        # print(response.content)
        # self.assertTrue(response.content.endswith(b'</html>\n'))


class NewVisitorTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스는 멋진 작업목록 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다.
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀과 헤더가 'thkwon'를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your To-Do list', header_text)

        # 그녀는 바로 작업을 추가하기로 한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # "공작깃털 사기" 라고 텍스트 상자에 입력한다."
        # (에디스의 취미는 날치 잡이용 그물을 만드는 것이다.)
        inputbox.send_keys('공작 깃털 사기')

        # 엔터키를 치면 페이지가 갱신되고 작업 록록에
        # "1: 공작깃털 사기" 아이템이 추가된다.
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: 공작 깃털 사기' for row in rows),
        )

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        # 다시 "공작 깃털을 이용해서 그물 만들기" 라고 입력한다(에디스는 매우 체계적인 사람이다.)
        self.fail('Finish the test!')

        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다.
