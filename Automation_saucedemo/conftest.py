import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com/"

USERS = {
    "standard": "standard_user",
    "locked_out": "locked_out_user",
    "problem": "problem_user",
    "performance_glitch": "performance_glitch_user",
    "error": "error_user",
    "visual": "visual_user",
}
PASSWORD = "secret_sauce"


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture()
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    context.close()


@pytest.fixture()
def logged_in_page(page):
    """Page already authenticated with standard_user, ready for the tests."""
    page.fill("#user-name", USERS["standard"])
    page.fill("#password", PASSWORD)
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    return page
