from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import datetime
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

ts = int(datetime.datetime.now().timestamp())  # timenow
SALUTATION = "Mr"
GIVEN_NAME = "Given Name"
MIDDLE_NAME = ""
SURNAME = "Surname"
DATE_OF_BIRTH = "11/06/1998"
NATIONALITY = "Turkey, Republic of"
EMAIL = "email@email.co"
PASSPORT_NUMBER = "123456"


browser = webdriver.Chrome(
    #  executable_path="./chromedriver",
    options=chrome_options,
)

browser.get(
    "https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm"
)

html = browser.find_element_by_tag_name("html")

category = browser.find_element_by_xpath('//*[@id="Category"]')
category = Select(category)
category.select_by_visible_text("All")

sub_category = browser.find_element_by_xpath('//*[@id="SubCategory"]')
sub_category = Select(sub_category)
sub_category.select_by_visible_text("All")

confirm_gnib = browser.find_element_by_xpath('//*[@id="ConfirmGNIB"]')
confirm_gnib = Select(confirm_gnib)
confirm_gnib.select_by_visible_text("No")

browser.execute_script(
    """
    try {
        let cookie1 = document.getElementById('cookiescript_injected');
        let cookie2 = document.getElementById('cookiescript_badge');
        cookie1.remove();
        cookie2.remove();
    } catch {
    }
"""
)

# cookies_close = browser.find_element_by_xpath('//*[@id="cookiescript_close"]')
# cookies_close.click()
