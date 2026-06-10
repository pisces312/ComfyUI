# ComfyUI API 生成图片使用说明

## 服务地址
```
http://127.0.0.1:8188
```

## 启动服务

```bash
cd D:\workspace\ComfyUI
./venv/Scripts/python.exe main.py --listen --port 8188
```

或使用启动脚本：
```bash
./run_service.bat
```

## Python API 调用示例

ComfyUI 使用工作流（workflow）JSON 格式提交生成任务。

```python
import requests
import json
import time
from pathlib import Path

url = "http://127.0.0.1:8188"
client_id = "my_client"

# 1. 定义工作流（txt2img）
workflow = {
    "1": {
        "inputs": {"ckpt_name": "majicmixRealistic_v7.safetensors"},
        "class_type": "CheckpointLoaderSimple"
    },
    "2": {
        "inputs": {
            "text": "a cute cat sitting on a windowsill, sunlight, photorealistic",
            "clip": ["1", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "3": {
        "inputs": {
            "text": "blurry, low quality, distorted",
            "clip": ["1", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "4": {
        "inputs": {"width": 512, "height": 512, "batch_size": 1},
        "class_type": "EmptyLatentImage"
    },
    "5": {
        "inputs": {
            "seed": 42,
            "steps": 20,
            "cfg": 7,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1,
            "model": ["1", 0],
            "positive": ["2", 0],
            "negative": ["3", 0],
            "latent_image": ["4", 0]
        },
        "class_type": "KSampler"
    },
    "6": {
        "inputs": {"samples": ["5", 0], "vae": ["1", 2]},
        "class_type": "VAEDecode"
    },
    "7": {
        "inputs": {"filename_prefix": "output", "images": ["6", 0]},
        "class_type": "SaveImage"
    }
}

# 2. 提交任务
payload = {"prompt": workflow, "client_id": client_id}
r = requests.post(f"{url}/prompt", json=payload)
prompt_id = r.json()["prompt_id"]

# 3. 轮询结果
for i in range(120):
    r = requests.get(f"{url}/history/{prompt_id}")
    history = r.json()
    if prompt_id in history and history[prompt_id].get("outputs"):
        # 获取图片
        for node_id, output in history[prompt_id]["outputs"].items():
            if "images" in output:
                for img in output["images"]:
                    img_r = requests.get(
                        f"{url}/view?filename={img['filename']}&type=output"
                    )
                    output_path = Path(f"output/{img['filename']}")
                    output_path.write_bytes(img_r.content)
                    print(f"Saved: {output_path}")
        break
    time.sleep(5)
```

## 工作流节点说明

| 节点 | class_type | 说明 |
|------|-----------|------|
| 加载模型 | `CheckpointLoaderSimple` | 指定 `.safetensors` 文件名 |
| 正向提示词 | `CLIPTextEncode` | 连接 clip 输出 |
| 反向提示词 | `CLIPTextEncode` | 连接 clip 输出 |
| 空白潜空间 | `EmptyLatentImage` | 设置图片尺寸 |
| 采样器 | `KSampler` | 核心生成节点 |
| VAE解码 | `VAEDecode` | 潜空间转图片 |
| 保存图片 | `SaveImage` | 输出到 `output/` 目录 |

## 可用模型

通过 `extra_model_paths.yaml` 共享 WebUI 的模型， checkpoint 放在 WebUI 的 `models/Stable-diffusion/`：
- `majicmixRealistic_v7.safetensors`
- `sd_xl_base_1.0.safetensors`
- `v1-5-pruned-emaonly.safetensors`

## 获取系统信息

```python
# 查看 GPU 信息
requests.get(f"{url}/system_stats")

# 查看可用模型
requests.get(f"{url}/object_info/CheckpointLoaderSimple")
```

## 提示

- 工作流 JSON 可以从 ComfyUI 网页界面导出（菜单 → Save → API Format）
- 节点 ID 用字符串数字（"1", "2"...），输入引用格式为 `["节点ID", 输出索引]`
