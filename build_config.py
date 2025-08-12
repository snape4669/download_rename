#!/usr/bin/env python3
"""
构建配置文件
包含应用程序的详细打包配置
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class BuildConfig:
    def __init__(self):
        self.app_name = "download_rename_app"
        self.app_version = "1.0.0"
        self.app_description = "文件下载重命名工具"
        self.app_author = "Your Name"
        self.app_identifier = "com.example.downloadrenameapp"
        
        # 构建目录
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.spec_dir = Path("specs")
        
        # 确保目录存在
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        self.spec_dir.mkdir(exist_ok=True)
        
    def clean_build(self):
        """清理构建文件"""
        print("🧹 清理构建文件...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir, Path("__pycache__")]
        files_to_clean = [Path(f"{self.app_name}.spec")]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  已删除目录: {dir_path}")
                
        for file_path in files_to_clean:
            if file_path.exists():
                file_path.unlink()
                print(f"  已删除文件: {file_path}")
                
    def install_dependencies(self):
        """安装依赖包"""
        print("📦 安装依赖包...")
        
        commands = [
            "pip install --upgrade pip",
            "pip install -r requirements.txt",
            "pip install pyinstaller"
        ]
        
        for cmd in commands:
            print(f"  执行: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                print(f"  ✅ {cmd} 成功")
            except subprocess.CalledProcessError as e:
                print(f"  ❌ {cmd} 失败: {e}")
                return False
                
        return True
        
    def create_windows_spec(self):
        """创建Windows构建规范文件"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.app_name}.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
        
        spec_file = self.spec_dir / f"{self.app_name}_windows.spec"
        spec_file.write_text(spec_content, encoding='utf-8')
        print(f"  ✅ 已创建Windows构建规范: {spec_file}")
        
    def create_macos_spec(self):
        """创建macOS构建规范文件"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.app_name}.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)

app = BUNDLE(
    exe,
    name='{self.app_name}.app',
    icon=None,
    bundle_identifier='{self.app_identifier}',
    info_plist={{
        'CFBundleName': '{self.app_description}',
        'CFBundleDisplayName': '{self.app_description}',
        'CFBundleIdentifier': '{self.app_identifier}',
        'CFBundleVersion': '{self.app_version}',
        'CFBundleShortVersionString': '{self.app_version}',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    }},
)
'''
        
        spec_file = self.spec_dir / f"{self.app_name}_macos.spec"
        spec_file.write_text(spec_content, encoding='utf-8')
        print(f"  ✅ 已创建macOS构建规范: {spec_file}")
        
    def create_linux_spec(self):
        """创建Linux构建规范文件"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.app_name}.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
        
        spec_file = self.spec_dir / f"{self.app_name}_linux.spec"
        spec_file.write_text(spec_content, encoding='utf-8')
        print(f"  ✅ 已创建Linux构建规范: {spec_file}")
        
    def build_windows(self):
        """构建Windows可执行文件"""
        print("🪟 构建Windows可执行文件...")
        
        spec_file = self.spec_dir / f"{self.app_name}_windows.spec"
        cmd = f"pyinstaller {spec_file}"
        
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            
            exe_path = self.dist_dir / f"{self.app_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"  ✅ Windows可执行文件构建成功: {exe_path}")
                print(f"  📏 文件大小: {size_mb:.2f} MB")
                return True
            else:
                print(f"  ❌ Windows可执行文件构建失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 构建命令执行失败: {e}")
            return False
            
    def build_macos(self):
        """构建macOS应用程序包"""
        print("🍎 构建macOS应用程序包...")
        
        spec_file = self.spec_dir / f"{self.app_name}_macos.spec"
        cmd = f"pyinstaller {spec_file}"
        
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            
            app_path = self.dist_dir / f"{self.app_name}.app"
            if app_path.exists():
                print(f"  ✅ macOS应用程序包构建成功: {app_path}")
                return True
            else:
                print(f"  ❌ macOS应用程序包构建失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 构建命令执行失败: {e}")
            return False
            
    def build_linux(self):
        """构建Linux可执行文件"""
        print("🐧 构建Linux可执行文件...")
        
        spec_file = self.spec_dir / f"{self.app_name}_linux.spec"
        cmd = f"pyinstaller {spec_file}"
        
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            
            exe_path = self.dist_dir / self.app_name
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"  ✅ Linux可执行文件构建成功: {exe_path}")
                print(f"  📏 文件大小: {size_mb:.2f} MB")
                return True
            else:
                print(f"  ❌ Linux可执行文件构建失败")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 构建命令执行失败: {e}")
            return False
            
    def build_all(self):
        """构建所有平台的应用程序"""
        print("🚀 开始构建所有平台的应用程序...")
        print("=" * 60)
        
        # 清理构建文件
        self.clean_build()
        
        # 安装依赖
        if not self.install_dependencies():
            print("❌ 依赖安装失败，构建终止")
            return False
            
        # 创建构建规范文件
        print("\n📝 创建构建规范文件...")
        self.create_windows_spec()
        self.create_macos_spec()
        self.create_linux_spec()
        
        # 根据当前平台构建
        system = platform.system().lower()
        print(f"\n🔨 当前平台: {system}")
        
        success = False
        if system == "windows":
            success = self.build_windows()
        elif system == "darwin":  # macOS
            success = self.build_macos()
        elif system == "linux":
            success = self.build_linux()
        else:
            print(f"❌ 不支持的操作系统: {system}")
            return False
            
        if success:
            print(f"\n🎉 构建完成！")
            print(f"📁 构建文件位于: {self.dist_dir.absolute()}")
        else:
            print(f"\n❌ 构建失败！")
            
        return success

def main():
    """主函数"""
    print("🔧 文件下载重命名工具 - 构建配置工具")
    print("=" * 60)
    
    config = BuildConfig()
    
    try:
        config.build_all()
    except KeyboardInterrupt:
        print("\n❌ 构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 