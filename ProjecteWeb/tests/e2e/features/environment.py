import os
import sys
import django
from splinter import Browser
from django.test.runner import DiscoverRunner

# Configura entorno Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# ⬇️ Importamos tu función que carga datos desde la API
from scripts.fetch_data import un_official

def before_all(context):
    # Inicia navegador y entorno Django
    context.browser = Browser('chrome', headless=True)
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.test_db = context.test_runner.setup_databases()
    context.get_url = lambda path: f"http://localhost:8000{path}"

    # 🔄 Carga datos desde la API para los tests
    print("\n🔄 Importando datos desde la API para los tests...")
    un_official()
    print("✅ Datos importados correctamente.\n")

def after_all(context):
    context.browser.quit()
    context.test_runner.teardown_databases(context.test_db)
    context.test_runner.teardown_test_environment()
