#! /bin/bash
set -e errexit

function echoColor() {
    echo -e "\033[32m${1}\033[0m"
}


function download_model(){
    cd pretrained_models

    model_url=$1

    tar_name=${model_url##*/}
    model_dir=${tar_name%.*}
    if [ ! -d "${model_dir}" ]; then
        wget ${model_url}
        tar xf ${tar_name} && rm ${tar_name}
    fi

    cd ..

    echo ${model_dir}
}

#=============参数配置=============================
# 测试图像，用于比较转换前后是否一致
test_img_path="doc/imgs_words/ch/word_1.jpg"

model_url="https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar"

model_dir=$(download_model ${model_url})

# 下载好的推理模型地址
save_inference_path="pretrained_models/${model_dir}"

# 转换识别模型对应的字典
rec_char_dict_path="ppocr/utils/ppocr_keys_v1.txt"
#==============================================

save_onnx_path="convert_model/${model_dir}.onnx"

# inference → onnx
echoColor ">>> starting inference → onnx"
paddle2onnx --model_dir ${save_inference_path} \
            --model_filename inference.pdmodel \
            --params_filename inference.pdiparams \
            --save_file ${save_onnx_path} \
            --opset_version 12
echoColor ">>> finished converted"

# onnx → dynamic onnx
echoColor ">>> strarting change it to dynamic model"
python change_dynamic.py --onnx_path ${save_onnx_path} \
                         --type_model "rec"
echoColor ">>> finished converted"

# verity onnx
echoColor ">>> starting verity consistent"
python tools/infer/predict_rec.py --image_dir=${test_img_path} \
                                  --rec_model_dir=${save_inference_path} \
                                  --onnx_path ${save_onnx_path} \
                                  --rec_char_dict_path ${rec_char_dict_path} \
                                  --use_gpu False
echoColor ">>> finished converted"

echoColor ">>> The final model has been saved "${save_onnx_path}
