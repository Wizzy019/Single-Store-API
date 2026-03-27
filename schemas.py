from pydantic import BaseModel,  constr, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int
    description:str

class OrderCreate(BaseModel):
    user_id: int
    total_price: int
    status: str

class OrderItemCreate(BaseModel):
     order_id: int
     product_id: int
     quantity: int