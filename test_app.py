#!/usr/bin/env python3
"""
简单的测试文件
用于验证应用程序的基本功能
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_tkinter():
    """测试tkinter是否正常工作"""
    try:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 测试基本功能
        messagebox.showinfo("测试", "tkinter工作正常！")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"tkinter测试失败: {e}")
        return False

def test_imports():
    """测试必要的导入"""
    try:
        import pandas as pd
        import requests
        import openpyxl
        import xlrd
        print("✅ 所有必要的包导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    required_files = [
        "download_rename_app.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有必需文件都存在")
        return True

def main():
    """主测试函数"""
    print("🧪 开始测试应用程序...")
    print("=" * 40)
    
    tests = [
        ("文件结构检查", test_file_structure),
        ("包导入测试", test_imports),
        ("tkinter测试", test_tkinter),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            print(f"✅ {test_name} 通过")
            passed += 1
        else:
            print(f"❌ {test_name} 失败")
    
    print("\n" + "=" * 40)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用程序准备就绪。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 