import pytest
from playwright.sync_api import expect
from conftest import USERS, PASSWORD


class TestLogin:

    def test_login_with_valid_credentials(self, page):
        """TC - Login with valid username and password should redirect to inventory."""
        page.fill("#user-name", USERS["standard"])
        page.fill("#password", PASSWORD)
        page.click("#login-button")
        page.wait_for_url("**/inventory.html")
        assert "inventory.html" in page.url
        expect(page.locator(".inventory_list")).to_be_visible()

    def test_login_locked_out_user(self, page):
        """TC - locked_out_user should display a lockout error message."""
        page.fill("#user-name", USERS["locked_out"])
        page.fill("#password", PASSWORD)
        page.click("#login-button")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "locked out" in error.inner_text().lower()

    def test_login_incorrect_password(self, page):
        """TC - Incorrect password should display an error message."""
        page.fill("#user-name", USERS["standard"])
        page.fill("#password", "wrong_password")
        page.click("#login-button")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "do not match" in error.inner_text().lower()

    def test_login_empty_username(self, page):
        """TC - Empty username field should display a required-field error."""
        page.fill("#password", PASSWORD)
        page.click("#login-button")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "username is required" in error.inner_text().lower()

    def test_login_empty_password(self, page):
        """TC - Empty password field should display a required-field error."""
        page.fill("#user-name", USERS["standard"])
        page.click("#login-button")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()
        assert "password is required" in error.inner_text().lower()

    def test_login_all_fields_empty(self, page):
        """TC - Both fields empty should display an error message."""
        page.click("#login-button")
        error = page.locator("[data-test='error']")
        expect(error).to_be_visible()

    def test_logout(self, logged_in_page):
        """TC - Logout should return to the login screen."""
        logged_in_page.click("#react-burger-menu-btn")
        # the side menu has a slide-in animation; wait for the link before clicking
        expect(logged_in_page.locator("#logout_sidebar_link")).to_be_visible()
        logged_in_page.click("#logout_sidebar_link")
        expect(logged_in_page.locator("#login-button")).to_be_visible()
