### paddleocr_convert
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/paddleocr_convert/"><img alt="PyPI" src="https://img.shields.io/pypi/v/paddleocr_convert"></a>
    <a href="https://pepy.tech/project/paddleocr_convert"><img src="https://static.pepy.tech/personalized-badge/paddleocr_convert?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

- 本仓库主要是针对性地将[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md)转换为onnx模型
- **注意**：
  - 输入是模型的url，输出即是转换后的ONNX模型。
  - 如果是识别模型，需要提供对应字典的原始txt路径，用来将字典写入到onnx模型中
- 搭配[RapidOCR](https://github.com/RapidAI/RapidOCR)中相关推理代码使用


### 使用步骤
1. 安装`paddleocr_convert`
   ```bash
   pip install paddleocr_convert
   ```
2. 命令行使用
   - 用法:
        ```bash
        $ paddleocr_convert -h
        usage: paddleocr_convert [-h] [-url MODEL_URL] [-o SAVE_DIR]
                                [-txt_url TXT_URL]

        optional arguments:
        -h, --help            show this help message and exit
        -url MODEL_URL, --model_url MODEL_URL
                                The inference model url of paddleocr. e.g.
                                https://paddleocr.bj.bcebos.com/PP-
                                OCRv3/chinese/ch_PP-OCRv3_det_infer.tar
        -o SAVE_DIR, --save_dir SAVE_DIR
                                The directory of saving the model.
        -txt_url TXT_URL, --txt_url TXT_URL
                                The raw txt url, if the model is recognition model.
        ```
   - 示例:
        ```bash
        $ paddleocr_convert -url https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar -o models

        $ paddleocr_convert -url https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar \
                            -o models \
                            -txt_url https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt
        ```
3. 脚本使用
    ```python
    from paddleocr_convert import PaddleOCRModelConvert

    converter = PaddleOCRModelConvert()

    url = 'https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar'

    save_dir = 'models'
    txt_url = 'https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt'

    converter(url, save_dir, txt_url=txt_url)
    ```

 可以移步到[RapidOCR部分的python目录](https://github.com/RapidAI/RapidOCR/tree/main/python/onnxruntime_infer)，替换相应模型即可


### 更新日志
- 2023-02-17 v0.0.2 update:
  - 将转换模型代码封装成包，便于自助转模型

- 2022-08-15 v0.0.1 update:
  - 将识别模型的字典写入到onnx模型中的meta中，便于后续分发。
