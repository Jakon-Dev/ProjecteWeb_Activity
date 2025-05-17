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

@when('I visit the homepage')
def step_impl(context):
    context.browser.visit(context.get_url('/'))
    time.sleep(1)
    assert context.browser.url.endswith('/'), f"Failed to load homepage, current URL is {context.browser.url}"

@then('I should see the homepage content')
def step_impl(context):
    # Verificar elementos típicos de la página de inicio
    assert context.browser.is_text_present('Welcome', wait_time=5) or \
           context.browser.is_text_present('Home', wait_time=5), "Homepage content not found"

@when('I go to the agents list page')
def step_impl(context):
    context.browser.visit(context.get_url('/agents/'))
    time.sleep(1)

    try:
        # Buscar el botón "See Agents"
        buttons = context.browser.links.find_by_text('See Agents')
        assert buttons, "No 'See Agents' links found on /agents/ page."
        context.browser.driver.execute_script("arguments[0].click();", buttons.first._element)
        time.sleep(1)
    except Exception as e:
        raise AssertionError(f"Failed to navigate to agents list: {str(e)}")

    assert '/agents/role/' in context.browser.url, f"Expected to navigate to agent list, got {context.browser.url}"

@then('I should see the agents list')
def step_impl(context):
    assert context.browser.is_element_present_by_css('.agent-card-container', wait_time=5), "No agent cards found"
