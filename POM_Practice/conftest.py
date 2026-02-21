import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

@pytest.fixture
def browser_instance(request):
    browser_name = request.config.getoption("browser_name")

    if browser_name.lower() == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Headless moderno, más estable
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")  # Ventana grande para que todo sea clickeable
        driver = webdriver.Chrome(options=chrome_options)

    elif browser_name.lower() == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=firefox_options)

    # Tiempo de espera implícito
    driver.implicitly_wait(5)

    yield driver
