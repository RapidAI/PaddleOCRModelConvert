## paddleocr_convert
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/paddleocr_convert/"><img alt="PyPI" src="https://img.shields.io/pypi/v/paddleocr_convert"></a>
</p>

### 1. Install package by pypi.
```bash
pip install paddleocr_convert
```

### 2. Run by command line.
- Usage:
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
- Example:
    ```bash
    $ paddleocr_convert -url https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar -o models

    $ paddleocr_convert -url https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar \
                        -o models \
                        -txt_url https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt
    ```

### See more details for [README](https://github.com/RapidAI/PaddleOCRModelConverter).