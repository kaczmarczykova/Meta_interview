import pytest
import playwright.sync_api as pw
import re
import definitions
import meta
import time
import requests
import json

@pytest.mark.playwright
def test_1_login_functionality(page):

    # 1. Login with Valid Credentials
    meta.login(page, definitions.ENTITY_CREDS)
    pw.expect(page).to_have_url(definitions.HOME_URL)
    meta.logout(page)

    # 2. Login with Invalid Credentials
    meta.login(page, definitions.TESTING_CREDS_INVALID)
    assert page.get_by_text("Invalid credentials. Please try again.", exact = True).is_visible()

    # 3. Login with Missing Credentials
    meta.login(page, definitions.TESTING_CREDS_INCOMPLETE)
    msg = meta.getValidationMessage(page, definitions.LOCATOR_PASSWORD_MISSING)
    assert msg == "Please fill out this field."

    # 4.  Login with Valid Credentials API

def test_1_4_api():
    
    payload = json.dumps({
        "username": definitions.ENTITY_CREDS[0],
        "password": definitions.ENTITY_CREDS[1]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", definitions.URL_API, headers=headers, data=payload)
    token = response.json().get("token")
    
    assert response.status_code == 200
    assert token is not None and token != ""
    print(f"Odpověď: {response.json()}")


###############################################################3

def test_2_form_submission(page):

    # 1. Submit Form with Missing Data
    meta.login(page, definitions.ENTITY_CREDS)
    meta.open_form(page)
    meta.fill_form_and_submit(page, definitions.FORM_DATA_INCOMPLETE)
    msg = meta.getValidationMessage(page, definitions.LOCATOR_EMAIL_MISSING)
    assert msg == "Please fill out this field."
    
    # 2. Submit Form with Valid Data
    page.reload()
    meta.fill_form_and_submit(page, definitions.FORM_DATA)
    
    # check Name is saved correctly
    pw.expect(page.locator(definitions.SAVED_DATA)).to_contain_text(definitions.FORM_DATA[0])
    # check Email is saved correctly
    pw.expect(page.locator(definitions.SAVED_DATA)).to_contain_text(definitions.FORM_DATA[1])
    # check Message is saved correctly
    pw.expect(page.locator(definitions.SAVED_DATA)).to_contain_text(definitions.FORM_DATA[2])

###############################################################

def test_3_button_interaction(page):
    meta.login(page, definitions.ENTITY_CREDS)
    meta.go_to_button_interaction(page)
    pw.expect(page.locator(definitions.BUTTON_MESSAGE)).not_to_contain_text("Button has been pressed")
    meta.press_the_button(page)
    pw.expect(page.locator(definitions.BUTTON_MESSAGE)).to_contain_text("Button has been pressed")

###############################################################

def test_4_checkbox_toggling(page):
    meta.login(page, definitions.ENTITY_CREDS)
    meta.go_to_checkbox_interaction(page)
    meta.click_the_checkbox(page)
    pw.expect(page.get_by_text("The switch is ON!")).to_be_visible()

###############################################################

def test_5_additional_select_interaction(page):
    meta.login(page, definitions.ENTITY_CREDS)
    meta.go_to_select_interaction(page)
    meta.select_2nd_option(page)
    element = page.locator(definitions.SELECTED_OPTION)
    pw.expect(element).to_have_text("You selected: option2")

###############################################################

def test_6_additional_API_incorrect_login(page):
    payload = json.dumps({
        "username": definitions.TESTING_CREDS_INVALID[0],
        "password": definitions.TESTING_CREDS_INVALID[1]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", definitions.URL_API, headers=headers, data=payload)
    
    assert response.status_code == 401

def test_7_drag_and_drop(page):
    meta.login(page, definitions.ENTITY_CREDS)
    
    #Locate the elements that can be dragged and the drop target on the page.
    assert page.locator(definitions.ITEM_TO_DRAG).count() == 3

    #Verify that the draggable items are identified and can be moved.
    total_count = page.locator(definitions.ITEM_TO_DRAG).count()
    for i in range(0,total_count):
        pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(i)).to_have_attribute("draggable", "true")

    #Simulate dragging an item from the list or container.
    #Drop the item into a new target location
    source = page.get_by_text("Item 1")
    target = page.get_by_text("Item 2")
    source.drag_to(target)
    
    #Validate the Drag-and-Drop Functionality
    pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(0)).to_have_text("Item 2")
    pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(1)).to_have_text("Item 1")
    pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(2)).to_have_text("Item 3")

    #Edge Case Testing
    source = page.get_by_text("Item 1")
    target = page.get_by_text("Go to Form Page")
    source.drag_to(target)
    pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(0)).to_have_text("Item 2")
    pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(1)).to_have_text("Item 1")
    pw.expect(page.locator(definitions.ITEM_TO_DRAG).nth(2)).to_have_text("Item 3")