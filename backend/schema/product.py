from pydantic import BaseModel,Field,EmailStr
from typing import Literal


class Create_product(BaseModel):
  name:str=Field(...)
  price:float=Field(...)
  stock:int=Field(...)
  description:str=Field(...)
  category:str=Field(...)



class Userregister(BaseModel):
  username:str=Field(...)
  email:EmailStr=Field(...)
  password:str=Field(...)