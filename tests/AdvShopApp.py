# -*- coding: utf-8 -*-
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

class AdvShopApp(unittest.TestCase):
    def setUp(self):
        # Chrome headless para CI (GitHub Actions)
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        # (Opcional) si tu red corporativa hace MITM en SSL:
        # opts.add_argument("--ignore-certificate-errors")

        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(10)

        # Toma la URL del entorno; fallback a la nueva app
        self.base_url = os.getenv("APP_URL", "https://advantageonlineshopping.com").rstrip("/")

        self.verificationErrors = []
        self.accept_next_alert = True

    def test_smoke_homepage_title(self):
        d = self.driver
        d.get(self.base_url)
        # Smoke assertion básica: el título contiene "Advantage"
        self.assertIn("Advantage", d.title)

        # (Opcional) Más validaciones poco frágiles:
        # Comprueba que hay al menos un link/categoría en la página
        # Esto evita depender de selectores muy específicos de Angular.
        links = d.find_elements(By.TAG_NAME, "a")
        self.assertTrue(len(links) > 0, "No se encontraron enlaces en la página principal")

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
        try:
            self.driver.quit()
        finally:
            # Mantén verificación de errores estilo unittest
            self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
