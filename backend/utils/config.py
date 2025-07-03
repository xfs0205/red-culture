import configparser
import ast
from typing import Any, Dict

class ConfigManager:
    def __init__(self, file_path: str):
        """初始化配置管理器，自动加载配置文件"""
        self.config = configparser.ConfigParser()
        self.config.read(file_path, encoding='utf-8')

    def get_value(
        self,
        section: str,
        key: str,
        default: Any = None,
        dtype: type = str
    ) -> Any:
        """
        通用配置获取方法，支持类型转换
        :param section: 配置模块名（如mysql/cors）
        :param key: 配置项名
        :param default: 默认值（当配置不存在时返回）
        :param dtype: 目标类型（支持str/int/float/bool/list）
        """
        try:
            if dtype == bool:
                return self.config.getboolean(section, key, fallback=default)
            elif dtype == int:
                return self.config.getint(section, key, fallback=default)
            elif dtype == float:
                return self.config.getfloat(section, key, fallback=default)
            elif dtype == list:
                return self.get_list(section, key, default)
            else:
                return self.config.get(section, key, fallback=default)
        except (ValueError, configparser.Error) as e:
            print(f"配置解析错误: {e}")
            return default

    def get_list(self, section: str, key: str, default: list = None) -> list:
        """安全获取列表类型配置（如allow_origins）"""
        try:
            raw = self.config.get(section, key, fallback="")
            return ast.literal_eval(raw) if raw else (default or [])
        except (SyntaxError, ValueError):
            return default or []

    def __getattr__(self, section: str) -> Dict[str, Any]:
        """动态访问配置模块（如config.mysql返回字典）"""
        if section in self.config.sections():
            return {k: self.get_value(section, k) for k in self.config.options(section)}
        raise AttributeError(f"未找到配置模块: {section}")


# 使用示例
if __name__ == "__main__":
    # 初始化配置（假设配置文件为config.ini）
    config = ConfigManager("../config/config.ini")

    # 1. 读取MySQL配置（自动类型转换）
    mysql_host = config.get_value("mysql", "host")  # 返回str
    mysql_port = config.get_value("mysql", "port", dtype=int)  # 返回int

    # 2. 读取CORS配置（处理列表和布尔值）
    allow_origins = config.get_value("cors", "allow_origins", dtype=list)
    allow_credentials = config.get_value("cors", "allow_credentials", dtype=bool)

    # 3. 读取其他模块配置
    other_config = config.server

    print("MySQL配置:", mysql_host, mysql_port)
    print("CORS配置:", allow_origins, allow_credentials)
    print("其他模块配置:", other_config)