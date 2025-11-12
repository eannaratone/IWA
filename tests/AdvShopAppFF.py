# -*- coding: utf-8 -*-
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class AdvShopAppFF(unittest.TestCase):
    def setUp(self):
        # Opciones Firefox para CI (headless)
        opts = FirefoxOptions()
        opts.headless = True

        # Proxy FAST (MITM). Lee FAST_PROXY del entorno (host:puerto)
        fast_proxy = os.getenv("FAST_PROXY", "127.0.0.1:8087")
        proxy_host, proxy_port = fast_proxy.split(":")
        proxy_port = int(proxy_port)

        # Configurar proxy para HTTP y HTTPS
        opts.set_preference("network.proxy.type", 1)  # 1=manual
        opts.set_preference("network.proxy.http", proxy_host)
        opts.set_preference("network.proxy.http_port", proxy_port)
        opts.set_preference("network.proxy.ssl", proxy_host)
        opts.set_preference("network.proxy.ssl_port", proxy_port)
        opts.set_preference("network.proxy.no_proxies_on", "")  # no bypass

        # Tolerar certificados MITM del FAST
        opts.set_preference("security.enterprise_roots.enabled", True)
        # Reduce bloqueos por HSTS estricta
        opts.set_preference("network.stricttransportsecurity.preloadlist", False)

        self.driver = webdriver.Firefox(options=opts)
        self.driver.implicitly_wait(10)

        # URL base por entorno; fallback a Advantage Online Shopping
        self.base_url = os.getenv("APP_URL", "https://advantageonlineshopping.com").rstrip("/")

    def test_smoke_homepage_title(self):
        d = self.driver
        d.get(self.base_url)
        # Smoke: título debe contener "Advantage"
        self.assertIn("Advantage", d.title)

        # (Opcional) valida que existan enlaces visibles
        links = d.find_elements(By.TAG_NAME, "a")
        self.assertTrue(len(links) > 0, "No se encontraron enlaces en la home")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
