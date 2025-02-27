import logging
import inspect
import os
import sys


class ColoredLogger:
    """
    小侠特制的日志记录器，用于在控制台输出彩色日志，提供四种日志级别：CRITICAL、ERROR、WARNING、INFO。

    Windows系统可能不支持彩色日志。
    """
    COLORS = {
        'CRITICAL': '\033[95m',  # Purple
        'ERROR': '\033[91m',  # Red
        'WARNING': '\033[93m',  # Yellow
        'INFO': '\033[92m',  # Green
        'RESET': '\033[0m'  # Reset to default color
    }

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            level_name = record.levelname
            color = ColoredLogger.COLORS.get(level_name, ColoredLogger.COLORS['RESET'])
            record.levelname = f"{color}{level_name}{ColoredLogger.COLORS['RESET']}"
            return super().format(record)

    def __init__(self, name='1'):
        # 获得命令行宽度
        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            print("无法获取终端宽度，使用默认值。")
            terminal_width = 150
        self.MAX_LINE_LENGTH = terminal_width - 65
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = self.ColoredFormatter(
            f'%(asctime)s ｜%(levelname)-18s\t %(continue)s｜%(message)-{self.MAX_LINE_LENGTH + 5}s｜%(classname)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def instant_log(self, msg):
        msg = msg.replace('\n', '\x10')
        print(f"{{log}}{msg}")
        # flush
        sys.stdout.flush()

    def log(self, msg, level='INFO', same_line=False, origin=None):
        """
        输出日志。
        :param msg: 日志内容
        :param level: 可选，日志级别，可选值为'CRITICAL'、'ERROR'、'WARNING'、'INFO'（默认）。
        """
        # 获取调用方的信息
        frame = inspect.currentframe().f_back
        if origin is not None:
            classname = origin
        else:
            classname = frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.f_locals else 'N/A'
        extra = {'classname': classname, "continue": ''}
        msgs = msg.split("\n")
        continue_mark = ''
        for msg in msgs:
            while len(msg) > 0:
                extra['continue'] = f'\r{" " * 34}\t>' if continue_mark == '  ...' else ''
                continue_mark = '  ...' if len(msg) > self.MAX_LINE_LENGTH else ''
                if level == 'CRITICAL':
                    self.logger.critical(msg[:self.MAX_LINE_LENGTH] + continue_mark, extra=extra)
                elif level == 'ERROR':
                    self.logger.error(msg[:self.MAX_LINE_LENGTH] + continue_mark, extra=extra)
                elif level == 'WARNING':
                    self.logger.warning(msg[:self.MAX_LINE_LENGTH] + continue_mark, extra=extra)
                elif level == 'INFO':
                    self.logger.info(msg[:self.MAX_LINE_LENGTH] + continue_mark, extra=extra)
                msg = msg[self.MAX_LINE_LENGTH:]
        # flush
        sys.stdout.flush()

    def enable_save_log(self, path):
        """
        保存日志到文件。
        :param path: 日志文件路径
        """
        handler = logging.FileHandler(path)
        formatter = self.ColoredFormatter(
            f'%(asctime)s ｜%(levelname)-18s\t %(continue)s｜%(message)-{self.MAX_LINE_LENGTH + 5}s｜%(classname)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


global_logger = ColoredLogger()


class ExampleClass:
    def __init__(self):
        self.logger = ColoredLogger()

    def run(self):
        self.logger.log("This is an example message", level='INFO')
        self.logger.log("This is an example message", level='WARNING')
        self.logger.log("This is an example message", level='ERROR')
        self.logger.log("This is an example message", level='CRITICAL')
        self.logger.log("123")


if __name__ == "__main__":
    example = ExampleClass()
    example.run()
