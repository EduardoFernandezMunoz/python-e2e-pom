import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )


@pytest.fixture
def browser_instance(request):
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecuta Chrome sin UI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)

    elif browser_name == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)

    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver