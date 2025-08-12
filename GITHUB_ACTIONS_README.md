# GitHub Actions 使用说明

本文档说明如何使用GitHub Actions来自动构建和发布文件下载重命名工具。

## 工作流概览

项目包含以下GitHub Actions工作流：

### 1. CI 工作流 (`.github/workflows/ci.yml`)

**触发条件**: 推送到主分支或创建PR时
**功能**: 
- 跨平台测试 (Windows, macOS, Linux)
- 代码质量检查 (linting)
- 安全漏洞扫描
- 代码覆盖率报告

### 2. 构建工作流 (`.github/workflows/build.yml`)

**触发条件**: 推送到主分支或创建PR时
**功能**:
- 构建Windows可执行文件 (.exe)
- 构建macOS应用程序包 (.app)
- 构建Linux可执行文件
- 上传构建产物

### 3. 发布工作流 (`.github/workflows/release.yml`)

**触发条件**: 推送版本标签 (如 `v1.0.0`)
**功能**:
- 自动构建所有平台的应用程序
- 创建GitHub Release
- 上传构建产物到Release页面

## 使用方法

### 自动构建和发布

1. **推送代码到主分支**
   ```bash
   git add .
   git commit -m "更新功能"
   git push origin main
   ```
   - 自动触发CI工作流
   - 自动触发构建工作流

2. **创建版本发布**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   - 自动触发发布工作流
   - 创建GitHub Release
   - 生成可下载的应用程序

### 手动触发构建

1. 在GitHub仓库页面，点击 "Actions" 标签
2. 选择 "Build and Package Application" 工作流
3. 点击 "Run workflow" 按钮
4. 选择分支和Python版本
5. 点击 "Run workflow" 开始构建

## 构建产物

### Windows
- 文件: `download_rename_app.exe`
- 位置: `dist/download_rename_app.exe`
- 特点: 单文件可执行程序，无需安装

### macOS
- 文件: `download_rename_app.app`
- 位置: `dist/download_rename_app.app`
- 特点: 标准的macOS应用程序包

### Linux
- 文件: `download_rename_app`
- 位置: `dist/download_rename_app`
- 特点: 单文件可执行程序

## 本地构建

### 使用构建脚本

```bash
# 运行本地构建脚本
python build.py

# 或使用构建配置工具
python build_config.py
```

### 手动构建

```bash
# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 构建应用程序
pyinstaller --onefile --windowed download_rename_app.py
```

## 配置说明

### 环境变量

工作流使用以下环境变量：
- `GITHUB_TOKEN`: 自动提供，用于GitHub API访问
- `PYTHON_VERSION`: 构建使用的Python版本

### 依赖管理

- 主要依赖: `requirements.txt`
- 构建依赖: `pyproject.toml` 中的 `build` 组
- 开发依赖: `pyproject.toml` 中的 `dev` 组

### 构建配置

- PyInstaller配置: `download_rename_app.spec`
- 应用程序元数据: `pyproject.toml`
- 构建脚本: `build.py`, `build_config.py`

## 故障排除

### 常见问题

1. **构建失败**
   - 检查依赖是否正确安装
   - 查看工作流日志中的错误信息
   - 确保Python版本兼容性

2. **文件过大**
   - 使用 `--onefile` 选项减少文件数量
   - 排除不必要的模块
   - 使用UPX压缩（已启用）

3. **权限问题**
   - 确保GitHub Actions有足够权限
   - 检查仓库设置中的Actions权限

### 调试技巧

1. **查看工作流日志**
   - 在Actions页面点击具体的工作流运行
   - 查看每个步骤的详细日志

2. **本地测试**
   - 使用本地构建脚本测试
   - 在本地环境中复现问题

3. **逐步调试**
   - 简化工作流配置
   - 逐个测试各个步骤

## 自定义配置

### 修改构建参数

编辑 `.github/workflows/` 下的工作流文件：

```yaml
# 修改Python版本
python-version: [3.9, 3.10, 3.11]

# 修改操作系统
os: [windows-latest, macos-latest, ubuntu-latest]

# 修改构建选项
pyinstaller --onefile --windowed --name custom_name download_rename_app.py
```

### 添加新的构建目标

1. 在矩阵中添加新的操作系统
2. 添加相应的构建步骤
3. 配置构建产物上传

### 修改发布配置

编辑 `release.yml` 中的发布信息：

```yaml
body: |
  ## 自定义发布说明
  
  ### 新功能
  - 功能1
  - 功能2
  
  ### 修复
  - 修复1
  - 修复2
```

## 最佳实践

1. **版本管理**
   - 使用语义化版本号 (如 v1.0.0)
   - 为每个发布创建标签

2. **代码质量**
   - 启用CI检查
   - 保持代码覆盖率
   - 定期更新依赖

3. **构建优化**
   - 使用缓存减少构建时间
   - 并行构建多个平台
   - 清理不必要的构建产物

4. **发布管理**
   - 自动化发布流程
   - 提供清晰的发布说明
   - 维护发布历史

## 支持

如果遇到问题：

1. 查看GitHub Actions文档
2. 检查工作流日志
3. 在仓库Issues中提问
4. 参考PyInstaller文档

## 更新日志

- v1.0.0: 初始版本，支持基本的CI/CD流程
- 支持Windows、macOS、Linux三平台构建
- 自动化发布流程
- 完整的测试和代码质量检查 