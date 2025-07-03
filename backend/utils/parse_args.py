import argparse

def parse_args():
    """解析命令行参数，返回配置文件路径"""
    parser = argparse.ArgumentParser(description="初始化工具")
    parser.add_argument(
        "--conf",
        type=str,
        default="./config/config.ini",
        help="配置文件路径（默认：项目根目录下的config/config.ini）"
    )
    args = parser.parse_args()
    return args.conf
