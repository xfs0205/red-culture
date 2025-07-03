from pydantic import BaseModel


# 样例
class UserBase(BaseModel):
    number_phone: str
    username: str
