# Python E2E Test Automation Framework (Selenium + PyTest + POM)

## Overview
End-to-end (E2E) automation framework for a sample e-commerce application using Python, Selenium WebDriver, and PyTest, following the Page Object Model (POM) design pattern.  
Simulates user purchase flow: login, add to cart, checkout, and order confirmation. Focused on maintainability, scalability, and reliability.

## Architecture & Project Structure
- **Framework:** Page Object Model (POM), PyTest, JSON-based test data, WebDriverWait for synchronization  
- **Utilities:** Centralized WebDriver management and reusable page methods  
- **CI:** GitHub Actions automated execution  


### Project Structure
python-e2e-pom/
├── POM_Practice/
│   ├── data/
│   │   └── test_data.json
│   │
│   ├── pageObjects/
│   │   ├── login_page.py
│   │   ├── ecommerce_page.py
│   │   ├── cart.py
│   │   └── checkout_page.py
│   │
│   ├── reports/
│   │   └── report.html
│   │
│   ├── tests/
│   │   └── test_e2e_purchase.py
│   │
│   │
│   └── conftest.py
│
├── utils/
│   └── browserutils.py
│
├── .github/
│   └── workflows/
│       └── CI.yml                
│
├── README.md                    

## Features
- User login and authentication  
- Add product to cart and checkout process  
- Order overview and completion validation  
- HTML and JUnit XML test reports  

## Key Automation Practices
- Explicit waits to handle dynamic content and synchronization  
- JavaScript click/scroll to avoid click interception  
- Data-driven testing via JSON and PyTest parametrization  
- CI/CD integration via GitHub Actions