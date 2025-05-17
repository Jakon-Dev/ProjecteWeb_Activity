import os
import django
import sys
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from behave import given, when, then
from django.contrib.auth.models import User
import uuid

# Configura Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

@given('I am on the register page')
def step_impl(context):
    context.browser.visit(context.get_url('/register/'))
    assert context.browser.is_text_present('Register', wait_time=5), "Register page not loaded"

@given('a user with username "{username}" already exists')
def step_impl(context, username):
    # Asegúrate de que el usuario existe
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password('betterhealth1')
        user.save()

@when('I enter registration details')
def step_impl(context):
    for row in context.table:
        username = row['username']
        email = row['email']
        password = row['password']
        password2 = row['password2']

        # Generar valores aleatorios si se usa newusertest
        if username == 'newusertest':
            uid = uuid.uuid4().hex[:8]
            username = f'user_{uid}'
            email = f'{uid}@example.com'
            password = f'Pass{uid}!'
            password2 = password  # asegurar coincidencia

            # Guardarlos en contexto para verificaciones posteriores si quieres
            context.generated_username = username
            context.generated_email = email
            context.generated_password = password

        # Borrar usuario si existía
        if User.objects.filter(username=username).exists():
            User.objects.get(username=username).delete()

        context.browser.fill('username', username)

        if context.browser.is_element_present_by_name('email'):
            context.browser.fill('email', email)

        context.browser.fill('password1', password)
        context.browser.fill('password2', password2)



@when('I click on the register button')
def step_impl(context):
    register_button = context.browser.find_by_tag('form').first.find_by_tag('button').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", register_button._element)
    time.sleep(0.5)

    try:
        register_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", register_button._element)
    
    time.sleep(1)

@then('I should be redirected to the login page')
def step_impl(context):
    assert 'login' in context.browser.url, f"Expected to be redirected to login page, got {context.browser.url}"

@then('I should see a registration success message')
def step_impl(context):
    assert context.browser.is_text_present('Registration successful', wait_time=5) or \
           context.browser.is_text_present('Your account has been created', wait_time=5), \
           "Success message not found"

@then('I should see an error message about existing username')
def step_impl(context):
    assert context.browser.is_text_present('A user with that username already exists', wait_time=5), \
           "Error message about existing username not found"

@then('I should remain on the register page')
def step_impl(context):
    assert 'register' in context.browser.url, f"Expected to remain on register page, got {context.browser.url}"

@then('I should see an error message about password mismatch')
def step_impl(context):
    error_divs = context.browser.find_by_css('.error-message')
    assert error_divs, "Error message about password mismatch not found"

