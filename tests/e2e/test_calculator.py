import pytest
import time
from multiprocessing import Process

from playwright.sync_api import sync_playwright
import uvicorn
from main import app

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")

@pytest.fixture(scope="module")
def server():
    proc = Process(target=run_server, daemon=True)
    proc.start()
    time.sleep(2)  # Wait for server to start
    yield
    proc.terminate()

def test_add_operation(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8001/")
        page.fill('input[id="a"]', "2")
        page.fill('input[id="b"]', "3")
        page.click('button[onclick="calculate(\'add\')"]')
        time.sleep(1)  # Wait for JS to execute
        result = page.inner_text("#result")
        assert "Result: 5" in result
        browser.close()

def test_divide_by_zero(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8001/")
        page.fill('input[id="a"]', "10")
        page.fill('input[id="b"]', "0")
        page.click('button[onclick="calculate(\'divide\')"]')
        time.sleep(1)
        result = page.inner_text("#result")
        assert "Error: Cannot divide by zero!" in result
        browser.close()