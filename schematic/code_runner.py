import argparse
import importlib.util
import inspect
import select
import signal
import os
import sys
import threading

from schematic.logger import global_logger

my_message_queue = {}
queue_lock = threading.Lock()

# 标志来表示信号处理程序的操作
process_input_flag = threading.Event()

def stdin_has_data():
    """使用 select.select() 非阻塞地判断 stdin 是否有数据"""
    return select.select([sys.stdin], [], [], 0.0)[0]

def signal_handler(signum, frame):
    """Signal handler function to process interrupt signal."""
    if signum == signal.SIGUSR1:
        # 使用标志通知主程序进行消息读取处理
        process_input_flag.set()

def process_input():
    """主程序读取 stdin 并处理消息队列。"""
    while True:
        if process_input_flag.is_set():
            # 处理信号中传递的消息
            process_input_flag.clear()

            while stdin_has_data():
                msg = input()
                info = msg.split('$')
                if len(info) == 2:
                    channel = int(info[0])
                    message = info[1]
                    # 使用锁来保证线程安全
                    with queue_lock:
                        if channel not in my_message_queue:
                            my_message_queue[channel] = []
                        my_message_queue[channel].append(message)
                    global_logger.instant_log(f"Message received: {message} on channel {channel}")
                else:
                    global_logger.instant_log(f"Invalid message format: {msg}")


def find_verb_function_from_file(file_path):
    # 获取文件的绝对路径和目录
    file_path = os.path.abspath(file_path)
    module_dir = os.path.dirname(file_path)
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 从执行根目录到目标目录逐步添加路径
    current_dir = os.getcwd()
    root_dir = os.path.abspath(os.sep)
    while current_dir != module_dir and current_dir != root_dir:
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        current_dir = os.path.dirname(current_dir)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    try:
        # 使用 importlib.util 来加载模块
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"Cannot create module spec for {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 查找带有 is_verb 属性的函数
        functions = inspect.getmembers(module, inspect.isfunction)
        for name, func in functions:
            if hasattr(func, 'is_verb') and getattr(func, 'is_verb'):
                return func

    except Exception as e:
        print(f"Error loading module from {file_path}: {e}")

    finally:
        # 清理路径，确保安全
        sys.path = [p for p in sys.path if os.path.abspath(p) not in (module_dir, current_dir)]

    return None


def run_script(script_relative_path):
    input_thread = threading.Thread(target=process_input, daemon=True)
    input_thread.start()
    signal.signal(signal.SIGUSR1, signal_handler)
    verb_func = find_verb_function_from_file(script_relative_path)

    if verb_func is None:
        raise Exception(f"Cannot find verb function in {script_relative_path}. If you believe you have a verb function, "
                        f"check for circular imports or ensure that the function is decorated with @verb.")

    verb_func()


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    parser = argparse.ArgumentParser(description="Code runner script")
    parser.add_argument("--script", help="Path to the script file", type=str)

    args, unknown_args = parser.parse_known_args()

    args_dict = vars(args)

    # 解析脚本参数
    for arg in unknown_args:
        if arg.startswith("--"):
            key_value = arg.split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                args_dict[key.lstrip("--")] = value
            else:
                # 如果参数没有=
                args_dict[arg.lstrip("--")] = None

    run_script(args.script)