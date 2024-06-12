'''ПАРСИНГ С SELENIUM'''

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

'''
Настройки Selenium с использованием прокси 194.110.9.94:1080 
Если не работает, то заменяю, рабочим отсюда: https://hidemy.io/ru/proxy-list/countries/russian-federation/
'''
options = Options()
options.add_argument('--proxy-server=http://194.110.9.94:1080')
options.add_argument('--headless')  # Запуск браузера в фоновом режиме
options.add_argument('--disable-gpu')

'''
Инициализация драйвера.
'''
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.ozon.ru/brand/bushido-33728620/")

'''
Ожидание загрузки товаров на странице (10 сек).
Поиск по названию класса.
'''
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pe0')))

'''
Сбор данных о товарах.
'''
products = driver.find_elements(By.CLASS_NAME, 'pe0')

'''
Создание списка товаров - items.
Выводит по каждому товару: заголовок, цена, ссылка страницу товара.
'''
items = []
for product in products:
    try:
        name = product.find_element(By.CLASS_NAME, 'a8b ba9 ac w8i_23').text
        price = product.find_element(By.CLASS_NAME, 'c306-a0').text
        #link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        link = product.find_element(By.PARTIAL_LINK_TEXT, 'a8b ba9 ac w8i_23').get_attribute('href')
        items.append({"name": name, "price": price, "link": link})
    except Exception as e:
        print(f"Error: {e}")

'''
Закрытие драйвера.
'''
driver.quit()

'''
Сохранение данных в JSON файл.
'''
with open('bushido_products.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Данные сохранены в bushido_products.json")
