# 小侠pipeline

## Getting started

```python
python -m run --workflow example --filename content.txt
```
## 我如何创建新脚本？
把新脚本放在`run/workflow`目录下，然后在`run/definition`中用`ScriptWithArgs`导入即可。

在新脚本中，请在所有的脚本最后添加`if __name__ == '__main__':`，并且调用入口函数。

在入口函数上使用@verb标记，框架会自动把workflow中的输入输出定义传递到入口函数的参数中。

可以使用`python -m run --help`查看你定义的全部workflow参数。

## 我如何创建新workflow？
在`run/__main__.py`中，把新的workflow中的ScriptWithArgs列表添加到if语句簇中即可。

### 神奇的ScriptWithArgs
`ScriptWithArgs`是一个装饰器，与verb配套使用，它会把workflow中的输入输出定义传递到入口函数的参数中。

ScriptWithArgs还有缓存的功能。如果把`cached`参数设置为True，那么框架会自动检查`cache_uri`是否为空，如果不为空，会跳过该脚本。




