from functools import wraps, partial
import os
from inspect import signature
from typing import List, Callable

from run.workflow.components.concurrency.concurrent import AnalysisChainExecutor
from run.workflow.llm.qwen_embedding_langchain_base import QwenEmbeddings
from run.workflow.llm.qwen_langchain_base import chat_total_invocations, chat_total_tokens
from schematic.logger import global_logger


def iterate(iterable_arg_index):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取需要迭代的参数
            iterable_arg = args[iterable_arg_index]
            # 创建callable对象列表
            callables = []
            for item in iterable_arg:
                # 为每个迭代项创建一个新的callable对象
                # 我们使用partial来固定迭代的参数
                from functools import partial
                callables.append(partial(func, *args[:iterable_arg_index], item, *args[iterable_arg_index + 1:]))
            return callables

        return wrapper

    return decorator


def iterate_files(file_extension=".md", folder_arg_name='folder_path', file_arg_name="file_path",
                  parallel_execution=True, max_workers=10, progress_report=True):
    """
    根据函数签名中的特定参数迭代文件夹中的所有文件，为每个文件根据函数内容创建一个callable对象，并按照选定的方式进行执行。
    函数签名中其他的参数将原样传递给被装饰函数。
    :param file_extension: 需要的文件扩展名，例如".md"
    :param folder_arg_name: 被装饰函数的签名中需要迭代其中的文件的文件夹参数的名称
    :param file_arg_name: 被装饰函数的签名中文件参数的名称，这个参数将被替换为文件的路径
    :param parallel_execution: 是否并行执行
    :param max_workers: 最大工作线程数，仅当parallel_execution为True时有效
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global chat_total_invocations
            sig = signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            args_dict = bound_args.arguments

            folder_path = args_dict[folder_arg_name]

            files = [f for f in os.listdir(folder_path) if f.endswith(file_extension.strip('*'))]

            callables = []
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                new_args_dict = {k: file_path if k == file_arg_name else v for k, v in args_dict.items()}
                callables.append(partial(func, **new_args_dict))
            chat_total_invocations = 0
            QwenEmbeddings.total_invocations = 0

            if parallel_execution:
                result_list = AnalysisChainExecutor().add_command(callables).execute(max_workers=max_workers, suppress_progressbar=not progress_report)
            else:
                result_list = [c() for c in callables]
            if chat_total_invocations > 0:
                global_logger.instant_log(f"Chat Invocation Summary: {chat_total_invocations} times in this iteration.")
            if QwenEmbeddings.total_invocations > 0:
                global_logger.instant_log(f"Embeddings Invocation Summary: {QwenEmbeddings.total_invocations} times, {QwenEmbeddings.total_tokens} tokens is this iteration.")

            return result_list

        return wrapper

    return decorator


@iterate_files()
def process_file(folder_path, file_path=None) -> List:
    print(f"Processing folder: {folder_path}: file {file_path}")


