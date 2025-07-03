import logging

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# 声明数据库连接变量
SQLALCHEMY_DATABASE_URL: str is None
engine: Engine is None
SessionLocal: sessionmaker is None
Base = declarative_base()


def setup_database(url: str) -> None:
    """初始化数据库连接并测试连通性"""
    global SQLALCHEMY_DATABASE_URL, engine, SessionLocal

    # 1. 创建引擎
    engine = create_engine(url)

    # 2. 测试连接
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # 简单查询测试
            logger.info("Database connection successful")

    except OperationalError as e:
        logger.error("Database connection failed")
        raise ConnectionError(f"Database connection failed: {e}") from e

    # 3. 初始化SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    SQLALCHEMY_DATABASE_URL = url


def get_engine() -> Engine:
    """获取数据库引擎"""
    if engine is None:
        raise RuntimeError("Database not initialized. Call setup_database() first.")
    return engine


def get_db():
    """获取数据库会话"""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call setup_database() first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
