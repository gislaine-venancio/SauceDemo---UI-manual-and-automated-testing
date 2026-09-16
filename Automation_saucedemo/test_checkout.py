import pytest
from playwright.sync_api import expect


@pytest.fixture()
def page_with_product_in_checkout(logged_in_page):
    """Adds a product and navigates to the 'Your Information' checkout step."""
    logged_in_page.click("#add-to-cart-sauce-labs-backpack")
    logged_in_page.click(".shopping_cart_link")
    logged_in_page.wait_for_url("**/cart.html")
    logged_in_page.click("#checkout")
    return logged_in_page


class TestCheckout:

    def test_start_checkout(self, page_with_product_in_checkout):
        """TC - The Checkout button should open the information form."""
        page_with_product_in_checkout.wait_for_url("**/checkout-step-one.html")
        expect(page_with_product_in_checkout.locator("#first-name")).to_be_visible()

    def test_checkout_with_valid_data(self, page_with_product_in_checkout):
        """TC - Filling in valid data and continuing should reach the overview page."""
        page = page_with_product_in_checkout
        page.fill("#first-name", "John")
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        page.wait_for_url("**/checkout-step-two.html")
        expect(page.locator(".summary_info")).to_be_visible()

    def test_checkout_missing_first_name(self, page_with_product_in_checkout):
        """TC - Empty First Name field should display an error."""
        page = page_with_product_in_checkout
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "first name is required" in error.inner_text().lower()

    def test_checkout_missing_last_name(self, page_with_product_in_checkout):
        """TC - Empty Last Name field should display an error."""
        page = page_with_product_in_checkout
        page.fill("#first-name", "John")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "last name is required" in error.inner_text().lower()

    def test_checkout_missing_postal_code(self, page_with_product_in_checkout):
        """TC - Empty Postal Code field should display an error."""
        page = page_with_product_in_checkout
        page.fill("#first-name", "John")
        page.fill("#last-name", "Doe")
        page.click("#continue")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "postal code is required" in error.inner_text().lower()

    def test_cancel_checkout_step_one(self, page_with_product_in_checkout):
        """TC - Cancel on step 1 should return to the cart."""
        page = page_with_product_in_checkout
        page.click("#cancel")
        page.wait_for_url("**/cart.html")
        expect(page.locator(".cart_list")).to_be_visible()

    def test_complete_purchase_successfully(self, page_with_product_in_checkout):
        """TC - The full purchase flow should display a success message."""
        page = page_with_product_in_checkout
        page.fill("#first-name", "John")
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        page.wait_for_url("**/checkout-step-two.html")
        page.click("#finish")
        page.wait_for_url("**/checkout-complete.html")
        header = page.locator(".complete-header")
        expect(header).to_be_visible()
        assert "thank you" in header.inner_text().lower()

    def test_order_summary_values(self, page_with_product_in_checkout):
        """TC - Order total should equal item subtotal + tax (subtotal + tax = total)."""
        page = page_with_product_in_checkout
        page.fill("#first-name", "John")
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        page.wait_for_url("**/checkout-step-two.html")
        expect(page.locator(".summary_total_label")).to_be_visible()

        subtotal = float(page.inner_text(".summary_subtotal_label").split("$")[1])
        tax = float(page.inner_text(".summary_tax_label").split("$")[1])
        total = float(page.inner_text(".summary_total_label").split("$")[1])

        assert round(subtotal + tax, 2) == round(total, 2)

    def test_cancel_checkout_step_two(self, page_with_product_in_checkout):
        """TC - Cancel on step 2 (overview) should return to the product listing."""
        page = page_with_product_in_checkout
        page.fill("#first-name", "John")
        page.fill("#last-name", "Doe")
        page.fill("#postal-code", "12345")
        page.click("#continue")
        page.wait_for_url("**/checkout-step-two.html")
        page.click("#cancel")
        page.wait_for_url("**/inventory.html")
        expect(page.locator(".inventory_list")).to_be_visible()
