- [ ] 商店安装22

- NVIDIA-SMI 566.03   ，**566.14**？
- CUDA Version: 12.7  
- GeForce RTX 3060 
  - nvcr.io/nvidia/pytorch:21.02-py3       19.2GB 
- T032
- triton cpu

[Triton 概念指南（Part 1）：如何部署模型推理服务？ - 知乎](https://zhuanlan.zhihu.com/p/660990715)

- https://arxiv.org/pdf/1704.03155v2.pdf
- https://docs.opencv.org/4.x/db/da4/samples_2dnn_2text_detection_8cpp-example.html
- [GitHub - clovaai/deep-text-recognition-benchmark: Text recognition (optical character recognition) with deep learning methods, ICCV 2019](https://github.com/clovaai/deep-text-recognition-benchmark)
- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html
- 
- https://youtu.be/JgP2WgNIq_w
- [GitHub - aws-samples/amazon-eks-scaling-with-keda-and-karpenter](https://github.com/aws-samples/amazon-eks-scaling-with-keda-and-karpenter)
- [GitHub - aws-samples/amazon-eks-scaling-with-keda-and-karpenter](https://github.com/aws-samples/amazon-eks-scaling-with-keda-and-karpenter)
- [client/src/python/examples at main · triton-inference-server/client · GitHub](https://github.com/triton-inference-server/client/tree/main/src/python/examples)
- [GitHub - triton-inference-server/backend: Common source, scripts and utilities for creating Triton backends.](https://github.com/triton-inference-server/backend#where-can-i-find-all-the-backends-that-are-available-for-triton)

安装桌面版本docker 打开交互？

```bash
wsl --set-version Ubuntu-22.04 2

wsl -d  Ubuntu-22.04

https://netron.app/

# 查询
docker login nvcr.io
$oauthtoken
docker run --gpus all nvcr.io/nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi

# 移除 --gpus 参数
# 以PyTorch镜像为例，尝试在CPU模式下进入bash
docker run --rm -it \
  --runtime=runc \           # 强制使用普通容器运行时
  -e CUDA_VISIBLE_DEVICES="" \ # 清空此变量，告知容器“看不到GPU”
  nvcr.io/nvidia/pytorch:24.07-py3 \
  bash

python -c "import torch;print(torch.cuda.is_available())

cd /mnt/c/home/yann/tech_sum/deploy/triton
git clone https://github.com/triton-inference-server/tutorials.git
cd Conceptual_Guide/Part_1-model_deployment
wget https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz
tar -xvf frozen_east_text_detection.tar.gz
docker run -it --gpus all -v ${PWD}:/workspace nvcr.io/nvidia/tensorflow:21.03-tf2-py3

pip install -U tf2onnx
python -m tf2onnx.convert --input frozen_east_text_detection.pb --inputs "input_images:0" --outputs "feature_fusion/Conv_7/Sigmoid:0","feature_fusion/concat_3:0" --output detection.onnx

wget https://www.dropbox.com/sh/j3xmli4di1zuv3s/AABzCC1KGbIRe2wRwa3diWKwa/None-ResNet-None-CTC.pth

docker run -it --gpus all -v ${PWD}:/workspace nvcr.io/nvidia/pytorch:21.02-py3

```

~~~python
import torch
from utils.model import STRModel


# Create PyTorch Model Object
model = STRModel(input_channels=1, output_channels=512, num_classes=37)

# Load model weights from external file
state = torch.load("None-ResNet-None-CTC.pth")
state = {key.replace("module.", ""): value for key, value in state.items()}
model.load_state_dict(state)

# Create ONNX file by tracing model
trace_input = torch.randn(1, 1, 32, 100)
torch.onnx.export(model, trace_input, "str.onnx", verbose=True)
~~~

~~~bash
mkdir -p model_repository/text_detection/1
mv detection.onnx model_repository/text_detection/1/model.onnx
# 配置文件失败一次

docker run --gpus=all -it --shm-size=256m --rm -p8000:8000 -p8001:8001 -p8002:8002 -v $(pwd)/model_repository:/models nvcr.io/nvidia/tritonserver:21.10-py3
tritonserver --model-repository=/models --log-verbose=1


#config
max_batch_size: 0 # t_d
python3 -c "import onnx; m = onnx.load('/models/text_recognition/1/model.onnx'); [o.name for o in m.graph.output]"  #307

~~~



~~~bash
https://github.com/triton-inference-server/client#client-library-apis
curl -v localhost:8000/v2/health/live
curl -v localhost:8000/v2/health/ready	
curl localhost:8000/v2/models/text_detection
curl localhost:8000/v2/models/text_recognition
curl localhost:8000/v2/models #?
curl localhost:8000/v2/models/text_recognition

curl -X POST localhost:8000/v2/models/text_recognition/infer   -H "Content-Type: application/json"   -d '{
    "inputs": [{
      "name": "input.1",
      "shape": [1, 1, 32, 100],
      "datatype": "FP32",
      "data": '"$(python3 -c "import numpy as np; print((np.random.randn(1*1*32*100) * 127).astype(np.float32).tolist())")"'
    }],
    "outputs": [{"name": "307"}]
  }'
  
pip install tritonclient[http] opencv-python-headless
python client.py
~~~







~~~python
import numpy as np
import cv2
import tritonclient.http as httpclient
from tritonclient.http import InferenceServerClient, InferInput, InferRequestedOutput
from typing import Tuple, List

def detection_preprocessing(image: cv2.Mat, target_size: Tuple[int, int] = (1024, 1024)) -> Tuple[np.ndarray, Tuple]:
    """
    对输入图像进行检测模型的预处理。
    包括：调整大小、归一化、转换为模型输入格式 (Batch, Height, Width, Channel)。
    """
    orig_h, orig_w = image.shape[:2]
    target_w, target_h = target_size

    # 1. 等比例缩放图像
    scale = min(target_w / orig_w, target_h / orig_h)
    new_w, new_h = int(orig_w * scale), int(orig_h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # 2. 将图像填充到目标尺寸
    padded = np.full((target_h, target_w, 3), 114, dtype=np.uint8)
    padded[:new_h, :new_w, :] = resized

    # 3. 归一化：减去均值（根据模型训练设定调整，此处为示例）
    mean = np.array([123.68, 116.78, 103.94], dtype=np.float32)
    normalized = padded.astype(np.float32) - mean

    # 4. 转换为模型所需的 NHWC 格式并增加批次维度
    # 即从 (H, W, C) -> (1, H, W, C)
    blob = np.expand_dims(normalized, axis=0)

    # 返回预处理后的张量及原始图像信息用于后处理还原坐标
    return blob, (orig_h, orig_w, scale)

def detection_postprocessing(scores: np.ndarray,
                             geometry: np.ndarray,
                             orig_info: Tuple,
                             score_threshold: float = 0.5) -> List[List[int]]:
    """
    处理检测模型的输出，生成文本边界框列表。
    基于EAST等文本检测器的后处理方法。
    scores: 置信度图，形状 (1, H, W, 1)
    geometry: 几何图，形状 (1, H, W, 5)
    orig_info: (原始高度, 原始宽度, 缩放比例)
    """
    orig_h, orig_w, scale = orig_info
    scores = scores[0, :, :, 0]  # 移除批次和通道维度
    geometry = geometry[0, :, :, :]  # 移除批次维度

    # 1. 根据置信度阈值获取候选框位置
    (y_coords, x_coords) = np.where(scores >= score_threshold)
    boxes = []
    confidences = []

    for y, x in zip(y_coords, x_coords):
        score = scores[y, x]
        geo_data = geometry[y, x]

        # 2. 解析几何信息（假设为5个值: dx1, dy1, dx2, dy2, angle）
        dx1, dy1, dx2, dy2, angle = geo_data

        # 3. 计算旋转框的角点（简化版，忽略旋转）
        offset_x, offset_y = x * 4.0, y * 4.0  # 特征图到原图的偏移
        x1 = int(offset_x - dx1)
        y1 = int(offset_y - dy1)
        x2 = int(offset_x + dx2)
        y2 = int(offset_y + dy2)

        # 4. 将坐标映射回原始图像尺寸
        x1, y1, x2, y2 = [int(coord / scale) for coord in [x1, y1, x2, y2]]
        boxes.append([x1, y1, x2, y2])
        confidences.append(float(score))

    # 5. 应用非极大值抑制 (NMS) 合并重叠框
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, 0.3)
    final_boxes = []
    if len(indices) > 0:
        for i in indices.flatten():
            final_boxes.append(boxes[i])

    return final_boxes

def crop_and_align_region(image: cv2.Mat, box: List[int], target_height: int = 32) -> np.ndarray:
    """
    根据检测框裁剪图像，并将裁剪区域调整为识别模型所需尺寸。
    """
    x1, y1, x2, y2 = box
    # 确保坐标在图像范围内
    h, w = image.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    text_region = image[y1:y2, x1:x2]
    if text_region.size == 0:
        return None

    # 转换为灰度图
    if len(text_region.shape) == 3:
        gray = cv2.cvtColor(text_region, cv2.COLOR_BGR2GRAY)
    else:
        gray = text_region

    # 调整高度到固定值，保持宽高比
    region_h, region_w = gray.shape
    r = target_height / float(region_h)
    new_w = int(region_w * r)
    resized = cv2.resize(gray, (new_w, target_height), interpolation=cv2.INTER_LINEAR)

    # 填充宽度到模型固定输入（根据你的模型输入，例如100）
    target_width = 100
    padded = np.full((target_height, target_width), 114, dtype=np.float32)
    if new_w <= target_width:
        padded[:, :new_w] = resized
    else:
        # 如果过宽，则从右侧裁剪
        padded[:, :] = resized[:, :target_width]

    # 归一化并调整维度顺序为 (1, 1, H, W) 即 (Batch, Channel, Height, Width)
    normalized = (padded.astype(np.float32) - 127.5) / 127.5
    blob = np.expand_dims(normalized, axis=0)  # 增加批次维度 -> (1, H, W)
    blob = np.expand_dims(blob, axis=0)        # 增加通道维度 -> (1, 1, H, W)

    return blob

def recognition_postprocessing(scores: np.ndarray, 
                               character_list: str = "0123456789abcdefghijklmnopqrstuvwxyz") -> str:
    """
    处理识别模型的输出，将概率序列解码为文本字符串。
    使用连接时序分类 (CTC) 的贪婪解码（简化版）。
    """
    # scores 形状假设为 (batch, sequence_length, num_classes)
    probs = scores[0] if len(scores.shape) == 3 else scores

    # 1. 获取每个时间步的最大概率索引
    pred_indices = np.argmax(probs, axis=-1)

    # 2. 合并重复字符
    merged = []
    prev_idx = -1
    for idx in pred_indices:
        if idx != prev_idx and idx < len(character_list):
            merged.append(character_list[idx])
        prev_idx = idx

    # 3. 移除空白字符（如果字符集包含空白符，通常是最后一个）
    # 简单实现：直接拼接
    text = ''.join(merged)
    return text

def main():
    # 1. 初始化客户端
    client = InferenceServerClient(url="localhost:8000")

    # 2. 加载测试图像
    image_path = "test_image.jpg"  # 请替换为你的测试图片路径
    image = cv2.imread(image_path)
    if image is None:
        print(f"错误：无法加载图像 {image_path}")
        return

    print("步骤1: 文本检测预处理...")
    # 3. 检测预处理
    blob, orig_info = detection_preprocessing(image)
    print(f"预处理后图像形状: {blob.shape}")

    # 4. 准备检测模型输入输出
    detection_input = InferInput("input_images:0", blob.shape, "FP32")
    detection_input.set_data_from_numpy(blob)

    detection_outputs = [
        InferRequestedOutput("feature_fusion/Conv_7/Sigmoid:0"),
        InferRequestedOutput("feature_fusion/concat_3:0")
    ]

    print("步骤2: 发送检测推理请求...")
    # 5. 发送检测推理请求
    detection_result = client.infer(
        model_name="text_detection",
        inputs=[detection_input],
        outputs=detection_outputs
    )

    # 6. 获取检测输出
    scores = detection_result.as_numpy("feature_fusion/Conv_7/Sigmoid:0")
    geometry = detection_result.as_numpy("feature_fusion/concat_3:0")

    print("步骤3: 检测后处理，生成文本框...")
    # 7. 检测后处理
    boxes = detection_postprocessing(scores, geometry, orig_info)
    print(f"检测到 {len(boxes)} 个文本区域")

    if len(boxes) == 0:
        print("未检测到文本，流程结束。")
        return

    all_texts = []
    # 8. 对每个检测框进行文本识别
    for i, box in enumerate(boxes):
        print(f"  处理区域 {i+1}/{len(boxes)}: 坐标{box}...")

        # 8.1 裁剪并预处理识别区域
        recognition_input_blob = crop_and_align_region(image, box)
        if recognition_input_blob is None:
            all_texts.append("")
            continue

        # 8.2 准备识别模型输入输出
        # **注意**：下面的输入输出名称 `INPUT__0` 和 `OUTPUT__0` 是示例
        # 你必须替换为你的 `text_recognition` 模型的实际输入输出名称！
        recognition_input = InferInput("INPUT__0", recognition_input_blob.shape, "FP32")
        recognition_input.set_data_from_numpy(recognition_input_blob)

        recognition_output = InferRequestedOutput("OUTPUT__0")

        # 8.3 发送识别推理请求
        recognition_result = client.infer(
            model_name="text_recognition",
            inputs=[recognition_input],
            outputs=[recognition_output]
        )

        # 8.4 识别后处理
        rec_scores = recognition_result.as_numpy("OUTPUT__0")
        text = recognition_postprocessing(rec_scores)
        all_texts.append(text)
        print(f"    识别结果: '{text}'")

    # 9. 输出最终结果
    print("\n" + "="*20 + " OCR 最终结果 " + "="*20)
    for i, (box, text) in enumerate(zip(boxes, all_texts)):
        print(f"文本区域 {i+1}: 坐标{box} -> '{text}'")

    # 10. 可选：可视化结果并保存
    result_image = image.copy()
    for box, text in zip(boxes, all_texts):
        x1, y1, x2, y2 = box
        cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(result_image, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imwrite("ocr_result.jpg", result_image)
    print("结果已可视化并保存到 'ocr_result.jpg'")

if __name__ == "__main__":
    main()
    
~~~

~~~bash
# 修正后的代码
recognition_input = InferInput("input.1", recognition_input_blob.shape, "FP32")  # 输入名
recognition_input.set_data_from_numpy(recognition_input_blob)
recognition_output = InferRequestedOutput("307")  # 输出名
...
recognition_result = client.infer(model_name="text_recognition", ...)
rec_scores = recognition_result.as_numpy("307")  # 输出名


~~~

