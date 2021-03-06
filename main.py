from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from time import sleep
import threading

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

SALUTATION = "Mr"
GIVEN_NAME = "Given Name"
MIDDLE_NAME = ""
SURNAME = "Surname"
DATE_OF_BIRTH = "11/06/1998"
NATIONALITY = "Turkey, Republic of"
EMAIL = "email@email.co"
PASSPORT_NUMBER = "123456"

available_threads = list(range(1, 11))
number_of_checks = 0


def reservation(thread_number):
    try:
        global number_of_checks
        global available_threads

        ts = int(datetime.datetime.now().timestamp())  # timenow
        browser = webdriver.Chrome(
            # ¬†executable_path="./chromedriver",
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

        declaration = browser.find_element_by_xpath('//*[@id="dvDeclareCheck"]')
        declaration.click()

        salutation = browser.find_element_by_xpath('//*[@id="Salutation"]')
        salutation = Select(salutation)
        salutation.select_by_visible_text(SALUTATION)

        given_name = browser.find_element_by_xpath('//*[@id="GivenName"]')
        given_name.send_keys(GIVEN_NAME)

        middle_name = browser.find_element_by_xpath('//*[@id="MidName"]')
        middle_name.send_keys(MIDDLE_NAME)

        surname = browser.find_element_by_xpath('//*[@id="SurName"]')
        surname.send_keys(SURNAME)

        browser.execute_script(
            """
        function getElementByXpath(path) {
        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
        getElementByXpath('//*[@id="DOB"]').removeAttribute('readonly');
        """
        )
        date_of_birth = browser.find_element_by_xpath('//*[@id="DOB"]')
        date_of_birth.send_keys(DATE_OF_BIRTH)

        nationality = browser.find_element_by_xpath('//*[@id="Nationality"]')
        nationality = Select(nationality)
        nationality.select_by_visible_text(NATIONALITY)

        email = browser.find_element_by_xpath('//*[@id="Email"]')
        email.send_keys(EMAIL)

        confirm_email = browser.find_element_by_xpath('//*[@id="EmailConfirm"]')
        confirm_email.send_keys(EMAIL)

        family_application = browser.find_element_by_xpath('//*[@id="FamAppYN"]')
        family_application = Select(family_application)
        family_application.select_by_visible_text("No")

        passport_travel_doc = browser.find_element_by_xpath('//*[@id="PPNoYN"]')
        passport_travel_doc = Select(passport_travel_doc)
        passport_travel_doc.select_by_visible_text("Yes")

        passport_number = browser.find_element_by_xpath('//*[@id="PPNo"]')
        passport_number.send_keys(PASSPORT_NUMBER)

        look_for_appointment_button = browser.find_element_by_xpath(
            '//*[@id="btLook4App"]'
        )
        look_for_appointment_button.click()

        appointment_type = browser.find_element_by_xpath('//*[@id="AppSelectChoice"]')
        appointment_type = Select(appointment_type)
        appointment_type.select_by_visible_text("closest to today")

        find_button = browser.find_element_by_xpath('//*[@id="btSrch4Apps"]')
        find_button.click()

        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btSrch4Apps"]'))
        ).click()

        source: str = browser.page_source

        if "No appointment" in source:
            print("Could not find any slot")
        else:
            print("Found slot")
            # body = browser.find_element_by_xpath('//*[@id="dvAppOptions"]')
            # body.screenshot(f"ss_{ts}.png")

        browser.save_screenshot(f"screenshots/ss_{ts}.png")
        f = open(f"htmls/html_{ts}.html", "w")
        f.write(source)
        f.close()

        # button = browser.find_element_by_xpath('//*[text()="Book This"]')

        number_of_checks += 1
        available_threads.append(thread_number)
        browser.quit()

    except Exception as e:
        print(f"Interrupted {str(e)}")


try:
    while True:
        if len(available_threads) > 0:
            print(f"Done {number_of_checks} checks.")
            thread_to_use = available_threads[0]
            th = threading.Thread(target=reservation, args=(thread_to_use,))
            th.start()
            available_threads.pop(0)
            print(f"{thread_to_use} is in use, left others {available_threads}")
            sleep(1)
except KeyboardInterrupt:
    print(f"Done {number_of_checks} checks.")
    print("Finished")
