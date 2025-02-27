import pathlib
from dataclasses import dataclass

from schematic.logger import global_logger


@dataclass
class ScriptWithArgs:
    script_name: str
    args: dict
    enabled: bool = True
    cached: bool = False
    cache_uri: str | pathlib.Path = ""

    def __iter__(self):
        if self.enabled:
            if self.cached:
                if self.cache_uri == "":
                    raise ValueError("cache_folder must be set when cached is True")
                else:
                    if isinstance(self.cache_uri, str):
                        cache_path = pathlib.Path(self.cache_uri)
                    else:
                        cache_path = self.cache_uri
                    # 判断是目录还是文件
                    if cache_path.is_file():
                        if cache_path.exists():
                            global_logger.log(f"Using cached result for {self.script_name}")
                            yield "noscript"
                            yield []
                            return
                        else:
                            yield self.script_name
                            yield self.args
                            return
                    elif cache_path.exists() and list(cache_path.iterdir()):
                        global_logger.log(f"Using cached result for {self.script_name}")
                        yield "noscript"
                        yield []
                        return
                    else:
                        yield self.script_name
                        yield self.args
                        return
            yield self.script_name
            yield self.args
        else:
            yield "noscript"
            yield []


@dataclass
class PlaceHolder:
    description: str

    def __iter__(self):
        global_logger.log(self.description)
        yield "noscript"
        yield []


@dataclass
class Exit:
    description: str

    def __iter__(self):
        global_logger.log(self.description)
        yield "exit"
        yield []