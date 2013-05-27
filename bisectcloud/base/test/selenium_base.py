import os

from django.test import LiveServerTestCase
from selenium import webdriver


class BaseTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.username = os.environ['SAUCE_USERNAME']
            cls.key = os.environ['SAUCE_ACCESS_KEY']
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
            desired_capabilities['version'] = os.environ['SAUCE_BROWSER_VERSION']
            desired_capabilities['platform'] = os.environ['SAUCE_PLATFORM']
            desired_capabilities['name'] = 'Bisect in the cloud'
            desired_capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            desired_capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            desired_capabilities['tags'] = [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']
            hub_url = "%s:%s@localhost:4445" % (cls.username, cls.key)

            cls.driver = webdriver.Remote(desired_capabilities=desired_capabilities,
                                          command_executor="http://%s/wd/hub" % hub_url)
        except Exception as e:
            print ("This following error was encounterd: %s" % e)
            cls.driver = webdriver.Firefox()
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.driver.quit()
