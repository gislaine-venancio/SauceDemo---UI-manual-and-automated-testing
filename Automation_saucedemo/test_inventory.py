from playwright.sync_api import expect


class TestInventory:

    def test_product_list_is_displayed(self, logged_in_page):
        """TC - After login, the product list should be displayed."""
        items = logged_in_page.locator(".inventory_item")
        expect(items).to_have_count(6)

    def test_add_product_to_cart(self, logged_in_page):
        """TC - Adding a product should update the cart counter."""
        logged_in_page.click("#add-to-cart-sauce-labs-backpack")
        badge = logged_in_page.locator(".shopping_cart_badge")
        expect(badge).to_have_text("1")

    def test_remove_product_from_cart_on_listing_page(self, logged_in_page):
        """TC - Remove a product directly from the inventory page."""
        logged_in_page.click("#add-to-cart-sauce-labs-backpack")
        logged_in_page.click("#remove-sauce-labs-backpack")
        expect(logged_in_page.locator(".shopping_cart_badge")).to_have_count(0)

    def test_add_multiple_products(self, logged_in_page):
        """TC - Adding several products should correctly sum the cart counter."""
        logged_in_page.click("#add-to-cart-sauce-labs-backpack")
        logged_in_page.click("#add-to-cart-sauce-labs-bike-light")
        logged_in_page.click("#add-to-cart-sauce-labs-bolt-t-shirt")
        badge = logged_in_page.locator(".shopping_cart_badge")
        expect(badge).to_have_text("3")

    def test_sort_by_price_low_to_high(self, logged_in_page):
        """TC - 'Price (low to high)' sorting should list products in ascending order."""
        logged_in_page.select_option(".product_sort_container", "lohi")
        prices = logged_in_page.locator(".inventory_item_price").all_inner_texts()
        values = [float(p.replace("$", "")) for p in prices]
        assert values == sorted(values)

    def test_sort_by_price_high_to_low(self, logged_in_page):
        """TC - 'Price (high to low)' sorting should list products in descending order."""
        logged_in_page.select_option(".product_sort_container", "hilo")
        prices = logged_in_page.locator(".inventory_item_price").all_inner_texts()
        values = [float(p.replace("$", "")) for p in prices]
        assert values == sorted(values, reverse=True)

    def test_sort_by_name_a_to_z(self, logged_in_page):
        """TC - 'Name (A to Z)' sorting should list products in alphabetical order."""
        logged_in_page.select_option(".product_sort_container", "az")
        names = logged_in_page.locator(".inventory_item_name").all_inner_texts()
        assert names == sorted(names)

    def test_sort_by_name_z_to_a(self, logged_in_page):
        """TC - 'Name (Z to A)' sorting should list products in reverse alphabetical order."""
        logged_in_page.select_option(".product_sort_container", "za")
        names = logged_in_page.locator(".inventory_item_name").all_inner_texts()
        assert names == sorted(names, reverse=True)

    def test_open_product_detail_page(self, logged_in_page):
        """TC - Clicking a product name should open its detail page."""
        logged_in_page.click("text=Sauce Labs Backpack")
        logged_in_page.wait_for_url("**/inventory-item.html**")
        expect(logged_in_page.locator(".inventory_details_name")).to_be_visible()

    def test_back_from_detail_page(self, logged_in_page):
        """TC - The 'back to products' button should return to the listing page."""
        logged_in_page.click("text=Sauce Labs Backpack")
        logged_in_page.wait_for_url("**/inventory-item.html**")
        logged_in_page.click("#back-to-products")
        logged_in_page.wait_for_url("**/inventory.html")
        expect(logged_in_page.locator(".inventory_list")).to_be_visible()
