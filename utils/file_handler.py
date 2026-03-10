"""

"""
import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(filepath: str):
    """
    获取文件的MD5的十六进制字符串
    :param filepath:文件路径
    :return:MD5的十六进制字符串
    """
    if not filepath:
        logger.error("[get_file_md5_hex]filepath is empty")
        return None
        
    if not os.path.exists(filepath):
        logger.error(f"[get_file_md5_hex]path {filepath} not exist")
        return None
        
    if not os.path.isfile(filepath):
        logger.error(f"[get_file_md5_hex]path {filepath} not file")
        return None

    md5_obj = hashlib.md5()

    chunk_size = 4096
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[get_file_md5_hex]file {filepath} md5 calculation error: {e}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    返回文件夹内的文件列表（允许的后缀）
    :return:
    """
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]path {path} not dir")
        return []

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return files


def pdf_loader(filepath: str, password: str) -> list[Document]:
    """
    加载PDF文件
    :param filepath: PDF文件路径
    :param password: PDF密码
    :return: 文档列表
    """
    try:
        loader = PyPDFLoader(filepath, password=password)
        documents = loader.load()
        logger.info(f"[pdf_loader]Successfully loaded {filepath} with {len(documents)} pages")
        return documents
    except Exception as e:
        logger.error(f"[pdf_loader]Failed to load {filepath}: {e}")
        return []


def txt_loader(filepath: str) -> list[Document]:
    """
    加载文本文件
    :param filepath: 文本文件路径
    :return: 文档列表
    """
    try:
        loader = TextLoader(filepath, encoding='utf-8')
        documents = loader.load()
        logger.info(f"[txt_loader]Successfully loaded {filepath}")
        return documents
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            loader = TextLoader(filepath, encoding='gbk')
            documents = loader.load()
            logger.info(f"[txt_loader]Successfully loaded {filepath} with GBK encoding")
            return documents
        except Exception as e:
            logger.error(f"[txt_loader]Failed to load {filepath} with multiple encodings: {e}")
            return []
    except Exception as e:
        logger.error(f"[txt_loader]Failed to load {filepath}: {e}")
        return []
