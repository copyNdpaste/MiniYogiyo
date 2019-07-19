"""
functional_test
"""
from selenium import webdriver
import unittest


class newVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트르 확인하러 간다.
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀과 헤더가 'To-D'를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

# 그녀는 바로 작업을 추가하기로 한다.

# "공작깃털 사기"라고 텍스트 상자에 입려갛ㄴ다.
# #(에디스의 취미는 날치 자비용ㅇ 그물을 만드는 것이다.)
#
# # 엔터키를 치면 페이지가 갱신되고 작업 ㅁ록록에
# # "1: 공작깃털 사기" 아이템이 추가된다.

# 추가 아이엩ㅁ을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
# 다시 "공작깃털을 이용해서 그물 만들기"라고 입력한다.
#
# # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다"
# 에디스는 사이특 ㅏ입력한 목록을 저장하고 있는지 궁금하다
# 사이트는 그녀를 위한 특정 URL을 생성해준다.
# 이떄 URL에 대한 설명도 함꼐 제공된다.

# 해당 URL에 접소갛면 그녀가 만든 작업 목록이 그대로 있는 것을 확인할 수 있다.
# 만족하고 잠자리에 든다.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
