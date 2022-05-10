#! /bin/bash
set -e errexit

function echoColor() {
    echo -e "\033[32m${1}\033[0m"
}

#=============参数配置===========================
# 测试图像，用于比较转换前后是否一致
test_img_path="doc/imgs_words_en/word_10.png"

# 转换模型对应的配置文件
yml_path="configs/rec/multi_language/rec_en_number_lite_train.yml"

# 原始预训练模型
raw_model_path="pretrained_models/ch_ppocr_mobile_v2.0_rec_pre/best_accuracy"

# 转换识别模型对应的字典
rec_char_dict_path="ppocr/utils/en_dict.txt"
#==============================================

save_infer_name=${raw_model_path#*/}
save_infer_name=${save_infer_name%/*}
save_inference_path="pretrained_models/${save_infer_name}"
save_onnx_path="convert_model/${save_inference_path##*/}.onnx"

# raw → inference
echoColor ">>> starting raw model → inference"
python3 tools/export_model.py -c ${yml_path} -o Global.pretrained_model=${raw_model_path} Global.load_static_weights=False Global.save_inference_dir=${save_inference_path}
echoColor ">>> finished converted"

# inference → onnx
echoColor ">>> starting inference → onnx"
paddle2onnx --model_dir ${save_inference_path} \
            --model_filename inference.pdmodel \
            --params_filename inference.pdiparams \
            --save_file ${save_onnx_path} \
            --opset_version 10
echoColor ">>> finished converted"

# onnx → dynamic onnx
echoColor ">>> strarting change it to dynamic model"
python rec_change_dynamic.py --onnx_path ${save_onnx_path} \
                             --type_model rec
echoColor ">>> finished converted"

# verity onnx
echoColor ">>> starting verity consistent"
python tools/infer/predict_rec_vertify_same.py --image_dir=${test_img_path} \
                                               --rec_model_dir=${save_inference_path} \
                                               --onnx_path ${save_onnx_path} \
                                               --use_gpu False
echoColor ">>> finished converted"

echoColor ">>> The final model has been saved "${save_onnx_path}