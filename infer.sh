#! /bin/bash
# @File: infer.sh
# @Time: 2021/07/17 16:10:30
set -e errexit

image_dir="doc/imgs_words_en/word_308.png"
rec_model_dir="pretrained_models/en_number_mobile_v2.0_rec_infer"
rec_char_dict_path="ppocr/utils/en_dict.txt"

python3 tools/infer/predict_rec.py --image_dir ${image_dir} \
                                   --rec_model_dir ${rec_model_dir} \
                                   --rec_char_dict_path ${rec_char_dict_path}