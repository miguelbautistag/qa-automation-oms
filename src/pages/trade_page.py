from playwright.sync_api import Page

class TradePage:
    def __init__(self, page: Page):
        self.page = page
        # Standards: Using get_by_role for accessibility-first testing
        self.asset_select = page.get_by_role("combobox", name="Select Asset")
        self.quantity_input = page.get_by_label("Quantity")
        self.buy_button = page.get_by_role("button", name="Place Buy Order")
        self.success_toast = page.get_by_role("alert")

    def navigate(self):
        self.page.goto("https://demo.ulitetrade.ai/market") # Placeholder URL

    def place_order(self, ticker: str, quantity: str):
        self.asset_select.select_option(ticker)
        self.quantity_input.fill(quantity)
        self.buy_button.click()