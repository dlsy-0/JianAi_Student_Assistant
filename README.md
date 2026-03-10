# JianAi_Student_Assistant
本项目是一个面向学习场景的轻量“学生助手”原型，提供对话式问答（Chat）、资料检索增强生成（RAG / 检索增强生成）与学习记录查询/写入等能力：通过向量库检索知识片段并交给大模型总结，同时支持按用户、年月读取外部学习记录并追加保存。技术栈采用 Python + LangChain（Agent/ReAct 工具调用链）+ Chroma 向量数据库，Embedding/Chat 使用通义（DashScopeEmbeddings、ChatTongyi），前端交互用 Streamlit。项目意义在于把“资料检索 + 总结回答 + 结构化记录”串成可运行闭环，便于快速验证学习助手的流程与数据落地方式。
