from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base, get_engine

# 样例
class User(Base):
    __tablename__ = "users"

    id = Column(String(6), primary_key=True)
    number_phone = Column(String(11), unique=True, index=True)
    hashed_password = Column(String(500))
    username = Column(String(20), default="体验用户")
    is_active = Column(Boolean, default=True)
    power = Column(Integer, default=1)
    email = Column(String(255), default="")
    head_img = Column(String(255), default="BackEnd/DataBase/Profile/Image/image.png")

    HistoryChat = relationship("UserAIHistory", back_populates="from_user")
    to_profile = relationship("Profile", back_populates="from_user")


if __name__ == "__main__":
    Base.metadata.create_all(bind=get_engine)
    print("数据库表刷新完毕")
