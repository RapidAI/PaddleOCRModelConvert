### PaddleOCR v3 相关模型转换
<p align="left">
    <a href="https://aistudio.baidu.com/aistudio/projectdetail/3974957?_=1652277622041&shared=1"><img src="https://img.shields.io/badge/PP-Open in AI Studio-blue.svg"></a>
</p>

- 本仓库会每天自动同步PaddleOCR仓库的代码
- 本仓库主要是针对性地将[PaddleOCR/release/v2.5](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_ch/models_list.md)转换为onnx模型
- 搭配[RapidOCR](https://github.com/RapidAI/RapidOCR)中相关推理代码使用更佳


### 使用步骤
1. 直接运行一下对应脚本即可
2. 最终转换后的模型会在`convert_model`目录下
3. 可以移步到[RapidOCR部分的python目录](https://github.com/RapidAI/RapidOCR/tree/main/python/onnxruntime_infer)，替换相应模型即可

### 更新日志
#### 2022-08-15 update:
- 将识别模型的字典写入到onnx模型中的meta中，便于后续分发。
