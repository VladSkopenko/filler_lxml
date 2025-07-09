import requests
import json
import os
from typing import Optional

# Варианты упаковки
PACKAGING_TYPES = {
    'IN_BULK': 'in bulk',
    'BIG_BAGS': 'big bags',
    'BIG_BAGS_INSIDE_CONTAINER': 'big bags inside container'
}

# DeepL API конфигурация
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')  # Получаем ключ из переменной среды

def translate_with_deepl(text: str, target_lang: str) -> Optional[str]:
    """
    Переводит текст через DeepL API
    
    Args:
        text: Текст для перевода
        target_lang: Целевой язык ('RU' для русского, 'UK' для украинского)
    
    Returns:
        Переведенный текст или None в случае ошибки
    """
    if not DEEPL_API_KEY:
        print("❌ Ошибка: Не найден DEEPL_API_KEY в переменных среды")
        print("Установите переменную: export DEEPL_API_KEY='ваш_ключ'")
        return None
    
    headers = {
        'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'text': text,
        'target_lang': target_lang,
        'source_lang': 'EN'
    }
    
    try:
        response = requests.post(DEEPL_API_URL, headers=headers, data=data)
        response.raise_for_status()
        
        result = response.json()
        if 'translations' in result and len(result['translations']) > 0:
            return result['translations'][0]['text']
        else:
            print(f"❌ Ошибка API: {result}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка JSON: {e}")
        return None

def generate_descriptions():
    """
    Генерирует описания на английском, русском и украинском через DeepL
    """
    descriptions = {}
    
    for packaging_type, packaging_name in PACKAGING_TYPES.items():
        # Английский оригинал
        eng_description = f"Ukrainian corn {packaging_name}, 2025 production year (hereinafter 'Goods')"
        
        # Русский перевод через DeepL
        ru_description = translate_with_deepl(eng_description, 'RU')
        
        # Украинский перевод через DeepL
        uk_description = translate_with_deepl(eng_description, 'UK')
        
        descriptions[packaging_type] = {
            'english': eng_description,
            'russian': ru_description,
            'ukrainian': uk_description
        }
    
    return descriptions

def print_descriptions():
    """
    Выводит все варианты описаний
    """
    descriptions = generate_descriptions()
    
    print("=" * 80)
    print("ОПИСАНИЯ ТОВАРА ДЛЯ РАЗНЫХ ВИДОВ УПАКОВКИ")
    print("=" * 80)
    
    for packaging_type, translations in descriptions.items():
        print(f"\n📦 Упаковка: {packaging_type}")
        print(f"   ({PACKAGING_TYPES[packaging_type]})")
        print("-" * 60)
        print(f"🇺🇸 English: {translations['english']}")
        print(f"🇷🇺 Russian: {translations['russian']}")
        print(f"🇺🇦 Ukrainian: {translations['ukrainian']}")
        print()

def get_description_for_packaging(packaging_type, language='english'):
    """
    Получить описание для конкретного типа упаковки и языка
    
    Args:
        packaging_type: IN_BULK, BIG_BAGS, или BIG_BAGS_INSIDE_CONTAINER
        language: 'english', 'russian', или 'ukrainian'
    
    Returns:
        str: Описание на указанном языке
    """
    descriptions = generate_descriptions()
    
    if packaging_type not in descriptions:
        raise ValueError(f"Неизвестный тип упаковки: {packaging_type}")
    
    if language not in descriptions[packaging_type]:
        raise ValueError(f"Неизвестный язык: {language}")
    
    return descriptions[packaging_type][language]

# Пример использования
if __name__ == "__main__":
    print_descriptions()
    
    print("\n" + "=" * 80)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ")
    print("=" * 80)
    
    # Пример для конкретного типа упаковки
    try:
        description_ru = get_description_for_packaging('BIG_BAGS', 'russian')
        print(f"Описание BIG_BAGS на русском: {description_ru}")
        
        description_uk = get_description_for_packaging('IN_BULK', 'ukrainian')
        print(f"Описание IN_BULK на украинском: {description_uk}")
        
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "=" * 80)
    print("НАСТРОЙКА DEEPL API")
    print("=" * 80)
    print("""
1. Зарегистрируйтесь на https://www.deepl.com/pro-api
2. Получите бесплатный API ключ (500,000 символов в месяц)
3. Установите переменную среды:
   
   Windows (PowerShell):
   $env:DEEPL_API_KEY="ваш_ключ_здесь"
   
   Windows (CMD):
   set DEEPL_API_KEY=ваш_ключ_здесь
   
   Linux/Mac:
   export DEEPL_API_KEY="ваш_ключ_здесь"
4. Запустите скрипт: python translate_description.py
    """)
    
    print("\n" + "=" * 80)
    print("КОД ДЛЯ ИНТЕГРАЦИИ")
    print("=" * 80)
    print("""
# Пример использования в вашем коде:
from translate_description import get_description_for_packaging

# Получить описание для BIG_BAGS на русском
description = get_description_for_packaging('BIG_BAGS', 'russian')

# Или для интеграции с вашим классом business:
def get_goods_description(business):
    return get_description_for_packaging(business.packaging_type, 'russian')
    """) 