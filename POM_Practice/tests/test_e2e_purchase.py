import json
import os
import pytest
from POM_Practice.pageObjects.login import LoginPage


# Get the current directory of this test file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the JSON test data file
test_data_path = os.path.join(current_dir, '..', 'data', 'test_e2e_purchase.json')

# Open and read the JSON file, loading the "data" array into test_list
with open(test_data_path, 'r', encoding='utf-8') as file:
    test_data = json.load(file)
    test_list = test_data["data"]


# Parametrize the test to run once for each item in test_list
@pytest.mark.parametrize("test_list_item", test_list)
def test_e2e_purchase (browser_instance, test_list_item):
    driver = browser_instance                               # The WebDriver instance injected by a fixture

    # Navigate to the login page
    loginPage = LoginPage(driver)
    driver.get("https://practice.qabrains.com/ecommerce/login")

    # Log in and receive the EcommercePage object
    ecommerce_page = loginPage.login(test_list_item["userEmail"], test_list_item["userPassword"])

    # Add the selected product to the cart
    ecommerce_page.add_product_to_cart(test_list_item["productName"])

    # Navigate to the cart page
    cart_page = ecommerce_page.go_to_cart()

    # Go to the checkout info page
    checkout_info_page = cart_page.go_to_checkout()

    # Fill in the user information
    checkout_info_page.fill_out_info(test_list_item["firstName"],test_list_item["lastName"],test_list_item["zipCode"])

    # Continue to the overview page
    checkout_overview_page = checkout_info_page.continue_to_payment()

    # Verify that the correct product appears in the overview
    checkout_overview_page.checkout_overview(test_list_item["productName"])

    # Finish the order and move to the final page
    checkout_complete_page = checkout_overview_page.finish_order()

    # Verify the order confirmation and close the browser
    checkout_complete_page.order_assertion()
