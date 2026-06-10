# CLAUDE.md - ComfyUI 项目指南

## 项目概述

ComfyUI v0.24.0 — 模块化 AI 图像/视频/3D/音频生成引擎，基于节点图工作流界面。

- **仓库**: https://github.com/comfyanonymous/ComfyUI
- **Python**: 3.11 (venv)
- **框架**: PyTorch + aiohttp Web 服务
- **端口**: 8188

## 项目结构

```
ComfyUI/
├── main.py              # 入口，启动服务
├── server.py            # HTTP/WebSocket 服务
├── nodes.py             # 内置节点注册
├── execution.py         # 工作流执行引擎
├── folder_paths.py      # 模型/目录路径管理
├── comfy/               # 核心推理库（模型加载、采样器、VAE 等）
├── comfy_api/           # API 版本定义 & Feature Flags
├── comfy_api_nodes/     # 外部 API 节点（OpenAI、Gemini 等）
├── comfy_extras/        # 扩展节点（ControlNet、Flux、Wan 等）
├── comfy_execution/     # 执行缓存、任务队列、进度追踪
├── comfy_config/        # 配置解析
├── api_server/          # REST API 路由
├── app/                 # 前端管理、用户系统、模型管理
├── custom_nodes/        # 自定义节点（当前为空）
├── models/              # 模型文件目录
├── blueprints/          # 预置工作流模板 (JSON)
├── script_examples/     # API 调用示例脚本
├── input/               # 输入图片
├── output/              # 输出图片
├── docs/                # 使用文档
├── venv/                # Python 虚拟环境
└── extra_model_paths.yaml  # 外部模型路径（共享 WebUI Forge）
```

## 启动服务

```bash
cd D:\workspace\ComfyUI
.\venv\Scripts\python.exe main.py --listen --port 8188
```

或直接运行：
```bash
.\run_service.bat
```

启动后访问: http://127.0.0.1:8188

### 常用启动参数

| 参数 | 说明 |
|------|------|
| `--listen [IP]` | 监听地址，默认 127.0.0.1；不带参数则 0.0.0.0 |
| `--port 8188` | 监听端口 |
| `--cpu` | 强制 CPU 推理（慢） |
| `--lowvram` / `--novram` | 低显存模式 |
| `--preview-method taesd` | 高质量潜空间预览 |
| `--auto-launch` | 启动后自动打开浏览器 |
| `--enable-manager` | 启用 ComfyUI-Manager |
| `--disable-api-nodes` | 禁用外部 API 节点 |
| `--force-fp16` / `--force-fp32` | 强制精度 |
| `--verbose DEBUG` | 详细日志 |

## 模型管理

- **本地模型**: `models/` 下各子目录（checkpoints、loras、vae 等）
- **共享模型**: `extra_model_paths.yaml` 配置了 WebUI Forge 的模型目录
  - Checkpoints 来自: `D:\workspace\stable-diffusion-webui-forge\models\Stable-diffusion\`
- 当前可用 checkpoint: `majicmixRealistic_v7.safetensors`、`sd_xl_base_1.0.safetensors`、`v1-5-pruned-emaonly.safetensors`

## API 调用

ComfyUI 通过 HTTP API 提交工作流 JSON 进行任务生成。

- `POST /prompt` — 提交工作流
- `GET /history/{prompt_id}` — 查询任务结果
- `GET /view?filename=xxx&type=output` — 获取输出图片
- `GET /system_stats` — GPU/系统状态
- `GET /object_info/{node_class}` — 节点参数信息

详见: `docs/api-usage-guide.md`

## 开发注意事项

- 工作流 JSON 中节点 ID 为字符串数字（"1", "2"...），输入引用格式 `["节点ID", 输出索引]`
- 工作流可从 Web UI 导出（菜单 → Save → API Format）
- `custom_nodes/` 目录当前为空，可安装 ComfyUI-Manager 管理
- Python 依赖: `requirements.txt`，Manager 依赖: `manager_requirements.txt`
- venv 位于项目内 `venv/`，Python 3.11

## 依赖安装（如需重建）

```bash
.\venv\Scripts\pip.exe install -r requirements.txt
```
