import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.url = "http://localhost:5000"
        self.driver.implicitly_wait(0.5)
        self.driver.get(self.url)


    def test_positiv(self):
        driver = self.driver
        elem = driver.find_element(By.NAME, "city")
        elem.send_keys("boston")
        button_elem = driver.find_element(By.NAME, "search_btn")
        button_elem.click()

    def test_negative(self):
        pass

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
