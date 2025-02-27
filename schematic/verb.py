import functools
import argparse
import inspect


def verb(func):
    """
    将一个函数声明为操作原语。
    """
    func.is_verb = True
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
        parser.add_argument('--script', help='Path to the script file', type=str)
        parsed_args = parser.parse_args()
        kwargs = vars(parsed_args)
        kwargs.pop('script')

        return func(**kwargs)

    return wrapper
