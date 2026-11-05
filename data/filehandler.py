import json
import os
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a
   kliens oldalon is jelezni kell.

'''

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    if not os.path.exists(JSON_FILE_PATH):
        return {"Users": [], "Baskets": []}
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Dict[str, Any]) -> None:
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_user(user: Dict[str, Any]) -> None:
    data = load_json()
    for u in data["Users"]:
        if u["id"] == user["id"]:
            raise ValueError(f"Ez a felhasználó azonosító már létezik: {user['id']}")
    data["Users"].append(user)
    save_json(data)

def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()
    for b in data["Baskets"]:
        if b["id"] == basket["id"]:
            raise ValueError(f"Ez a kosár azonosító már létezik: {basket['id']}")
        if b["user_id"] == basket["user_id"]:
            raise ValueError(f"Ehhez a felhasználóhoz már tartozik kosár: {basket['user_id']}")
    data["Baskets"].append(basket)
    save_json(data)

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> Dict[str, Any]:
    data = load_json()
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket["items"].append(item)
            save_json(data)
            return basket
    raise ValueError(f"Nem található kosár a felhasználóhoz: {user_id}")

def update_item_in_basket(user_id: int, item_id: int, updated_item: Dict[str, Any]) -> Dict[str, Any]:
    data = load_json()
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            for i, item in enumerate(basket["items"]):
                if item["item_id"] == item_id:
                    basket["items"][i] = updated_item
                    save_json(data)
                    return basket
            raise ValueError(f"Termék nem található a kosárban: {item_id}")
    raise ValueError(f"Nem található kosár a felhasználóhoz: {user_id}")

def delete_item_from_basket(user_id: int, item_id: int) -> Dict[str, Any]:
    data = load_json()
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            new_items = [i for i in basket["items"] if i["item_id"] != item_id]
            if len(new_items) == len(basket["items"]):
                raise ValueError(f"Termék nem található a kosárban: {item_id}")
            basket["items"] = new_items
            save_json(data)
            return basket
    raise ValueError(f"Nem található kosár a felhasználóhoz: {user_id}")
