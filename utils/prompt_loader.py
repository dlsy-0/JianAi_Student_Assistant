from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_conf['system_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_system_prompts]can't find 'system_prompt_path' in prompts.yml")
        raise e

    try:
        return open(system_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_system_prompts]'{system_prompt_path}' read error: {str(e)}")
        raise e


def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]can't find 'rag_summarize_prompt_path' in prompts.yml")
        raise e

    try:
        return open(rag_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]'{rag_prompt_path}' read error: {str(e)}")
        raise e


def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_report_prompts]can't find 'report_prompt_path' in prompts.yml")
        raise e

    try:
        return open(report_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_report_prompts]'{report_prompt_path}' read error: {str(e)}")
        raise e


system_prompt = load_system_prompts()
rag_prompt = load_rag_prompts()
report_prompt = load_report_prompts()

