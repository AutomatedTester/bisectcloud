from selenium_base import BaseTestCase
from selenium.webdriver.common.by import By
SITE_ROOT = 'http://localhost:8000/'

class Home(BaseTestCase):
    fixtures = ['site.json']

    def test_can_add_a_job(self):
        self.driver.get(self.live_server_url)
        bad = self.driver.find_element(By.ID, "hg-bad")
        good = self.driver.find_element(By.ID, "hg-good")
        test = self.driver.find_element(By.ID, "test")
        submit = self.driver.find_element(By.ID, "submitbutton")

        bad.send_keys("asdfghk")
        good.send_keys("qweqweqwe")
        test.send_keys("foobar")
        submit.click()

        import time
        time.sleep(5)
        #if we don't have any tasks we haven't added anything
        tasks = self.driver.find_elements(By.CSS_SELECTOR, ".task")
        self.assertGreater(len(tasks), 0)
