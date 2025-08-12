from setuptools import setup, find_packages

setup(
    name="download_rename_app",
    version="1.0.0",
    description="文件下载重命名工具",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "requests>=2.25.0",
        "openpyxl>=3.0.0",
        "xlrd>=2.0.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "download_rename_app=download_rename_app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
) 