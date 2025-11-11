# -*- coding: utf-8 -*-
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # Chrome headless para CI
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(10)

        # Toma la URL de entorno (fallback a la tuya)
        self.base_url = os.getenv("APP_URL", "http://zero.webappsecurity.com").rstrip("/")
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        d = self.driver
        d.get(f"{self.base_url}/index.html")
        d.find_element(By.LINK_TEXT, "Zero Bank").click()
        d.find_element(By.XPATH, "//li[@id='onlineBankingMenu']/div/strong").click()
        d.get(f"{self.base_url}/online-banking.html")
        d.find_element(By.XPATH, "//li[@id='feedback']/div").click()
        d.get(f"{self.base_url}/feedback.html")
        d.find_element(By.LINK_TEXT, "Zero Bank").click()
        d.get(f"{self.base_url}/index.html")
        d.find_element(By.ID, "online-banking").click()
        d.get(f"{self.base_url}/online-banking.html")

    # Helpers actualizados a Selenium 4
    def is_element_present(self, how, what):
        try:
            self.driver.find_element(how, what)
            return True
        except NoSuchElementException:
            return False

    def is_alert_present(self):
        try:
            _ = self.driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # Cierra el navegador y valida errores
        try:
            self.driver.quit()
        finally:
            self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
