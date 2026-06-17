"""
WeatherAPI - Консольное приложение для получения данных о погоде
Автор: GhoulFreeze
Версия: 1.0
Описание: Программа взаимодействует с OpenWeatherMap API и выводит текущую погоду
"""

import os
import json
import requests
from datetime import datetime

# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

# Инструкция по получению API-ключа:
# 1. Перейти на сайт https://openweathermap.org/api
# 2. Зарегистрироваться и получить бесплатный API-ключ
# 3. Вставить ключ ниже вместо "ваш_api_ключ"
API_KEY = "ваш_api_ключ"  # Заменить на действительный ключ

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"  # metric = Цельсии, imperial = Фаренгейты
LANG = "ru"       # Язык описания погоды

# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def clear_console():
    """
    Очищает экран консоли.
    Поддерживает Windows (nt) и Unix-подобные системы.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_header():
    """
    Выводит заголовок программы с визуальным оформлением.
    """
    print("=" * 60)
    print("      🌤️  WeatherAPI - Консольный метеоролог  🌧️")
    print("=" * 60)
    print()

def validate_api_key():
    """
    Проверяет, вставлен ли действительный API-ключ.
    
    Returns:
        bool: True, если ключ действительный, иначе False
    """
    if API_KEY == "ваш_api_ключ" or not API_KEY:
        print("\n⚠️  ОШИБКА: API-ключ не настроен!")
        print("Инструкция по получению ключа:")
        print("1. Перейдите на https://openweathermap.org/api")
        print("2. Зарегистрируйтесь и получите бесплатный ключ")
        print("3. Вставьте его в файл Weather.py в переменную API_KEY")
        print("\nПрограмма будет завершена.")
        return False
    return True

# ============================================================================
# ОСНОВНЫЕ ФУНКЦИИ
# ============================================================================

def get_weather(city_name):
    """
    Отправляет запрос к OpenWeatherMap API и получает данные о погоде.
    
    Аргументы:
        city_name (str): Название города на английском языке
    
    Возвращает:
        dict or None: Словарь с данными о погоде или None при ошибке
    
    Исключения:
        Обрабатываются все ошибки сети, HTTP и парсинга JSON
    """
    # Формируем параметры запроса согласно документации API
    params = {
        'q': city_name.strip(),
        'appid': API_KEY,
        'units': UNITS,
        'lang': LANG
    }
    
    try:
        # Выполняем GET-запрос к серверу
        print(f"⏳ Отправка запроса к OpenWeatherMap...")
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Проверяем статус HTTP-ответа (выбросит исключение при 4xx или 5xx)
        response.raise_for_status()
        
        # Парсим JSON-ответ
        weather_data = response.json()
        return weather_data
        
    except requests.exceptions.Timeout:
        print("\n❌ ОШИБКА: Превышено время ожидания ответа от сервера.")
        print("   Проверьте интернет-соединение и попробуйте снова.")
        return None
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ОШИБКА: Не удалось подключиться к серверу.")
        print("   Проверьте интернет-соединение.")
        return None
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("\n❌ ОШИБКА: Неверный API-ключ.")
            print("   Проверьте правильность ключа в файле Weather.py")
        elif response.status_code == 404:
            print(f"\n❌ ОШИБКА: Город '{city_name}' не найден.")
            print("   Убедитесь, что название введено на английском языке.")
        else:
            print(f"\n❌ HTTP ОШИБКА: {e}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ОШИБКА ЗАПРОСА: {e}")
        return None
        
    except json.JSONDecodeError:
        print("\n❌ ОШИБКА: Сервер вернул некорректные данные (не JSON).")
        return None

def display_weather(weather_data, city_name):
    """
    Извлекает нужные данные из ответа API и выводит их в структурированном виде.
    
    Аргументы:
        weather_data (dict): Словарь с данными от OpenWeatherMap
        city_name (str): Название города, введённое пользователем
    """
    if weather_data is None:
        return
    
    # Проверяем код ответа (в случае ошибки API возвращает cod != 200)
    if weather_data.get('cod') != 200:
        error_msg = weather_data.get('message', 'Неизвестная ошибка')
        print(f"\n❌ ОШИБКА API: {error_msg}")
        return
    
    # Извлекаем данные из JSON-структуры
    main_info = weather_data.get('main', {})
    wind_info = weather_data.get('wind', {})
    weather_list = weather_data.get('weather', [{}])
    weather_desc = weather_list[0].get('description', 'нет данных').capitalize()
    
    temp = main_info.get('temp')
    feels_like = main_info.get('feels_like')
    humidity = main_info.get('humidity')
    wind_speed = wind_info.get('speed')
    
    # Выводим информацию с форматированием
    print("\n" + "-" * 60)
    print(f"📍  ГОРОД: {city_name.upper()}")
    print("-" * 60)
    
    if temp is not None:
        print(f"🌡️  Температура:        {temp:.1f}°C")
    if feels_like is not None:
        print(f"🤔  Ощущается как:      {feels_like:.1f}°C")
    if humidity is not None:
        print(f"💧  Влажность:           {humidity}%")
    if wind_speed is not None:
        print(f"💨  Ветер:               {wind_speed:.1f} м/с")
    
    print(f"☁️  Описание:            {weather_desc}")
    print("-" * 60)
    
    # Дополнительная информация: время запроса
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"🕐  Данные получены:     {current_time}")
    print("-" * 60)

def get_user_city():
    """
    Запрашивает у пользователя название города и проверяет ввод.
    
    Возвращает:
        str: Название города или None, если ввод пустой
    """
    print("\n🌍  Введите название города (на английском языке):")
    print("   (Например: Moscow, London, Berlin, Tokyo)")
    
    city = input("> ").strip()
    
    if not city:
        print("\n❌ ОШИБКА: Название города не может быть пустым.")
        return None
    
    # Проверяем, что введены только буквы, пробелы и дефисы
    if not all(c.isalpha() or c.isspace() or c == '-' for c in city):
        print("\n⚠️  ВНИМАНИЕ: Название должно содержать только буквы.")
        print("   Попробуйте снова.")
        return None
    
    return city

# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ПРОГРАММЫ
# ============================================================================

def main():
    """
    Главная функция, управляющая работой программы.
    Реализует основной цикл: проверка API -> ввод города -> запрос -> вывод.
    """
    # Очищаем экран и выводим заголовок
    clear_console()
    print_header()
    
    # Шаг 1: Проверка API-ключа
    if not validate_api_key():
        input("\nНажмите Enter для выхода...")
        return
    
    # Шаг 2: Ввод города
    city = get_user_city()
    if city is None:
        input("\nНажмите Enter для выхода...")
        return
    
    # Шаг 3: Получение данных о погоде
    weather_data = get_weather(city)
    
    # Шаг 4: Вывод результата
    display_weather(weather_data, city)
    
    # Шаг 5: Завершение программы
    print("\n✨  Программа завершена. Спасибо за использование! ✨")
    input("\nНажмите Enter для выхода...")

# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

if __name__ == "__main__":
    main()
