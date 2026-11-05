from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List

'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a
   kliens oldalon is jelezni kell.

'''

ShopName = 'Bolt'

class Item(BaseModel):
    item_id: int = Field(..., ge=0)
    name: str
    brand: str
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)

    @field_validator('item_id', 'price', 'quantity')
    @classmethod
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError('Az érték nem lehet negatív')
        return v


class Basket(BaseModel):
    id: int = Field(..., ge=0)
    user_id: int = Field(..., ge=0)
    items: List[Item]

    @field_validator('id', 'user_id')
    @classmethod
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError('Az érték nem lehet negatív')
        return v


class User(BaseModel):
    id: int = Field(..., ge=0)
    name: str
    email: EmailStr

    @field_validator('id')
    @classmethod
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError('Az azonosító nem lehet negatív')
        return v
