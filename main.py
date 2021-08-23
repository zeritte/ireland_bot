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
