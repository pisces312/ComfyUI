# ComfyUI 服务启动与使用指南

## 1. 启动服务

### 方式一：启动脚本（推荐）

```bash
cd D:\workspace\ComfyUI
.\run_service.bat
```

### 方式二：命令行启动

```bash
cd D:\workspace\ComfyUI
.\venv\Scripts\python.exe main.py --listen --port 8188
```

启动成功后控制台输出：
```
Starting server
To see the GUI go to: http://127.0.0.1:8188
```

浏览器打开 http://127.0.0.1:8188 即可使用 Web UI。

### 方式三：带 Manager 启动

```bash
.\venv\Scripts\python.exe main.py --listen --port 8188 --enable-manager
```

> 注意：首次使用 Manager 需先安装依赖：`.\venv\Scripts\pip.exe install -r manager_requirements.txt`

## 2. 常用启动参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--listen [IP]` | 127.0.0.1 | 监听地址。不带参数则监听所有接口 (0.0.0.0) |
| `--port PORT` | 8188 | 监听端口 |
| `--auto-launch` | 关 | 启动后自动打开浏览器 |
| `--cpu` | 关 | 使用 CPU 推理（非常慢） |
| `--lowvram` | 关 | 低显存模式，文本编码器跑 CPU |
| `--novram` | 关 | 极低显存模式 |
| `--highvram` | 关 | 模型常驻 GPU |
| `--preview-method auto\|taesd\|latent2rgb\|none` | none | 潜空间预览方式 |
| `--force-fp16` / `--force-fp32` | 自动 | 强制计算精度 |
| `--fp16-vae` / `--fp32-vae` / `--bf16-vae` | 自动 | VAE 精度 |
| `--enable-manager` | 关 | 启用 ComfyUI-Manager |
| `--disable-api-nodes` | 关 | 禁用外部 API 节点 |
| `--verbose DEBUG` | INFO | 日志级别 |
| `--cuda-device ID` | 全部 | 指定 CUDA 设备 |
| `--extra-model-paths-config PATH` | 无 | 额外模型路径配置文件 |

## 3. 停止服务

在运行窗口按 `Ctrl+C` 即可。

## 4. Web UI 基本操作

1. **加载工作流**：拖拽 JSON 文件到页面，或菜单 → Load
2. **添加节点**：双击空白处搜索节点名
3. **连线**：从节点输出端口拖拽到另一节点输入端口
4. **运行**：`Ctrl+Enter` 或点击 Queue Prompt
5. **查看输出**：生成的图片显示在 SaveImage 节点，保存到 `output/` 目录

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Enter` | 执行当前工作流 |
| `Ctrl+Shift+Enter` | 优先执行 |
| `Ctrl+Alt+Enter` | 取消当前生成 |
| `Ctrl+S` | 保存工作流 |
| `Ctrl+O` | 加载工作流 |
| `Space+拖拽` | 画布平移 |
| 双击空白 | 搜索添加节点 |
| `Ctrl+Z/Y` | 撤销/重做 |

## 5. 模型文件

### 目录结构

```
models/
├── checkpoints/        # 主模型 (.safetensors, .ckpt)
├── loras/              # LoRA 微调
├── vae/                # VAE 模型
├── controlnet/         # ControlNet 模型
├── clip/               # CLIP 文本编码器
├── clip_vision/        # CLIP Vision 模型
├── embeddings/         # Textual Inversion
├── upscale_models/     # 超分模型 (ESRGAN 等)
├── diffusion_models/   # 独立扩散模型
├── style_models/       # 风格模型
└── vae_approx/         # TAESD 预览解码器
```

### 共享外部模型

通过 `extra_model_paths.yaml` 共享 WebUI Forge 的模型：

```yaml
webui_forge:
  base_path: D:\workspace\stable-diffusion-webui-forge/models/
  checkpoints: Stable-diffusion/
  embeddings: embeddings/
  lora: Lora/
  vae: VAE/
  controlnet: ControlNet/
```

当前可用 Checkpoint：
- `majicmixRealistic_v7.safetensors`
- `sd_xl_base_1.0.safetensors`
- `v1-5-pruned-emaonly.safetensors`

### Template 与模型路径

Template 创建的 workflow 会硬编码默认模型文件名（如 `DreamShaper_8_pruned.safetensors`），但 ComfyUI 的 `CheckpointLoaderSimple` 节点会自动扫描所有配置的模型路径（包括 `extra_model_paths.yaml` 中的外部路径），在下拉框中合并显示所有可用模型。

**操作方式**：在界面中点击 Checkpoint 节点的 `ckpt_name` 下拉框，直接选择外部路径中的模型即可。如果想改变 workflow 的默认模型，修改后重新 Save 即可覆盖。

**Workflow 保存位置**：`D:\workspace\ComfyUI\user\default\workflows\`

## 6. API 调用

详见 [api-usage-guide.md](api-usage-guide.md)

核心流程：
1. `POST /prompt` 提交工作流 JSON
2. 轮询 `GET /history/{prompt_id}` 等待完成
3. `GET /view?filename=xxx&type=output` 获取结果图片

## 7. 常见问题

| 问题 | 解决方案 |
|------|----------|
| `ModuleNotFoundError` | 安装依赖：`.\venv\Scripts\pip.exe install -r requirements.txt` |
| 黑色输出图片 | 尝试 `--fp32-vae` |
| 显存不足 | 尝试 `--lowvram` 或 `--novram` |
| CUDA 错误 | 尝试 `--disable-cuda-malloc` |
| 模型找不到 | 检查 `extra_model_paths.yaml` 配置和文件名 |
| 显存不足 (OOM) | 加 `--lowvram` 或 `--novram` 启动参数 |

## 8. Image-to-Video 显存参考

| 模型 | 最低显存 | 推荐显存 | 8GB 可行性 |
|------|---------|---------|-----------|
| AnimateDiff (SD1.5) | 6-8 GB | 8-12 GB | ✅ 可以 |
| SVD (Stable Video Diffusion) | 8 GB | 12-16 GB | ⚠️ 需 `--lowvram` |
| CogVideoX-2B | 8 GB | 12 GB | ⚠️ 体验一般 |
| CogVideoX-5B | 12 GB | 16-24 GB | ❌ 不够 |
| Wan2.1-I2V | 12 GB | 16-24 GB | ❌ 不够 |
| HunyuanVideo | 16 GB | 24+ GB | ❌ 不够 |

> RTX 5060 8GB 推荐 AnimateDiff，显存吃紧时加 `--lowvram` 启动。
