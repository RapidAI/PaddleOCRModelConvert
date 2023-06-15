# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import List, Union

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
        try:
            self.convert_to_onnx(model_dir, save_onnx_path)
        except ConvertError as e:
            raise e
        else:
            print(f'Successfully convert model to {save_onnx_path}')

        try:
            self.change_to_dynamic(save_onnx_path)
        except Exception as e:
            raise ConvertError(
                'change the model to dynamic meets error.') from e

        if is_rec:
            txt_path = self.get_file_path(txt_path, '.')
            character_dict = self.read_txt(txt_path)
            self.write_dict_to_onnx(save_onnx_path, character_dict)

            if is_del_raw:
                txt_path.unlink()

            print(
                'The dict of recognition has been written to the onnx model.')
        return save_onnx_path

    @staticmethod
    def get_file_path(file_path: str, save_dir: str) -> str:
        """获得文件的本地路径，如果是url，则会自动下载到本地之后，再返回本地文件对应路径

        Args:
            file_path (str): url or 本地路径
            save_dir (str): 下载到本地的路径

        Raises:
            FileExistsError: 本地为存在该文件的异常

        Returns:
            str: 文件的本地路径
        """
        if is_http_url(file_path):
            file_path = download_file(file_path, save_dir)

        if not Path(file_path).exists():
            raise FileExistsError(f'{file_path} does not exist.')
        return file_path

    def convert_to_onnx(self, model_dir: str, save_onnx_path: str) -> None:
        """借助 :code:`paddle2onnx` 工具转换模型为onnx格式

        Args:
            model_dir (str): 保存paddle格式模型所在目录
            save_onnx_path (str): 保存的onnx全路径
        """
        shell_str = f'paddle2onnx --model_dir {model_dir} ' \
                    '--model_filename inference.pdmodel ' \
                    '--params_filename inference.pdiparams ' \
                    f'--opset_version {self.opset} ' \
                    f'--save_file {save_onnx_path}'
        with Popen(shell_str, stdout=PIPE, stderr=STDOUT, shell=True) as proc:
            run_log = [v.decode() for v in proc.stdout.readlines()]
            run_log = '\n'.join(run_log)

        # 通过日志中是否有failed字样，来确定是否转化成功
        failed_phrases = ['Failed to', 'parsing failed', 'convert failed']
        if self.is_contain(run_log, failed_phrases):
            raise ConvertError(run_log)

    def change_to_dynamic(self, onnx_path: Union[str, Path]) -> None:
        """更改onnx格式模型的指定为维度为动态输入

        Args:
            onnx_path (Union[str, Path]): onnx模型路径
        """
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

        print('The model has changed to dynamic inputs.')
        onnx.save(onnx_model, onnx_path)

    def write_dict_to_onnx(self, model_path: str, character_dict: str):
        """将文本识别模型对应的字典文件写入到onnx模型中

        Args:
            model_path (str): onnx模型路径
            character_dict (str): 字典列表
        """
        model = onnx.load_model(str(model_path))
        meta = model.metadata_props.add()
        meta.key = 'character'
        meta.value = character_dict
        onnx.save_model(model, str(model_path))

    @staticmethod
    def read_txt(txt_path: Union[str, Path]) -> str:
        """读取txt文件

        Args:
            txt_path (Union[str, Path]): 字典文件全路径

        Returns:
            str: 字典字符串
        """
        with open(str(txt_path), 'r', -1, 'u8') as f:
            value = f.read()
        return value

    @staticmethod
    def is_contain(sentence: str, key_words: Union[str, List],) -> bool:
        """sentences中是否包含key_words中任意一个"""
        return any(i in sentence for i in key_words)


class ConvertError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--model_path', type=str,
                        help='The inference model url or local path of paddleocr. e.g. https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar or models/ch_PP-OCRv3_det_infer.tar')
    parser.add_argument('-o', '--save_dir', type=str,
                        help='The directory of saving the model.')
    parser.add_argument('-txt_path', '--txt_path', type=str, default=None,
                        help='The raw txt url or local txt path, if the model is recognition model.')
    args = parser.parse_args()

    converter = PaddleOCRModelConvert()

    converter(args.model_path, args.save_dir, args.txt_path)


if __name__ == '__main__':
    main()
