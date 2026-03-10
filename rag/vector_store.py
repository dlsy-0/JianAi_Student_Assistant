import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from model.factory import embedding_model
from utils.config_handler import chroma_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_conf["persist_directory"]),
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        需要计算md5完成去重
        :return:None
        """

        def check_md5_hex(md5: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False            # md5未处理过

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5:
                        return True     # md5处理过

                return False            # md5未处理过

        def save_md5_hex(md5: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5 + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path, "123456")
            if read_path.endswith(".txt"):
                return txt_loader(read_path)

            return []

        allowed_files_path = listdir_with_allowed_type(
            path=get_abs_path(chroma_conf["data_path"]),
            allowed_types=tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            # 确保路径是绝对路径
            abs_path = get_abs_path(path) if not os.path.isabs(path) else path
            
            md5_hex = get_file_md5_hex(abs_path)
            if md5_hex is None:
                logger.error(f"[load_document]{abs_path} MD5 calculation failed")
                continue
                
            if check_md5_hex(md5_hex):
                logger.info(f"[load_document]{abs_path} already exists in knowledge base")
                continue
            try:
                documents: list[Document] = get_file_documents(abs_path)

                if not documents:
                    logger.warning(f"[load_document]{abs_path} has no documents")
                    continue

                # 过滤空文档
                valid_documents = []
                for doc in documents:
                    if doc.page_content and doc.page_content.strip():
                        valid_documents.append(doc)
                    else:
                        logger.warning(f"[load_document]{abs_path} has empty document page")
                
                if not valid_documents:
                    logger.warning(f"[load_document]{abs_path} has no valid documents after filtering")
                    continue

                split_document = self.splitter.split_documents(valid_documents)

                if not split_document:
                    logger.warning(f"[load_document]{abs_path} has no effective sharding")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)
                # 保存md5
                save_md5_hex(md5_hex)

                logger.info(f"[load_document]{abs_path} saved successfully")
            except Exception as e:
                logger.error(f"[load_document]{abs_path} failed error: {e}", exc_info=True)
                continue


if __name__ == '__main__':
    print("0")
    vs = VectorStoreService()
    print("1")
    vs.load_document()
    print("2")
    retriever = vs.get_retriever()
    print("3")
    res = retriever.invoke("字典")
    print("4")
    for i in res:
        print(i.page_content)
        print("-"*20)
