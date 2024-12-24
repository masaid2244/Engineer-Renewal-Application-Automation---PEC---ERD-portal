# Engineer Renewal Application Automation - Pakistan Engineer Council - Engineer Registration Portal

This project automates the process of renewing an engineer's registration through the **Pakistan Engineer Council Engineer Registration Portal** using **Python** and **Selenium**. The automation reduces the time and effort required for engineers to submit their renewal applications, ensuring the process is efficient and error-free.

## Key Features:
- **Automated Engineer Renewal Application**: Automates the process of filling out and submitting the renewal application form on the Pakistan Engineer Registration Portal.
- **Selenium WebDriver**: Utilizes Selenium WebDriver to simulate user interactions with the portal, including navigating pages, filling forms, and submitting data.
- **Page Object Model (POM)**: Implements the Page Object Model (POM) design pattern, organizing the code into reusable and maintainable components. Each webpage in the application is represented by a separate Python class, improving scalability and code readability.
- **Cross-browser Compatibility**: The automation script supports multiple browsers (e.g., Chrome, Firefox), making it flexible for different testing environments.

## Technologies Used:
- **Python**: The core language used for writing the automation scripts.
- **Selenium**: A web automation tool used to interact with the engineer registration portal and simulate real-user actions.
- **Page Object Model (POM)**: A design pattern used to maintain clean and scalable code for interaction with multiple web pages.
- **WebDriver**: Selenium’s WebDriver is used for driving the browser to automate tasks.

## Project Structure:
- **Page Objects**: Python classes under the `pages` directory represent different pages of the engineer renewal application portal (e.g., login page,upload detail page , cpd points upload etc).
- **Tests**: The `tests` directory contains the automation scripts that execute the renewal application process, simulating real-world user interaction.

## Setup & Installation:
1. Clone the repository: `git clone <repository_url>`
2. Install required Python dependencies: `pip install -r requirements.txt`
3. Set up the necessary WebDriver (ChromeDriver, GeckoDriver, etc.) as per the browser you plan to use.
4. Run the tests: `python -m unittest discover`
