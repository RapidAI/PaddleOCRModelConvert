### PaddleOCR模型转换
- 本仓库主要是针对性地将[PaddleOCR提供模型](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_ch/models_list.md)转换为onnx模型
- 搭配[RapidOCR](https://github.com/RapidAI/RapidOCR)中相关推理代码使用更加

### 使用步骤
1. 从这里下载自己需要转换的**推理**或者**预训练模型**，保存到`pretrained_models`目录下
2. 配置并运行一下脚本
   **Note: 注意配置里面相应参数**
    - 如果下载的是推理模型
        ```shell
        bash convert_rec_infer_model.sh
        ```
    - 如果是预训练模型
        ```shell
        bash convert_rec_pretrain_model.sh
        ```
3. 最终转换后的模型会在`conver_model`目录下