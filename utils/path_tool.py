"""
为整个工程提供统一的绝对路径
"""
import os


def get_project_tool() -> str:
    """
    获取工程所在的根目录
    :return: 字符串目录
    """

    # 当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    # 获取当前文件夹的绝对路径
    current_dir = os.path.dirname(current_file)
    # 获取工程的根目录
    project_dir = os.path.dirname(current_dir)

    return project_dir


def get_abs_path(relative_path: str) -> str:
    """
    传递相对路径，返回绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """

    # 获取相对路径
    project_root = get_project_tool()
    # 拼接得到绝对路径
    return os.path.join(project_root, relative_path)
