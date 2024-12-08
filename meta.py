import pytest
import playwright.sync_api
import re
import datetime
import definitions

def login(page, creds):
    page.goto(definitions.BASE_URL)
    page.locator('[placeholder="Username"]').fill(creds[0])
    page.locator('[placeholder="Password"]').fill(creds[1])
    page.locator('[data-cy="login-button"]').click()

def logout(page):
    page.goto(definitions.HOME_URL)
    page.locator('button:has-text("Logout")').first.click()

def open_form(page):
    page.get_by_text("Go to Form Page", exact = True).click()
    
def fill_form_and_submit(page, data):
    page.locator('[id="name"]').fill(data[0])
    page.locator('[id="email"]').fill(data[1])
    page.locator('[id="message"]').fill(data[2])
    page.get_by_text("Save Information", exact = True).click()

def go_to_button_interaction(page):
    page.get_by_text("Go to Button Interaction", exact = True).click()

def press_the_button(page):
    page.locator('button:has-text("Press Me")').click()

def getValidationMessage(page, locator):
    return page.locator(locator).evaluate("el => el.validationMessage")

def go_to_checkbox_interaction(page):
    page.get_by_text("Go to CheckBox Interaction", exact = True).click()

def click_the_checkbox(page):
    page.get_by_text("Toggle me", exact = True).click()
