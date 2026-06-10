# ComfyUI 问题排查记录

## 记录时间
2026-06-06

## 问题1：缺少核心依赖

**现象**：启动报错 `ModuleNotFoundError`
```
ModuleNotFoundError: No module named 'sqlalchemy'
ModuleNotFoundError: No module named 'yaml'
```

**原因**：新 clone 的 ComfyUI 项目，venv 只安装了 PyTorch，缺少其他运行时依赖。

**解决**：完整安装 requirements.txt
```bash
cd D:\workspace\ComfyUI
./venv/Scripts/pip.exe install -r requirements.txt
```

安装的依赖包括：
- sqlalchemy, alembic（数据库相关）
- pyyaml（配置解析）
- transformers, tokenizers（模型加载）
- aiohttp（Web 服务）
- comfyui-frontend-package（前端资源）
- 等等

---

## 问题2：模型目录共享配置

**配置**：通过 `extra_model_paths.yaml` 共享 WebUI Forge 的模型目录

**文件路径**：`D:\workspace\ComfyUI\extra_model_paths.yaml`

**内容**：
```yaml
webui_forge:
  base_path: D:\workspace\stable-diffusion-webui-forge/models/
  checkpoints: Stable-diffusion/
  embeddings: embeddings/
  lora: Lora/
  vae: VAE/
  controlnet: ControlNet/
```

**验证**：启动日志应显示
```
[INFO] Adding extra search path checkpoints D:\workspace\stable-diffusion-webui-forge\models\Stable-diffusion
```

---

## 当前稳定启动命令

```bash
cd D:\workspace\ComfyUI
./venv/Scripts/python.exe main.py --listen --port 8188
```

或使用启动脚本：
```bash
./run_service.bat
```

## 可用模型

通过 `extra_model_paths.yaml` 共享 WebUI 的模型，当前可用 checkpoint：
- `majicmixRealistic_v7.safetensors`
- `sd_xl_base_1.0.safetensors`
- `v1-5-pruned-emaonly.safetensors`
