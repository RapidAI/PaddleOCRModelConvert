# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import os
from pathlib import Path
from typing import Union, Dict

import onnx

from .utils import download_file, is_http_url, unzip_file


class PaddleOCRModelConvert():
    def __init__(self) -> None:
        self.opset = 12

    def __call__(self, model_path: str,
                 save_dir: str, txt_path: str = None,
                 is_del_raw: bool = False) -> str:
        save_dir = str(save_dir)
        model_name = Path(model_path).stem
        is_rec = 'rec' in model_name
        if is_rec and not txt_path:
            raise ConvertError('Please give the txt url.')

        model_path = self.get_file_path(model_path, save_dir)

        # 解压模型
        model_dir = unzip_file(model_path, save_dir, is_del_raw=is_del_raw)

        # 转换模型
        save_onnx_path = model_dir / f'{Path(model_path).stem}.onnx'
        run_flag = self.convert_to_onnx(model_dir, save_onnx_path)
        if run_flag == 0:
            print(f'Successfully convert model to {save_onnx_path}')
        else:
            raise ConvertError('paddle2onnx convert failed!')

        try:
            self.change_to_dynamic(save_onnx_path)
        except Exception as e:
            raise ConvertError(
                'change the model to dynamic meets error.') from e

        if is_rec:
            txt_path = self.get_file_path(txt_path, '.')
            character_dict = self.read_txt(txt_path)
            self.write_dict_to_onnx(save_onnx_path, character_dict)
            print(
                'The dict of recognition has been written to the onnx model.')
        return save_onnx_path

    @staticmethod
    def get_file_path(file_path: str, save_dir: str) -> str:
        if is_http_url(file_path):
            file_path = download_file(file_path, save_dir)

        if not Path(file_path).exists():
            raise FileExistsError(f'{file_path} does not exist.')
        return file_path

    def convert_to_onnx(self, model_dir: str, save_onnx_path: str) -> int:
        shell_str = f'paddle2onnx --model_dir {model_dir} ' \
                    '--model_filename inference.pdmodel ' \
                    '--params_filename inference.pdiparams ' \
                    f'--opset_version {self.opset} ' \
                    f'--save_file {save_onnx_path}'
        run_flag = os.system(shell_str)
        return run_flag

    def change_to_dynamic(self, onnx_path: Union[str, Path]) -> None:
        onnx_path = str(onnx_path)
        onnx_model = onnx.load_model(onnx_path)
        dim_shapes = onnx_model.graph.input[0].type.tensor_type.shape.ListFields()[0][1]

        dynamic_name = 'DynamicDimension'
        if dynamic_name not in dim_shapes[0].dim_param:
            onnx_model.graph.input[0].type.tensor_type.shape.dim[0].dim_param = 'None'

        if dynamic_name not in dim_shapes[2].dim_param:
            onnx_model.graph.input[0].type.tensor_type.shape.dim[2].dim_param = '?'

        if dynamic_name not in dim_shapes[3].dim_param:
            onnx_model.graph.input[0].type.tensor_type.shape.dim[3].dim_param = '?'

        print('The model has change to dynamic inputs.')
        onnx.save(onnx_model, onnx_path)

    def write_dict_to_onnx(self, model_path: str, character_dict: Dict):
        model = onnx.load_model(str(model_path))
        model = self.onnx_add_metadata(model, key='character',
                                       value=character_dict)
        onnx.save_model(model, str(model_path))

    @staticmethod
    def read_txt(txt_path: Union[str, Path]) -> str:
        with open(str(txt_path), 'r', -1, 'u8') as f:
            value = f.read()
        return value

    @staticmethod
    def onnx_add_metadata(model, key, value):
        meta = model.metadata_props.add()
        meta.key = key
        meta.value = value
        return model


class ConvertError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--model_path', type=str,
                        help='The inference model url or local path of paddleocr. e.g. https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar or models/ch_PP-OCRv3_det_infer.tar')
    parser.add_argument('-o', '--save_dir', type=str,
                        help='The directory of saving the model.')
    parser.add_argument('-txt_path', '--txt_path', type=str, default=None,
                        help='The raw txt url, if the model is recognition model.')
    args = parser.parse_args()

    converter = PaddleOCRModelConvert()

    converter(args.model_path, args.save_dir, args.txt_url)


if __name__ == '__main__':
    main()
