from selenium_base import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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

        wait = WebDriverWait(self.driver, 5)
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".task")) == 2)

        self.assertEqual('', bad.get_attribute('value'))
        self.assertEqual('', good.get_attribute('value'))
        self.assertEqual('', test.get_attribute('value'))
