import pytest
import playwright.sync_api as pw
import re
import definitions
import meta
import time
import requests

@pytest.mark.playwright
def test_1_login_functionality(page):

    # 1. Login with Valid Credentials
    meta.login(page, definitions.ENTITY_CREDS)
    #page.evaluate("document.body.style.zoom = '0.33'")
    pw.expect(page).to_have_url(definitions.HOME_URL)
    meta.logout(page)

    # 2. Login with Invalid Credentials
    meta.login(page, definitions.TESTING_CREDS_INVALID)
    assert page.get_by_text("Invalid credentials. Please try again.", exact = True).is_visible()

    # 3. Login with Missing Credentials
    meta.login(page, definitions.TESTING_CREDS_INCOMPLETE)
    msg = meta.getValidationMessage(page, definitions.LOCATOR_PASSWORD_MISSING)
    assert page.locator(definitions.LOCATOR_PASSWORD_MISSING).is_visible()

    # 4.  Login with Valid Credentials API

def test_api_login():
    url = "http://localhost:8000/login"
    payload = {
        "username": "admin",
        "password": "admin321"
    }
    response = requests.post(url, payload)

    assert response.status_code == 200
    print(f"Odpověď: {response.json()}")


###############################################################3

def test_2_1_form_submission(page):

    # 1. Submit Form with Missing Data
    meta.login(page, definitions.ENTITY_CREDS)
    #page.evaluate("document.body.style.zoom = '0.33'")
    meta.open_form(page)
    meta.fill_form_and_submit(page, definitions.FORM_DATA_INCOMPLETE)
    MSG = meta.getValidationMessage(page, definitions.LOCATOR_EMAIL_MISSING)
    #pw.expect(definitions.LOCATOR_EMAIL_MISSING).to_have_text("Vyplňte prosím toto pole.")
    assert page.locator(definitions.LOCATOR_EMAIL_MISSING).is_visible()

def test_2_2_form_submission(page):
    # 2. Submit Form with Valid Data

    meta.login(page, definitions.ENTITY_CREDS)
    page.evaluate("document.body.style.zoom = '0.33'")
    meta.open_form(page)

    #page.reload()
    meta.fill_form_and_submit(page, definitions.FORM_DATA)
    saved_data = page.locator('[id="root"]')
   

    #saved_data = page.locator('.saved-item p:has(strong:has-text("Name:"))')
    #saved_data = page.locator('[class="class-name"]')
    pw.expect(page.locator('//div[@id="root"]')).to_contain_text("my name")
    
    
    
    # check Name is saved correctly
    pw.expect(saved_data).to_contain_text(definitions.FORM_DATA[0])
    # check Email is saved correctly
    #pw.expect(saved_data).to_have_text(definitions.FORM_DATA[1])
    # check Message is saved correctly
    #pw.expect(saved_data).to_have_text(definitions.FORM_DATA[2])

###############################################################

def test_3_button_interaction(page):
    meta.login(page, definitions.ENTITY_CREDS)
    meta.go_to_button_interaction(page)
    pw.expect(page.locator('//div[@id="root"]')).not_to_have_text("Button has been pressed.")
    meta.press_the_button(page)
    pw.expect(page.locator('//div[@id="root"]')).to_have_text("Button has been pressed")

###############################################################

def test_4_checkbox_toggling(page):
    meta.login(page, definitions.ENTITY_CREDS)
    meta.go_to_checkbox_interaction(page)
    meta.click_the_checkbox(page)
    pw.expect(page.get_by_text("The switch is ON!")).to_be_visible()

