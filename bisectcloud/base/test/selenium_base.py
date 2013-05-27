import os

from django.test import LiveServerTestCase
from selenium import webdriver


class BaseTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.environ['SAUCE_USERNAME']
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
            desired_capabilities['version'] = os.environ['SAUCE_BROWSER_VERSION']
            desired_capabilities['platform'] = os.environ['SAUCE_PLATFORM']
            desired_capabilities['name'] = 'Bisect in the cloud'

            cls.driver = webdriver.Remote(desired_capabilities=desired_capabilities,
                                          command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % \
                                          (os.environ['SAUCE_USERNAME'],
                                          os.environ['SAUCE_ACCESS_KEY'])
                                         )
        except Exception as e:
            print ("This following error was encounterd: %s" % e)
            cls.driver = webdriver.Firefox()
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.driver.quit()
