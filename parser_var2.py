'''ПАРСИНГ С BEAUTIFULSOUP'''

import requests
from bs4 import BeautifulSoup
import json

'''Настройки прокси 194.110.9.94:1080 
Если не работает, то заменяю, рабочим отсюда: https://hidemy.io/ru/proxy-list/countries/russian-federation/
'''
proxies = {
    "http": "http://194.110.9.94:1080",
    "https": "http://194.110.9.94:1080",
}

'''
URL страницы бренда
'''
url = "https://www.ozon.ru/brand/bushido-33728620/"

'''
Заголовки для обхода блокировки
'''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

'''
Получение HTML страницы
'''
response = requests.get(url, headers=headers, proxies=proxies)
response.raise_for_status()  # Проверка успешности запроса

'''
Парсинг HTML через BeautifulSoup
'''
soup = BeautifulSoup(response.content, "html.parser")

'''
Сбор данных о товарах.
Выводит по каждому товару: заголовок, цена, ссылка страницу товара.
'''
products = soup.find_all("div", class_="pe0")
items = []

for product in products:
    try:
        name = product.find("span", class_="a8b ba9 ac w8i_23").get_text(strip=True)
        price = product.find("span", class_="c306-a0").get_text(strip=True)
        link = product.find("a", href=True)["href"]
        full_link = f"https://www.ozon.ru{link}"
        items.append({"name": name, "price": price, "link": full_link})
    except Exception as e:
        print(f"Error: {e}")

'''
Сохранение данных в JSON файл.
'''
with open('bushido_products.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Данные сохранены в bushido_products.json")
