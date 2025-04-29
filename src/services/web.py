from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page
import logging

logger = logging.getLogger(__name__)

class WebAutomation:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()

    async def navigate(self, url: str) -> None:
        """
        Navigue vers une URL spécifique.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.goto(url)

    async def click(self, selector: str) -> None:
        """
        Clique sur un élément spécifié par son sélecteur.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.click(selector)

    async def fill(self, selector: str, value: str) -> None:
        """
        Remplit un champ spécifié par son sélecteur.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.fill(selector, value)

    async def submit(self, selector: str) -> None:
        """
        Soumet un formulaire spécifié par son sélecteur.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.press(selector, "Enter")

    async def get_text(self, selector: str) -> str:
        """
        Récupère le texte d'un élément spécifié par son sélecteur.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        return await self.page.text_content(selector)

    async def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        """
        Attend qu'un élément spécifié par son sélecteur soit visible.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def execute_script(self, script: str) -> Any:
        """
        Exécute un script JavaScript dans la page.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        return await self.page.evaluate(script)

    async def take_screenshot(self, path: str) -> None:
        """
        Prend une capture d'écran de la page.
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")
        await self.page.screenshot(path=path)

    async def close(self) -> None:
        """
        Ferme le navigateur.
        """
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None 