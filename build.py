#!/usr/bin/env python3
"""
本地构建脚本
用于测试应用程序的打包过程
"""

import os
import sys
import subprocess
import platform
import shutil

def run_command(command, check=True):
    """运行命令并返回结果"""
    print(f"执行命令: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print("输出:", result.stdout)
        if result.stderr:
            print("错误:", result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return e

def install_dependencies():
    """安装依赖包"""
    print("正在安装依赖包...")
    run_command("pip install -r requirements.txt")
    run_command("pip install pyinstaller")

def build_windows():
    """构建Windows可执行文件"""
    print("正在构建Windows可执行文件...")
    run_command("pyinstaller --onefile --windowed --name download_rename_app download_rename_app.py")
    
    # 检查输出文件
    exe_path = "dist/download_rename_app.exe"
    if os.path.exists(exe_path):
        print(f"✅ Windows可执行文件构建成功: {exe_path}")
        print(f"文件大小: {os.path.getsize(exe_path) / 1024 / 1024:.2f} MB")
    else:
        print("❌ Windows可执行文件构建失败")

def build_macos():
    """构建macOS应用程序包"""
    print("正在构建macOS应用程序包...")
    
    # 构建可执行文件
    run_command("pyinstaller --onefile --windowed --name download_rename_app download_rename_app.py")
    
    # 创建.app包
    app_name = "download_rename_app.app"
    if os.path.exists(app_name):
        shutil.rmtree(app_name)
    
    # 创建目录结构
    os.makedirs(f"{app_name}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_name}/Contents/Resources", exist_ok=True)
    
    # 复制可执行文件
    shutil.copy("dist/download_rename_app", f"{app_name}/Contents/MacOS/")
    
    # 创建Info.plist
    info_plist = f"""{app_name}/Contents/Info.plist"""
    with open(info_plist, 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>download_rename_app</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.downloadrenameapp</string>
    <key>CFBundleName</key>
    <string>文件下载重命名工具</string>
    <key>CFBundleDisplayName</key>
    <string>文件下载重命名工具</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>''')
    
    print(f"✅ macOS应用程序包构建成功: {app_name}")

def build_linux():
    """构建Linux可执行文件"""
    print("正在构建Linux可执行文件...")
    run_command("pyinstaller --onefile --windowed --name download_rename_app download_rename_app.py")
    
    # 检查输出文件
    exe_path = "dist/download_rename_app"
    if os.path.exists(exe_path):
        print(f"✅ Linux可执行文件构建成功: {exe_path}")
        print(f"文件大小: {os.path.getsize(exe_path) / 1024 / 1024:.2f} MB")
    else:
        print("❌ Linux可执行文件构建失败")

def clean_build():
    """清理构建文件"""
    print("正在清理构建文件...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["download_rename_app.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"已删除文件: {file_name}")

def main():
    """主函数"""
    print("🚀 文件下载重命名工具 - 本地构建脚本")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        sys.exit(1)
    
    print(f"✅ Python版本: {sys.version}")
    print(f"✅ 操作系统: {platform.system()} {platform.release()}")
    
    # 安装依赖
    install_dependencies()
    
    # 根据操作系统构建
    system = platform.system().lower()
    
    if system == "windows":
        build_windows()
    elif system == "darwin":  # macOS
        build_macos()
    elif system == "linux":
        build_linux()
    else:
        print(f"❌ 不支持的操作系统: {system}")
        sys.exit(1)
    
    print("\n🎉 构建完成！")
    print("构建文件位于 'dist' 目录中")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ 构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建过程中出现错误: {e}")
        sys.exit(1) 