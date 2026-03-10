import os
from datetime import datetime
from utils.config_handler import agent_conf
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

rag = RagSummarizeService()


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query) -> str:
    return rag.rag_summarize(query)


@tool(description="获取用户所在城市")
def get_location():
    return "上海"


@tool(description="获取用户id")
def get_user_id():
    return "10001"


@tool(description="获取当前年月日信息，返回纯字符串")
def get_date() -> str:
    return datetime.now().strftime('%Y-%m-%d')


external_data = {}


def generate_study_record():
    """
    {
        "user_id": {
            "month": {"..."}
            "month": {"..."}
        }
        "user_id": {
            "month": {"..."}
            "month": {"..."}
        }
        "user_id": {
            "month": {"..."}
            "month": {"..."}
        }
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"external data path {external_data_path} does not exist")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                arr = line.strip().split("$")
                user_id = arr[0].replace('"', "")
                event_type = arr[1].replace('"', "")
                skill = arr[2].replace('"', "")
                details = arr[3].replace('"', "")
                year = arr[4].replace('"', "")
                month = arr[5].replace('"', "")
                day = arr[6].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}
                if year not in external_data[user_id]:
                    external_data[user_id][year] = {}
                if month not in external_data[user_id][year]:
                    external_data[user_id][year][month] = []

                external_data[user_id][year][month].append({
                    "类型": event_type,
                    "技术栈": skill,
                    "详情": details,
                    "日期": year+"/"+month+"/"+day
                })


@tool(description="获取指定用户在特定月份内的学习记录，输入为年月以及用户id，输出纯字符串。若未检索到内容，返回空字符串。")
def get_study_record(user_id, year, month) -> dict:
    generate_study_record()

    try:
        return external_data[user_id][year][month]
    except KeyError:
        logger.warning(f"[get_study_record]can't find required records")
        return {}


@tool(description="将经过总结的用户学习内容录入至外部文件，输入为用户id、学习内容字符串、年、月、日。若录入成功，返回“录入成功”；若录入失败，返回“录入失败”")
def save_study_record(user_id, study_info, year, month, day):
    external_data_path = get_abs_path(agent_conf["external_data_path"])
    if not os.path.exists(external_data_path):
        raise FileNotFoundError(f"external data path {external_data_path} does not exist")
    try:
        with open(external_data_path, "a", encoding="utf-8") as f:
            f.write(f"{user_id}${study_info}${year}${month}${day}\n")
            f.close()
            return "录入成功"
    except Exception as e:
        logger.error(f"[save_study_record]save study record failed: {e}")
        return "录入失败"


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"


if __name__ == '__main__':
    res = rag_summarize("python列表的用法")
    print(res)
    pass
