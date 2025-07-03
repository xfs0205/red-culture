from fastapi import Depends, APIRouter, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import crud

'''
在下面代码的参数中：
prefix：表示该模块父路径，其下面的子路径会直接与该路径拼接
tags：表示该模型标题，会在docs中显示
'''
router = APIRouter(prefix="/test", tags=["test"])

@router.get("/test1")
def test1():
    return {"message": "test1"}