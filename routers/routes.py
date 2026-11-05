from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter, status
from data.filehandler import add_user, add_basket, add_item_to_basket, save_json, update_item_in_basket, delete_item_from_basket
from data.filereader import get_user_by_id, get_basket_by_user_id, get_all_users, get_total_price_of_basket, load_json
import os
import shutil
from typing import List

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User):
    try:
        add_user(user.model_dump())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    try:
        get_user_by_id(userid)

        data = load_json()
        max_id = 100
        if data["Baskets"]:
            max_id = max(b["id"] for b in data["Baskets"])

        new_basket = {
            "id": max_id + 1,
            "user_id": userid,
            "items": []
        }
        add_basket(new_basket)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Sikeres kosár hozzárendelés.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item):
    try:
        basket = add_item_to_basket(userid, item.model_dump())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=basket)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@routers.put('/updateitem', response_model=Basket)
def updateitem(userid: int, itemid: int, updateItem: Item):
    try:
        item_data = updateItem.model_dump()
        item_data['item_id'] = itemid
        basket = update_item_in_basket(userid, itemid, item_data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=basket)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@routers.delete('/deleteitem', response_model=Basket)
def deleteitem(userid: int, itemid: int):
    try:
        basket = delete_item_from_basket(userid, itemid)
        return JSONResponse(status_code=status.HTTP_200_OK, content=basket)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@routers.get('/user', response_model=User)
def user(userid: int):
    try:
        user_data = get_user_by_id(userid)
        return JSONResponse(status_code=status.HTTP_200_OK, content=user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@routers.get('/users', response_model=List[User])
def users():
    try:
        users_list = get_all_users()
        return JSONResponse(status_code=status.HTTP_200_OK, content=users_list)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@routers.get('/shoppingbag', response_model=List[Item])
def shoppingbag(userid: int):
    try:
        items = get_basket_by_user_id(userid)
        return JSONResponse(status_code=status.HTTP_200_OK, content=items)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@routers.get('/getusertotal', response_model=float)
def getusertotal(userid: int):
    try:
        total = get_total_price_of_basket(userid)
        return JSONResponse(status_code=status.HTTP_200_OK, content=total)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@routers.post('/save')
def save(source: str, dest: str):
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        src_path = os.path.join(base_dir, "data", source)
        dst_path = os.path.join(base_dir, "data", dest)

        if not os.path.exists(src_path):
            raise ValueError(f"Forrás fájl nem található: {source}")

        shutil.copy2(src_path, dst_path)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Sikeres mentés: {dest}")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@routers.post('/reload')
def reload(dest: str, source: str):
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        src_path = os.path.join(base_dir, "data", source)
        dst_path = os.path.join(base_dir, "data", dest)

        if not os.path.exists(src_path):
            raise ValueError(f"Forrás fájl nem található: {source}")

        shutil.copy2(src_path, dst_path)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Sikeres visszatöltés: {dest}")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
