import json
import os
from typing import Dict, Any, List

'''
Útmutató a fájl használatához:

Felhasználó adatainak lekérdezése:

user_id = 1
user = get_user_by_id(user_id)
print(f"Felhasználó adatai: {user}")

Felhasználó kosarának tartalmának lekérdezése:

user_id = 1
basket = get_basket_by_user_id(user_id)
print(f"Felhasználó kosarának tartalma: {basket}")

Összes felhasználó lekérdezése:

users = get_all_users()
print(f"Összes felhasználó: {users}")

Felhasználó kosarában lévő termékek összárának lekérdezése:

user_id = 1
total_price = get_total_price_of_basket(user_id)
print(f"A felhasználó kosarának összára: {total_price}")

Hogyan futtasd?

Importáld a függvényeket a filehandler.py modulból:

from filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    if not os.path.exists(JSON_FILE_PATH):
        return {"Users": [], "Baskets": []}
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    data = load_json()
    for user in data.get("Users", []):
        if user.get("id") == user_id:
            return user
    raise ValueError(f"Felhasználó nem található: {user_id}")

def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    data = load_json()
    for basket in data.get("Baskets", []):
        if basket.get("user_id") == user_id:
            return basket.get("items", [])
    raise ValueError(f"Kosár nem található a felhasználóhoz: {user_id}")

def get_all_users() -> List[Dict[str, Any]]:
    data = load_json()
    return data.get("Users", [])

def get_total_price_of_basket(user_id: int) -> float:
    items = get_basket_by_user_id(user_id)
    total = sum(item.get("price", 0) * item.get("quantity", 0) for item in items)
    return round(total, 2)