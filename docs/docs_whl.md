## paddleocr_convert
<p>
    <a href=""><img src="https://img.shields.io/badge/Python->=3.7,<=3.10-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/paddleocr_convert/"><img alt="PyPI" src="https://img.shields.io/pypi/v/paddleocr_convert"></a>
    <a href="https://pepy.tech/project/paddleocr_convert"><img src="https://static.pepy.tech/personalized-badge/paddleocr_convert?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
    <a href="http://rapidai-team.com/PaddleOCRModelConverter/paddleocr_convert.html"><img height="20" alt="paddleocr_convert documentation" src="https://shields.mitmproxy.org/badge/API Docs-paddocr_convert-brightgreen.svg"></a>
</p>

### 1. Install package by pypi.
```bash
pip install paddleocr_convert
```

### 2. Run by command line.
- Usage:
    ```bash
    $ paddleocr_convert -h
    usage: paddleocr_convert [-h] [-p MODEL_PATH] [-o SAVE_DIR]
                            [-txt_path TXT_PATH]

    optional arguments:
    -h, --help            show this help message and exit
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

    $ paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar \
                        -o models \
                        -txt_path https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt

    # offline
    $ paddleocr_convert -p models/ch_PP-OCRv3_det_infer.tar \
                        -o models

    $ paddleocr_convert -p models/ch_PP-OCRv3_rec_infer.tar \
                        -o models \
                        -txt_path models/ppocr_keys_v1.txt
    ```

### 3. Run by script.
```python
from paddleocr_convert import PaddleOCRModelConvert

converter = PaddleOCRModelConvert()

save_dir = 'models'

# online
url = 'https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar'
txt_url = 'https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.6/ppocr/utils/ppocr_keys_v1.txt'

converter(url, save_dir, txt_path=txt_url)

# offline
model_path = 'models/ch_PP-OCRv3_rec_infer.tar'
txt_path = 'models/ppocr_keys_v1.txt'
converter(model_path, save_dir, txt_path=txt_path)
```

### See more details for [README](https://github.com/RapidAI/PaddleOCRModelConverter).