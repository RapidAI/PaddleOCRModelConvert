<div align="center">
     <div align="center">
        <h1><b><i>🔄 PaddleOCR Model Convert</i></b></h1>
     </div>
     <div>&nbsp;</div>
     <a href="https://huggingface.co/spaces/SWHL/PaddleOCRModelConverter" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%A4%97 -Online Convert-blue"></a>
     <a href="https://www.modelscope.cn/studios/liekkas/PaddleOCRModelConverter/summary" target="_blank"><img src="https://img.shields.io/badge/ModelScope-Online Convert -blue"></a>
     <a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
     <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
     <a href="https://pypi.org/project/paddleocr_convert/"><img alt="PyPI" src="https://img.shields.io/pypi/v/paddleocr_convert"></a>
     <a href="https://pepy.tech/project/paddleocr_convert"><img src="https://static.pepy.tech/personalized-badge/paddleocr_convert?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads "></a>
    <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</div>

### Introduction

- This repository is mainly to convert [Inference Model in PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md) into ONNX format.
- **Input**: **url** or local **tar** path of inference model
- **Output**: converted **ONNX** model
- If it is a recognition model, you need to provide the original txt path of the corresponding dictionary (**Open the txt file in github, click the path after raw in the upper right corner, similar to [this](https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt)**), used to write the dictionary into the ONNX model
- ☆ It needs to be used with the relevant reasoning code in [RapidOCR](https://github.com/RapidAI/RapidOCR)
- If you encounter a model that cannot be successfully converted, you can check which steps are wrong one by one according to the ideas in the figure below.

### Overall framework

```mermaid
flowchart TD

A([PaddleOCR inference model]) --paddle2onnx--> B([ONNX])
B --> C([Change Dynamic Input]) --> D([Rec: save the character dict to onnx])
D --> E([Save])
```

### Installation

```bash
pip install paddleocr_convert
```

### Usage
>
> [!WARNING]
>
> Only support the **reasoning model** in the download address in [link](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md), if it is a training model, Manual conversion to inference format is required.
>
> The **slim quantized model** in PaddleOCR does not support conversion.

#### Using the command line

- Usage:

    ```bash
    $ paddleocr_convert -h
    usage: paddleocr_convert [-h] [-p MODEL_PATH] [-o SAVE_DIR]
                            [-txt_path TXT_PATH]

    optional arguments:
    -h, --help show this help message and exit
    -p MODEL_PATH, --model_path MODEL_PATH
                            The inference model url or local path of paddleocr.
                            e.g. https://paddleocr.bj.bcebos.com/PP-
                            OCRv3/chinese/ch_PP-OCRv3_det_infer.tar or
                            models/ch_PP-OCRv3_det_infer.tar
    -o SAVE_DIR, --save_dir SAVE_DIR
                            The directory of saving the model.
    -txt_path TXT_PATH, --txt_path TXT_PATH
                            The raw txt url or local txt path, if the model is
                            recognition model.
    ```

- Example:

    ```bash
    # online
    $ paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar \
                        -o models

    $ paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar\
                        -o models\
                        -txt_path https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt

    # offline
    $ paddleocr_convert -p models/ch_PP-OCRv3_det_infer.tar \
                        -o models

    $ paddleocr_convert -p models/ch_PP-OCRv3_rec_infer.tar \
                        -o models\
                        -txt_path models/ppocr_keys_v1.txt
    ```

#### Script use

- online mode

    ```python
    from paddleocr_convert import PaddleOCRModelConvert

    converter = PaddleOCRModelConvert()
    save_dir = 'models'
    url = 'https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar'
    txt_url = 'https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt'

    converter(url, save_dir, txt_path=txt_url)
    ```

- offline mode

    ```python
    from paddleocr_convert import PaddleOCRModelConvert

    converter = PaddleOCRModelConvert()
    save_dir = 'models'
    model_path = 'models/ch_PP-OCRv3_rec_infer.tar'
    txt_path = 'models/ppocr_keys_v1.txt'
    converter(model_path, save_dir, txt_path=txt_path)
    ```

### Use the model

Assuming that the model needs to be recognized in Japanese, and it has been converted, the path is `local/models/japan.onnx`

1. Install `rapidocr` library

    ```bash
    # rapidocr v3.2.0
    pip install rapidocr onnxruntime
    ```

2. Script use

    ```python
    from rapidocr import RapidOCR

    model_path = 'local/models/japan.onnx'
    engine = RapidOCR(params={'Rec.model_path': model_path})

    img_url = "https://img1.baidu.com/it/u=3619974146,1266987475&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=516"
    result = engine(img_url)
    print(result)
    result.vis('vis_result.jpg)
    ```

### Changelog ([more](https://github.com/RapidAI/PaddleOCRModelConvert/releases))

<details>
    <summary>Click to expand</summary>

- 2023-09-22 v0.0.17 update:
    - Improve the log when meets the error.
- 2023-07-27 v0.0.16 update:
    - Added the online conversion version of ModelScope.
    - Change python version from python 3.6 ~ 3.11.
- 2023-04-13 update:
    - Add online conversion program [link](https://huggingface.co/spaces/SWHL/PaddleOCRModelConverter)
- 2023-03-05 v0.0.4~7 update:
    - Support transliteration of local models and dictionaries
    - Optimize internal logic and error feedback
- 2023-02-28 v0.0.3 update:
    - Added setting to automatically change to dynamic input for models that are not dynamic input
- 2023-02-27 v0.0.2 update:
    - Encapsulate the conversion model code into a package, which is convenient for self-help model conversion
- 2022-08-15 v0.0.1 update:
    - Write the dictionary of the recognition model into the meta in the onnx model for subsequent distribution.

</details>
