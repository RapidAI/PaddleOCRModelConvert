# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
import os

import onnx

from .utils import download_file, unzip_file


class PaddleOCRModelConvert():
    def __init__(self) -> None:
        self.opset = 12

    def __call__(self, model_url: str, save_dir: str, txt_url: str = None):
        model_name = Path(model_url).stem
        is_rec = 'rec' in model_name
        if is_rec and not txt_url:
            raise ValueError('Please give the txt url.')

        # 下载模型
        model_path = download_file(model_url, save_dir)

        # 解压模型
        model_dir = unzip_file(model_path, save_dir)

        # 转换模型
        save_onnx_path = model_dir / f'{model_path.stem}.onnx'
        shell_str = f'paddle2onnx --model_dir {model_dir} ' \
                    '--model_filename inference.pdmodel ' \
                    '--params_filename inference.pdiparams ' \
                    f'--opset_version {self.opset} ' \
                    f'--save_file {save_onnx_path}'
        os.system(shell_str)
        print(f'Successfully convert model to {save_onnx_path}')

        if is_rec:
            self.write_dict_to_onnx(save_onnx_path, txt_url)
            print('The dict of recognition has been written to the onnx model.')

    def write_dict_to_onnx(self, model_path: str, txt_url: str):
        txt_path = download_file(txt_url, '.')
        character_dict = self.read_txt(txt_path)

        model = onnx.load_model(str(model_path))
        model = self.onnx_add_metadata(model, key='character',
                                       value=character_dict)
        onnx.save_model(model, str(model_path))
        txt_path.unlink()

    @staticmethod
    def read_txt(txt_path: str):
        with open(txt_path, 'r', -1, 'u8') as f:
            value = f.read()
        return value

    @staticmethod
    def onnx_add_metadata(model, key, value):
        meta = model.metadata_props.add()
        meta.key = key
        meta.value = value
        return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '--model_url', type=str,
                        help='The inference model url of paddleocr. e.g. https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar')
    parser.add_argument('-o', '--save_dir', type=str,
                        help='The directory of saving the model.')
    parser.add_argument('-txt_url', '--txt_url', type=str, default=None,
                        help='The raw txt url, if the model is recognition model.')
    args = parser.parse_args()

    converter = PaddleOCRModelConvert()

    converter(args.model_url, args.save_dir, args.txt_url)


if __name__ == '__main__':
    main()