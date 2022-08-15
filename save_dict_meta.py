# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse

import onnx


def read_txt(txt_path):
    with open(txt_path, 'r', -1, 'u8') as f:
        value = f.read()
    return value


def onnx_add_metadata(model, key, value):
    meta = model.metadata_props.add()
    meta.key = key
    meta.value = value
    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--onnx_path', type=str)
    parser.add_argument('--key_path', type=str)
    args = parser.parse_args()

    model = onnx.load_model(args.onnx_path)
    chars = read_txt(args.key_path)

    model = onnx_add_metadata(model, key='character', value=chars)
    onnx.save_model(model, args.onnx_path)
