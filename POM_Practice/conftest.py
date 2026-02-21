import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Browser selection: chrome or firefox"
    )

@pytest.fixture
def browser_instance(request):
    browser_name = request.config.getoption("browser_name").lower()

    if browser_name == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Modern headless mode, more stable
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")  # Large window so all elements are clickable
        driver = webdriver.Chrome(options=chrome_options)

    elif browser_name == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")  # Large window for clickable elements
        firefox_options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=firefox_options)

    # Set implicit wait for all elements
    driver.implicitly_wait(5)

    yield driver
