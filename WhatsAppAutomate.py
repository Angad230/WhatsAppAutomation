import sched
import time as time_module
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from time import sleep
from urllib.parse import quote
from sys import platform


def printmessage():
    options = webdriver.ChromeOptions();
    options.add_argument('--user-data-dir=./User_Data')
    driver = webdriver.Chrome(chrome_options=options)
    f = open("./inputs/message.txt", "r")
    message = f.read()
    f.close()
    print("*********************************************************")
    print('Your Input Message is: \n')
    print(message)
    message = quote(message)
    numbers = []
    f = open("./inputs/numbers.txt", "r")
    for line in f.read().splitlines():
        if line != "":
            numbers.append(line)
    f.close()
    total_number = len(numbers)
    print("**********************************************************")
    print('\nYou have entered ' + str(total_number) + ' numbers in the file')
    print()
    delay = 30
    driver.get('https://web.whatsapp.com')
    time_module.sleep(60)
    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            continue
        print('{}/{} => Sending message to {}.'.format((idx + 1), total_number, number))
        try:
            url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    try:
                        click_btn = WebDriverWait(driver, delay).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, '_1E0Oz')))
                    except Exception as e:
                        print(f"Something went wrong..\n Failed to send message to: {number}, retry ({i + 1}/3)")
                        print("Make sure your phone and computer is connected to the internet.")
                        print("If there is an alert, please dismiss it.")
                        input("Press enter to continue")
                    else:
                        sleep(1)
                        click_btn.click()
                        sent = True
                        sleep(3)
                        print('Message sent to: ' + number)
        except Exception as e:
            print('Failed to send message to ' + number + str(e))


def main():

    scheduler = sched.scheduler(time_module.time, time_module.sleep)
    # Change here date and time as per your requirements
    t = time_module.strptime('2021-06-29 18:29:00', '%Y-%m-%d %H:%M:%S')
    t = time_module.mktime(t)
    scheduler_e = scheduler.enterabs(t, 1, printmessage, ())
    scheduler.run()