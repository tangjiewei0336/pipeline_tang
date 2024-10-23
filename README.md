# FDS专家系统

## Getting started

请先安装requirements.txt中的依赖包

```shell
python -m run --filename wiper_NT2.pdf --workflow generation
```

workflow的可选值：
- generation （生成思维导图）
- validation （验证思维导图生成质量，如果generation还未执行会自动执行）
- graphing （把思维导图转换为知识图谱）

llm的可选值：
- qwen （使用qwen的模型）
- openai （使用openai的模型）

更多参数请查看`python -m run --help`


### fast run
#### validation
```shell
python -m run --filename="wiper_NT1.pdf" --workflow=validation --llm="qwen" 
python -m run --filename="wiper_NT2.pdf" --workflow=validation --llm="qwen" 
python -m run --filename="Fridge_NT2.pdf" --workflow=validation --llm="qwen" 
python -m run --filename="ECO Plus Mode_NT2.pdf" --workflow=validation --llm="qwen"  
```
#### graphing（目前还不是全自动的）
```shell
python -m run --filename="wiper_NT1.pdf" --workflow=graphing --llm="qwen" 
```