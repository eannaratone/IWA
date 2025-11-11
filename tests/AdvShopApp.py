# -*- coding: utf-8 -*-
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class AdvShopApp(unittest.TestCase):
    def setUp(self):
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

        # <<< PROXY FAST >>>
        fast_proxy = os.getenv("FAST_PROXY", "127.0.0.1:8087")
        opts.add_argument(f"--proxy-server={fast_proxy}")
        # FAST intercepta HTTPS; evitar fallos de certificado en headless:
        opts.add_argument("--ignore-certificate-errors")
        opts.add_argument("--allow-insecure-localhost")
        # (Opcional) reducir bloqueos por HSTS
        opts.add_argument("--disable-hsts")

        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(10)

        self.base_url = os.getenv("APP_URL", "https://advantageonlineshopping.com").rstrip("/")

    def test_smoke_homepage_title(self):
        d = self.driver
        d.get(self.base_url)
        self.assertIn("Advantage", d.title)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
