import time
import logging

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import STAGE, PWD, USERNAME, PHONE, DJANGO_URL, TEST_IMMOWEB_CODE
from utils.utils import is_int, random_sleep


BACKEND_API_URL = DJANGO_URL + '/api-v1/'
IMMOWEB_ARTICLE_URL = 'https://www.immoweb.be/fr/annonce/'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

### Scrapper Utils ###


def get_driver(headless=False):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=1920,1080")
    if headless:
        chrome_options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=chrome_options)


def close_popup(driver):
    try:
        popup_button = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, "uc-btn-accept-banner"))
        )
        popup_button.click()
    except:
        logger.info("No popup to close")


def login(driver, mail, pwd):
    close_popup(driver)
    my_immo_button = driver.find_element_by_id('myImmowebMenu')
    my_immo_button.click()
    mail_input = driver.find_element_by_id('emailInput')
    pwd_input = driver.find_element_by_id('passwordInput')
    mail_input.send_keys(mail)
    pwd_input.send_keys(pwd)
    pwd_input.send_keys(Keys.RETURN)
    Keys.ENTER
    WebDriverWait(driver, 6).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[@href="https://www.immoweb.be/fr/deconnexion"]'))
    )


def get_next_page_button(driver):
    try:
        next_page_button = driver.find_element_by_class_name(
            'pagination__link--next')
    except:
        logger.info("Last page reached")
        return False
    return next_page_button


### API ###

def get_searches_urls():
    resp = requests.get(BACKEND_API_URL + 'searches')
    for search in resp.json():
        yield search.get('url')


def get_visited_immoweb_codes():
    resp = requests.get(BACKEND_API_URL + 'properties')
    return [property.get('immoweb_code') for property in resp.json()]


def get_to_do_prospections():
    resp = requests.get(BACKEND_API_URL + 'prospection_rules')
    return resp.json()


def get_candidates(driver, visited_codes):
    candidate_codes = []
    articles = driver.find_elements_by_tag_name('article')
    for article in articles:
        try:
            article.find_element_by_class_name('card__logo')
        except:
            id = article.get_attribute('id').split('_')
            if len(id) == 2 and is_int(id[1]):
                code = int(id[1])
                if code not in visited_codes:
                    candidate_codes.append(code)
    return candidate_codes


def visit_article(driver, code):
    driver.get(IMMOWEB_ARTICLE_URL + str(code))
    has_agency = False
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'customer-card'))
        )
        driver.find_element_by_class_name("customer-detail__name")
    except:
        has_agency = True

    payload = {
        'immoweb_code': code,
        'has_agency': has_agency
    }
    requests.post(BACKEND_API_URL + 'properties/', json=payload)
    random_sleep()


def execute_searches(driver):
    candidate_codes = []
    for url in get_searches_urls():
        visited_codes = get_visited_immoweb_codes()
        driver.get(url)
        close_popup(driver)
        while True:
            candidate_codes.extend(get_candidates(driver, visited_codes))
            next_page_button = get_next_page_button(driver)
            if next_page_button is False:
                break
            next_page_button.click()
            random_sleep(4, 6)  # TODO sleep is weak: use an explicit wait
    for candidate_code in candidate_codes:
        visit_article(driver, candidate_code)


def send_message(driver, property_code, message):
    driver.get(IMMOWEB_ARTICLE_URL + str(property_code))
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//textarea[@name="message"]'))
        )
    except:
        return False
    phone_input = driver.find_element_by_xpath(
        '//input[@name="phone"]')
    message_textarea = driver.find_element_by_xpath(
        '//textarea[@name="message"]')
    send_message_checkbox = driver.find_element_by_xpath(
        '//fieldset[@class="input-after-message"]//input')
    send_message_checkbox_label = driver.find_element_by_xpath(
        '//fieldset[@class="input-after-message"]//label')
    submit_button = driver.find_element_by_class_name('sendMyRequestButton')
    if not send_message_checkbox.is_selected():
        send_message_checkbox_label.click()

    message_textarea.clear()
    message_textarea.click()
    message_textarea.send_keys(message)
    phone_input.send_keys(PHONE)
    if STAGE == "prod" or (STAGE == "test" and TEST_IMMOWEB_CODE == property_code):
        random_sleep(1, 2)
        submit_button.submit()
    random_sleep()
    return True


def execute_prospection(driver):
    prospection_rules = get_to_do_prospections()
    for prospection_rule in prospection_rules:
        message = prospection_rule['message']
        properties = prospection_rule["properties"]
        for property in properties:
            status = send_message(driver, property, message)
            if status:
                payload = {
                    'property': property,
                    'rule': prospection_rule["id"]
                }
                requests.post(BACKEND_API_URL +
                              "prospection_logs/", json=payload)


def main():
    random_sleep(15, 20)
    driver = get_driver(headless=True)
    driver.get("https://www.immoweb.be/fr")
    if STAGE in ['prod', 'test']:
        login(driver, USERNAME, PWD)
    if STAGE in ['prod', 'dev']:
        execute_searches(driver)
        execute_prospection(driver)
    elif STAGE == 'test' and TEST_IMMOWEB_CODE:
        print("send message")
        send_message(driver, TEST_IMMOWEB_CODE,
                     'Hello, ceci est un test... Un peu de texte supplémentaire inutile.')
    driver.close()


if __name__ == '__main__':
    main()
