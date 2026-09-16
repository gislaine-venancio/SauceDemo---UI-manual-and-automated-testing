from playwright.sync_api import expect


class TestCart:

    def test_go_to_cart(self, logged_in_page):
        """TC - The cart icon should navigate to the cart page."""
        logged_in_page.click("#add-to-cart-sauce-labs-backpack")
        logged_in_page.click(".shopping_cart_link")
        logged_in_page.wait_for_url("**/cart.html")
        expect(logged_in_page.locator(".cart_list")).to_be_visible()

    def test_product_appears_in_cart(self, logged_in_page):
        """TC - An added product should be listed in the cart."""
        logged_in_page.click("#add-to-cart-sauce-labs-backpack")
        logged_in_page.click(".shopping_cart_link")
        item = logged_in_page.locator(".cart_item")
        expect(item).to_have_count(1)
        expect(item).to_contain_text("Sauce Labs Backpack")

    def test_remove_product_from_cart_page(self, logged_in_page):
        """TC - Remove a product from within the cart page."""
        logged_in_page.click("#add-to-cart-sauce-labs-backpack")
        logged_in_page.click(".shopping_cart_link")
        logged_in_page.wait_for_url("**/cart.html")
        logged_in_page.click("#remove-sauce-labs-backpack")
        expect(logged_in_page.locator(".cart_item")).to_have_count(0)

    def test_empty_cart_shows_no_items(self, logged_in_page):
        """TC - The cart should be empty when no product has been added."""
        logged_in_page.click(".shopping_cart_link")
        logged_in_page.wait_for_url("**/cart.html")
        expect(logged_in_page.locator(".cart_item")).to_have_count(0)

    def test_continue_shopping(self, logged_in_page):
        """TC - The 'Continue Shopping' button should return to the product listing."""
        logged_in_page.click(".shopping_cart_link")
        logged_in_page.wait_for_url("**/cart.html")
        logged_in_page.click("#continue-shopping")
        logged_in_page.wait_for_url("**/inventory.html")
        expect(logged_in_page.locator(".inventory_list")).to_be_visible()
