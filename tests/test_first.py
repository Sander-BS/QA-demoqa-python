from playwright.sync_api import Page, expect


def test_fill_form_smoke(page: Page):
    page.goto("https://demoqa.com/text-box")

    page.get_by_placeholder("Full Name").fill("Test User")

    page.get_by_role("button", name="Submit").click()

    expect(page.locator("#name")).to_contain_text("Test User")
