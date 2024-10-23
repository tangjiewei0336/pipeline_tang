import functools
import argparse
import inspect


def verb(func):
    """
    将一个函数声明为操作原语。
    """
    @functools.wraps(func)
    def wrapper():
        parser = argparse.ArgumentParser(description=func.__doc__)

        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            arg_name = f'--{name}'
            arg_kwargs = {
                'type': param.annotation if param.annotation != inspect.Parameter.empty else str,
                'help': f'{name} of type {param.annotation.__name__}' if param.annotation != inspect.Parameter.empty else f'{name}',
            }
            if param.default != inspect.Parameter.empty:
                arg_kwargs['default'] = param.default
            else:
                arg_kwargs['required'] = True
            parser.add_argument(arg_name, **arg_kwargs)

        parsed_args = parser.parse_args()
        return func(**vars(parsed_args))

    return wrapper
