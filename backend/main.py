import logging

from database import setup_database
from routers import Route
from utils import ConfigManager, parse_args

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":

    # 0. 读取全部配置
    conf_path = parse_args()
    config = ConfigManager(conf_path)
    logging.info(f"加载配置文件路径: {conf_path}")

    # 1. 读取MySQL配置（自动类型转换）
    mysql_host = config.get_value("mysql", "host")  # 返回str
    mysql_port = config.get_value("mysql", "port", dtype=int)  # 返回int
    mysql_user = config.get_value("mysql", "user")
    mysql_password = config.get_value("mysql", "password")
    mysql_db = config.get_value("mysql", "database")
    setup_database(
        f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
    )

    # 2. 读取CORS配置（处理列表和布尔值）
    allow_origins = config.get_value("cors", "allow_origins", dtype=list)
    allow_credentials = config.get_value("cors", "allow_credentials", dtype=bool)
    allow_methods = config.get_value("cors", "allow_methods", dtype=list)
    allow_headers = config.get_value("cors", "allow_headers", dtype=list)

    # 3. 创建路由
    route = Route(
        host=config.get_value("server", "host"),
        port=config.get_value("server", "port", dtype=int),
        img_path=config.get_value("server", "img_path"),
        video_path=config.get_value("server", "video_path"),
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )

    # 4. 运行路由
    route.run()
