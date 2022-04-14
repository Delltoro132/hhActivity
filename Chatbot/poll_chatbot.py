import telebot
import Configs.config as conf
import time
from telebot import types
from UserInfo.userinfo import *


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

url_page = "https://spb.hh.ru"
driver_path = "../Chromedriver/chromedriver.exe"

# options

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(useragent.ie)

driver = webdriver.Chrome(
    executable_path=driver_path,
    options=options)

# user_name = "89312805619"
# user_password = "AquaThor132"

bot = telebot.TeleBot(conf.TOKEN)


# Функция, обрабатывающая команду /start и /go
@bot.message_handler(commands=["start", "go"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton("Да")
    button_2 = types.KeyboardButton("Нет")
    markup.add(button_1)
    markup.add(button_2)
    msg = bot.send_message(message.chat.id,
                           'Привет. Я поднимаю резюме вверх на hh. Если хочешь приступить, скажи "Да".')
    bot.register_next_step_handler(msg, stet_1)


def stet_1(message):
    text = message.text
    if text.lower() != "да":
        msg = bot.send_message(message.chat.id, 'Если что, я тут...')
        bot.register_next_step_handler(msg, start)  # askSource
        return
    msg = bot.send_message(message.chat.id, 'Отлично, мне нужен твой мобильный номер телефона. Начни с 7 или 8')
    bot.register_next_step_handler(msg, stet_2)


def stet_2(message):
    text = message.text
    if len(text) != 11:
        msg = bot.send_message(message.chat.id, 'Цифр должно быть 10...')
        bot.register_next_step_handler(msg, stet_2)  # askSource
        return
    # user_name
    write_user_name(text)

    msg = bot.send_message(message.chat.id, 'Отлично, теперь мне нужен твой пароль')
    bot.register_next_step_handler(msg, stet_3)


def stet_3(message):
    text = message.text
    if len(text) <= 3:
        msg = bot.send_message(message.chat.id, 'Букв должно быть больше 3х...')
        bot.register_next_step_handler(msg, stet_3)  # askSource
        return
    # user_password
    write_user_password(text)
    print(info_list)

    bot.send_message(message.chat.id, 'Спасибо за ответы. Приступаю к работе.')
    start_program(message)


def start_program(message):

    while True:
        try:
            driver.get(url=url_page)

            # find and click on Enter
            bot.send_message(message.chat.id, "Захожу най сайт hh...")
            print("Захожу най сайт hh...")
            time.sleep(2)
            enter_button = driver.find_element(By.XPATH,
                                               "/html/body/div[7]/div[1]/div[2]/div/div[1]/div[1]/div/div[6]/a")
            enter_button.click()

            # find and clik on "Войти с паролем"
            time.sleep(3)
            more_form = driver.find_element(By.XPATH,
                                            "/html/body/div[7]/div[1]/div[3]/div/div/div/div/div/div/div[1]/div["
                                            "1]/div[1]/div[2]/div/div/form/div[4]/button[2]")
            more_form.click()

            # find and enter login
            bot.send_message(message.chat.id, "Ввожу данные...")
            print("Ввожу данные...")
            time.sleep(2)
            phone_input = driver.find_element(By.XPATH,
                                              "/html/body/div[7]/div[1]/div[3]/div/div/div/div/div/div/div[1]/div["
                                              "1]/div[1]/div[2]/div/form/div[1]/input")
            phone_input.send_keys(Keys.CONTROL + "a")
            phone_input.send_keys(Keys.ENTER)

            phone_input.send_keys(info_list["user_name"])

            # find and enter password
            time.sleep(2)
            password_input = driver.find_element(By.XPATH,
                                                 "/html/body/div[7]/div[1]/div[3]/div/div/div/div/div/div/div[1]/div["
                                                 "1]/div[1]/div[2]/div/form/div[2]/span/input")
            password_input.clear()
            password_input.send_keys(info_list["user_password"])

            # enter
            time.sleep(2)
            button_enter = driver.find_element(By.XPATH,
                                               "/html/body/div[7]/div[1]/div[3]/div/div/div/div/div/div/div[1]/div["
                                               "1]/div[1]/div[2]/div/form/div[4]/div/button[1]")
            button_enter.click()
            bot.send_message(message.chat.id, "Я залогинился!")
            print("Я залогинился!")

            # click on "Моё резюме"
            bot.send_message(message.chat.id, 'Захожу в раздел "Моё резюме"...')
            print('Захожу в раздел "Моё резюме"...')
            time.sleep(2)
            next_page = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div/div[1]/div[1]/a")
            next_page.click()

            # click on "Поднять в поиске"
            time.sleep(2)
            all_buttons = driver.find_elements(By.CLASS_NAME, "bloko-link")
            all_buttons_list = []

            for button in all_buttons:
                if button.text == "Поднять в поиске":
                    button.click()
                    bot.send_message(message.chat.id, "Я поднял резюме!")
                    print("Я поднял резюме!")
                    all_buttons_list.append(button.text)

            if "Поднять в поиске" not in all_buttons_list:
                bot.send_message(message.chat.id, "Кнопки не найдены попробуйте позже.")
                print("Кнопки не найдены попробуйте позже.")
                all_buttons_list.clear()

            # exit
            exit_button = driver.find_element(By.XPATH,
                                              "/html/body/div[6]/div[1]/div/div/div[1]/div[10]/div[1]/span/button/span")
            exit_button.click()
            time.sleep(2)

            exit_button = driver.find_element(By.XPATH, "/html/body/div[11]/div/div[2]/div[3]/form/input[1]")
            exit_button.click()

        except Exception as ex:
            print(ex)
        finally:
            bot.send_message(message.chat.id, "Я вышел!")
            info_list["session"] += 1
            bot.send_message(message.chat.id, f'Сессия {info_list["session"]} завершена! Повтор через 4 ч.')
            print(f'Сессия {info_list["session"]} завершена! Повтор через 2 ч.')

        time.sleep(14400)


# Запускаем бота

bot.polling(none_stop=True, interval=0)
