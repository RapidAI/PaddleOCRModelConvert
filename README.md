### PaddleOCR v3 相关模型转换
<p align="left">
    <a href="https://aistudio.baidu.com/aistudio/projectdetail/3974957?_=1652277622041&shared=1"><img src="https://img.shields.io/badge/PP-Open in AI Studio-blue.svg"></a>
</p>

- 本仓库主要是针对性地将[PaddleOCR/release/v2.5](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_ch/models_list.md)转换为onnx模型
- 搭配[RapidOCR](https://github.com/RapidAI/RapidOCR)中相关推理代码使用更佳

### 运行环境
- 操作系统： Linux / Mac
- 安装依赖包:
    ```bash
    pip install -r requirements.txt -i https://pypi.douban.com/simple/
    ```
- 测试可以成功转换的库版本如下：
  ```txt
  onnx                        1.8.0
  onnxruntime                 1.10.0
  opencv-python               4.2.0.32
  paddle2onnx                 0.9.0
  paddlepaddle-gpu            2.0.2.post100
  ```

### 使用步骤
1. 直接运行一下对应脚本即可
    - 推理模型转换
        ```shell
        $ bash det_inference_to_onnx.sh
        # bash cls_inference_to_onnx.sh  # 这个模型转换后误差较大
        $ bash rec_inference_to_onnx.sh
        ```
    - 预训练模型转换
        ```shell
        $ bash det_pretrain_to_onnx.sh
        $ bash cls_pretrain_to_onnx.sh
        $ bash rec_pretrain_to_onnx.sh
        ```
    - 如果遇到`rec_inference_to_onnx.sh: line 3: $'\r': command not found`类似错误
        ```bash
        $ vi rec_inference_to_onnx.sh

        # vi中执行以下命令即可
        # :set ff=unix
        # :wq
        ```
2. 最终转换后的模型会在`convert_model`目录下
3. 可以移步到[RapidOCR部分的python目录](https://github.com/RapidAI/RapidOCR/tree/main/python/onnxruntime_infer)，替换相应模型即可

### 更新日志
#### 2022-08-15 update:
- 将识别模型的字典写入到onnx模型中的meta中，便于后续分发。
