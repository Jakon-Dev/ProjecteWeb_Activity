import os
import django
import sys
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from behave import given, when, then
from django.contrib.auth.models import User

# Configura Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

@given('I am on the login page')
def step_impl(context):
    context.browser.visit(context.get_url('/login/'))
    assert context.browser.is_text_present('Login', wait_time=5), "Login page not loaded"

@when('I enter username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.fill('username', username)
    context.browser.fill('password', password)

@when('I click on the login button')
def step_impl(context):
    login_button = context.browser.find_by_tag('form').first.find_by_tag('button').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", login_button._element)
    time.sleep(0.5)

    try:
        login_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", login_button._element)
    
    time.sleep(1)

@then('I should be redirected to the homepage')
def step_impl(context):
    current_url = context.browser.url
    assert current_url.endswith('/'), f"Expected homepage URL, got {current_url}"

@then('I should see the "{text}" option')
def step_impl(context, text):
    assert context.browser.is_text_present(text, wait_time=5), f"Text '{text}' not found on page"

@then('I should see an error message')
def step_impl(context):
    assert context.browser.is_text_present('Invalid username or password', wait_time=5), "Error message not found"

@then('I should remain on the login page')
def step_impl(context):
    current_url = context.browser.url
    assert 'login' in current_url, f"Expected to remain on login page, got {current_url}"

@given('I am not logged in')
def step_impl(context):
    context.browser.visit(context.get_url('/'))  # ✅ visit en vez de get
    try:
        logout_link = context.browser.find_by_text('Log Out').first
        logout_link.click()
        time.sleep(1)
    except:
        pass  # Ya está deslogueado