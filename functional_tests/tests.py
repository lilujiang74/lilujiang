from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import  unittest
MAX_WAIT=10
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def wait_for_row_in_list_tablb(self,row_text):
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn(row_text, [row.text for row in rows])
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except(AssertionError,WebDriverException)as e:
                if time.time() - start_time > MAX_WAIT:
                    raise  e
                time.sleep(0.5)
    def test_can_start_a_list_for_one_user(self):
        #edith has heard about a cool new online to-do app.she goes
        #to check out its homepage
        self.browser.get(self.live_server_url)

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text=self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)

        #She is invited to enter a to-do item straight away
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #she types "Buy peacock feathers" into a text box (Edith's hobby
        #is tying fiy-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tablb('1: Buy peacock feathers')
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tablb('1: Buy peacock feathers')
        self.wait_for_row_in_list_tablb('2: Use peacock feathers to make a fly')

        table=self.browser.find_element_by_id("id_list_table")
        rows=table.find_elements_by_tag_name("tr")
        self.assertIn('1: Buy peacock feathers',[row.text for row in rows]
        )
        self.assertIn(
            '2: Use peacock feathers to make a fly',
            [row.text for row in rows]
        )
        self.assertTrue(
            any(row.text=="1: Buy peacock feathers" for row in rows),
            f"New to-do item did not appear in table. Contents were:\n{table.text}"
        )
        #There is still a text box inviting her to add another item. She
        #enters "Use peacock feathers to make a fly"(Edith is very
        #methodical)
    def test_multiple_users_can_start_lists_at_different_urls(self):
        #The page updates again, and now shows both items on her list
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tablb('1: Buy peacock feathers')
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        self.browser.quit()
        self.browser=webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tablb('1: Buy milk')

        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        self.wait_for_row_in_list_tablb('1: testing')
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tablb('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
