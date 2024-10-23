from schematic.logger import global_logger


def debug_output(message, use_logger=False):
    """
    在类被实例化或者方法被调用时向控制台打印一条消息。
    """
    def decorator(obj):
        if isinstance(obj, type):
            original_init = obj.__init__

            def new_init(self, *args, **kwargs):
                if use_logger:
                    global_logger.log(message)
                else:
                    print(message)
                original_init(self, *args, **kwargs)

            obj.__init__ = new_init
            return obj

        else:
            def new_func(*args, **kwargs):
                if use_logger:
                    global_logger.log(message)
                else:
                    print(message)
                return obj(*args, **kwargs)

            return new_func

    return decorator