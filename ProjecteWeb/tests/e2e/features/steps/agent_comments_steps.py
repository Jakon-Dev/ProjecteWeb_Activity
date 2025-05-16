import os
import django
import sys
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from behave import given, when, then
from django.contrib.auth.models import User as AuthUser
from web.models import Agent, AgentComment
from splinter.exceptions import ElementDoesNotExist

# Configura Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# ID real de Phoenix desde la API
PHOENIX_ID = "eb93336a-449b-9c1b-0a54-a891f7921d69"

@given('I am logged in as "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.username = username
    context.password = password

    user, _ = AuthUser.objects.get_or_create(username=username)
    user.set_password(password)
    user.save()
    context.user = user

    context.browser.visit(context.get_url('/login/'))
    context.browser.fill('username', username)
    context.browser.fill('password', password)

    login_button = context.browser.find_by_tag('form').first.find_by_tag('button').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", login_button._element)
    time.sleep(0.5)

    try:
        login_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", login_button._element)

    assert context.browser.is_text_present("Log Out", wait_time=5), "Login failed"
    time.sleep(1)

@given('I go to the agent detail page for agent with name "{agent_name}"')
def step_impl(context, agent_name):
    time.sleep(1)
    agent = Agent.objects.get(name=agent_name)
    context.agent = agent
    context.browser.visit(context.get_url(f'/agents/detail/{agent.id}/'))

@when('I submit a new comment "{comment}"')
def step_impl(context, comment):
    assert context.browser.is_element_present_by_name('comment', wait_time=5), "Comment textarea not found"
    context.browser.fill('comment', comment)
    assert context.browser.is_element_present_by_value('Send Comment', wait_time=5), "Send Comment button not found"
    button = context.browser.find_by_value('Send Comment').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", button._element)
    time.sleep(0.5)
    try:
        button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", button._element)


@then('I should see the comment "{comment}"')
def step_impl(context, comment):
    assert context.browser.is_text_present(comment, wait_time=5), f"Comment '{comment}' not found"

@given('I have previously added the comment "{comment}"')
def step_impl(context, comment):
    user = context.user
    agent = Agent.objects.get(id=PHOENIX_ID)
    context.agent = agent
    AgentComment.objects.create(agent=agent, user=user, comment=comment)

@when('I edit the comment to "{new_comment}"')
def step_impl(context, new_comment):
    context.browser.visit(context.get_url(f'/agents/detail/{context.agent.id}/'))
    assert context.browser.is_element_present_by_css('.fa-edit', wait_time=5), "Edit icon not found"
    edit_button = context.browser.find_by_css('.fa-edit').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", edit_button._element)
    time.sleep(0.5)
    try:
        edit_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", edit_button._element)

    assert context.browser.is_element_present_by_name('comment', wait_time=5), "Comment edit textarea not found"
    context.browser.fill('comment', new_comment)
    assert context.browser.is_element_present_by_value('Guardar cambios', wait_time=5), "Save button not found"
    save_button = context.browser.find_by_value('Guardar cambios').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", save_button._element)
    time.sleep(0.5)
    try:
        save_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", save_button._element)


@when('I delete the comment')
def step_impl(context):
    context.browser.visit(context.get_url(f'/agents/detail/{context.agent.id}/'))
    assert context.browser.is_element_present_by_css('.fa-trash-alt', wait_time=5), "Delete icon not found"
    trash_button = context.browser.find_by_css('.fa-trash-alt').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", trash_button._element)
    time.sleep(0.5)
    try:
        trash_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", trash_button._element)

    assert context.browser.is_element_present_by_value('Delete', wait_time=5), "Delete confirmation button not found"
    # Forzar cierre del modal-backdrop si está presente (lo que tapa el botón)
    context.browser.driver.execute_script("""
        const backdrop = document.querySelector('.modal-backdrop.fade.show');
        if (backdrop) backdrop.remove();
    """)

    delete_button = context.browser.find_by_value('Delete').first
    context.browser.driver.execute_script("arguments[0].scrollIntoView(true);", delete_button._element)
    time.sleep(0.5)
    try:
        delete_button.click()
    except ElementClickInterceptedException:
        context.browser.driver.execute_script("arguments[0].click();", delete_button._element)


@then('I should not see the comment "{comment}"')
def step_impl(context, comment):
    assert not context.browser.is_text_present(comment, wait_time=5), f"Comment '{comment}' still present"
