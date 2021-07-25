# ----- Import Libraries ----- #
from time import sleep

import twilio.rest
from selenium import webdriver
import os

# ----- Declare Variables ----- #
threshold_price = 3300
twilio_api_key = os.environ.get('twilio_key')
twilio_id = os.environ.get('twilio_id')
twilio_phone_num = os.environ.get('twilio_num')
my_phone = os.environ.get('my_phone')
first_run = True
# ----- Initialize Objects ----- #
# Web Driver Init
driver = webdriver.Chrome(executable_path='chromedriver.exe')
graphics_card = driver.get(
    url='https://www.amazon.com/ASUS-Graphics-DisplayPort-Axial-Tech-2-9-Slot/dp/B08J6GMWCQ/ref=dp_prsubs_2'
        '?pd_rd_i=B08J6GMWCQ&psc=1')

# Twilio Init
client = twilio.rest.Client(twilio_id, twilio_api_key)


# ----- Define Functions ----- #


def get_current_price():
    if not first_run:
        driver.refresh()
    return float(driver.find_element_by_id('priceblock_ourprice').text.replace('$', '').replace(',', ''))


def send_text():
    print('is below threshold')
    message = client.messages.create(body=f'The Price is below the threshold of {threshold_price} the price '
                                          f'is currently {current_price}',
                                     from_=twilio_phone_num,
                                     to=my_phone)


# ----- Code Meat ----- #
run = True
cooldown = 0
while run:
    sleep(5)
    print(cooldown)
    if cooldown < 1:
        current_price = get_current_price()
    if current_price < threshold_price and cooldown < 1:
        send_text()
        driver.find_element_by_id('submit.add-to-cart').click()
        sleep(3)
        driver.find_element_by_id('attachSiNoCoverage').click()
        cooldown = 36
    else:
        cooldown -= 1
    first_run = False
