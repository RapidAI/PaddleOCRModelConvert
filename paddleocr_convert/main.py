# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import Optional, Union

import onnx

from .utils import (
    InputType,
    Logger,
    download_file,
    is_contain,
    is_http_url,
    read_txt,
    unzip_file,
)


class PaddleOCRModelConvert:
    def __init__(self) -> None:
        self.opset = 14
        self.logger = Logger(logger_name=__name__).get_log()

    def __call__(
        self,
        model_url: str,
        save_dir: InputType,
        txt_path: Optional[str] = None,
        is_del_raw: bool = False,
        is_rec: Optional[bool] = None,
    ) -> str:
        model_name = Path(model_url).stem

        if is_rec is None:
            is_rec = "rec" in model_name

        if is_rec and not txt_path:
            raise ConvertError("Please give the txt url.")

        model_file_path = self.get_file_path(model_url, save_dir)
        unzip_result = unzip_file(model_file_path, save_dir, is_del_raw=is_del_raw)

        save_onnx_path = (
            Path(unzip_result.get("model_dir", "")).parent / f"{model_name}.onnx"
        )
        try:
            self.convert_to_onnx(unzip_result, save_onnx_path)
        except ConvertError as e:
            raise e

        self.logger.info(f"Successfully convert model to {save_onnx_path}")

        try:
            self.change_to_dynamic(save_onnx_path)
        except Exception as e:
            raise ConvertError("change the model to dynamic meets error.") from e

        if is_rec:
            txt_path = self.get_file_path(txt_path, ".")
            character_dict = read_txt(txt_path)
            self.write_dict_to_onnx(save_onnx_path, character_dict)

            if is_del_raw:
                txt_path.unlink()

            self.logger.info(
                "The dict of recognition has been written to the onnx model."
            )
        return str(save_onnx_path)

    @staticmethod
    def get_file_path(file_path: str, save_dir: InputType) -> str:
        """获得文件的本地路径，如果是url，则会自动下载到本地之后，再返回本地文件对应路径

        Args:
            file_path (str): url or 本地路径
            save_dir (InputType): 下载到本地的路径

        Raises:
            FileExistsError: 本地为存在该文件的异常

        Returns:
            str: 文件的本地路径
        """
        if is_http_url(file_path):
            file_path = download_file(str(file_path), save_dir)

        if not Path(file_path).exists():
            raise FileExistsError(f"{file_path} does not exist.")
        return file_path

    def convert_to_onnx(self, unzip_result: object, save_onnx_path: Path) -> None:
        """借助 :code:`paddle2onnx` 工具转换模型为onnx格式

        Args:
            unzip_result (object):
                - model_dir (Path): 解压后模型保存路径。
                - my_files (set): 解压得到的文件名集合。
            save_onnx_path (Path): 保存的onnx全路径
        """
        model_dir = unzip_result.get("model_dir", "")
        my_files = unzip_result.get("my_files", {})
        model_filename = (
            "inference.json" if "inference.json" in my_files else "inference.pdmodel"
        )
        shell_str = (
            f"paddle2onnx --model_dir {model_dir} "
            f"--model_filename {model_filename} "
            "--params_filename inference.pdiparams "
            f"--opset_version {self.opset} "
            f"--save_file {save_onnx_path}"
        )
        with Popen(shell_str, stdout=PIPE, stderr=STDOUT, shell=True) as proc:
            run_log = "\n".join([v.decode() for v in proc.stdout.readlines()])

        failed_phrases = ["Failed to", "parsing failed", "convert failed", "Oops"]
        if is_contain(run_log, failed_phrases) or not save_onnx_path.exists():
            raise ConvertError(run_log)

    def change_to_dynamic(self, onnx_path: Union[str, Path]) -> None:
        """更改onnx格式模型的指定为维度为动态输入

        Args:
            onnx_path (Union[str, Path]): onnx模型路径
        """
        onnx_path = str(onnx_path)
        onnx_model = onnx.load_model(onnx_path)
        dim_shapes = onnx_model.graph.input[0].type.tensor_type.shape.ListFields()[0][1]

        dynamic_name = "DynamicDimension"
        if dynamic_name not in dim_shapes[0].dim_param:
            onnx_model.graph.input[0].type.tensor_type.shape.dim[0].dim_param = "None"

        if dynamic_name not in dim_shapes[2].dim_param:
            onnx_model.graph.input[0].type.tensor_type.shape.dim[2].dim_param = "?"

        if dynamic_name not in dim_shapes[3].dim_param:
            onnx_model.graph.input[0].type.tensor_type.shape.dim[3].dim_param = "?"

        self.logger.info("The model has changed to dynamic inputs.")
        onnx.save(onnx_model, onnx_path)

    def write_dict_to_onnx(self, model_path: Union[str, Path], character_dict: str):
        """将文本识别模型对应的字典文件写入到onnx模型中

        Args:
            model_path (str): onnx模型路径
            character_dict (str): 字典列表
        """
        model = onnx.load_model(str(model_path))
        meta = model.metadata_props.add()
        meta.key = "character"
        meta.value = character_dict
        onnx.save_model(model, str(model_path))


class ConvertError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--model_path",
        type=str,
        help="The inference model url or local path of paddleocr. e.g. https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar or models/ch_PP-OCRv3_det_infer.tar",
    )
    parser.add_argument(
        "-o", "--save_dir", type=str, help="The directory of saving the model."
    )
    parser.add_argument(
        "-txt_path",
        "--txt_path",
        type=str,
        default=None,
        help="The raw txt url or local txt path, if the model is recognition model.",
    )
    args = parser.parse_args()

    converter = PaddleOCRModelConvert()
    converter(args.model_path, args.save_dir, args.txt_path)


if __name__ == "__main__":
    main()
