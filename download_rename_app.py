import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import requests
import os
import threading
from urllib.parse import urlparse
import time

class DownloadRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件下载重命名工具")
        self.root.geometry("800x600")
        
        # 变量
        self.excel_file_path = tk.StringVar()
        self.download_folder = tk.StringVar()
        self.download_list = []
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Excel文件选择
        ttk.Label(main_frame, text="Excel文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.excel_file_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_frame, text="浏览", command=self.browse_excel_file).grid(row=0, column=2, padx=5, pady=5)
        
        # 下载文件夹选择
        ttk.Label(main_frame, text="下载文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.download_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_frame, text="浏览", command=self.browse_download_folder).grid(row=1, column=2, padx=5, pady=5)
        
        # 预览按钮
        ttk.Button(main_frame, text="预览Excel内容", command=self.preview_excel).grid(row=2, column=1, pady=10)
        
        # 下载按钮
        ttk.Button(main_frame, text="开始下载", command=self.start_download).grid(row=2, column=2, pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="就绪")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # 预览表格
        ttk.Label(main_frame, text="Excel内容预览:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        # 创建Treeview用于显示Excel内容
        self.tree = ttk.Treeview(main_frame, height=15)
        self.tree.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=6, column=3, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        # 配置行权重
        main_frame.rowconfigure(6, weight=1)
        
    def browse_excel_file(self):
        filename = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file_path.set(filename)
            
    def browse_download_folder(self):
        folder = filedialog.askdirectory(title="选择下载文件夹")
        if folder:
            self.download_folder.set(folder)
            
    def preview_excel(self):
        if not self.excel_file_path.get():
            messagebox.showerror("错误", "请先选择Excel文件")
            return
            
        try:
            # 读取Excel文件
            df = pd.read_excel(self.excel_file_path.get())
            
            # 清空现有内容
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # 设置列
            columns = list(df.columns)
            self.tree['columns'] = columns
            self.tree['show'] = 'headings'
            
            # 设置列标题
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, minwidth=100)
                
            # 添加数据
            for index, row in df.iterrows():
                values = [row[col] for col in columns]
                self.tree.insert('', 'end', values=values)
                
            self.status_label.config(text=f"已加载 {len(df)} 行数据")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法读取Excel文件: {str(e)}")
            
    def start_download(self):
        if not self.excel_file_path.get():
            messagebox.showerror("错误", "请先选择Excel文件")
            return
            
        if not self.download_folder.get():
            messagebox.showerror("错误", "请先选择下载文件夹")
            return
            
        if self.is_downloading:
            messagebox.showwarning("警告", "下载正在进行中，请等待完成")
            return
            
        # 在新线程中开始下载
        download_thread = threading.Thread(target=self.download_files)
        download_thread.daemon = True
        download_thread.start()
        
    def download_files(self):
        try:
            self.is_downloading = True
            self.status_label.config(text="正在读取Excel文件...")
            
            # 读取Excel文件
            df = pd.read_excel(self.excel_file_path.get())
            
            # 查找URL列
            url_column = None
            for col in df.columns:
                if 'url' in col.lower() or '链接' in col or '地址' in col:
                    url_column = col
                    break
                    
            if url_column is None:
                messagebox.showerror("错误", "未找到包含URL的列，请确保Excel文件中有URL列")
                self.is_downloading = False
                return
                
            # 获取Excel文件名（不含扩展名）
            excel_filename = os.path.splitext(os.path.basename(self.excel_file_path.get()))[0]
            
            # 过滤有效的URL
            valid_urls = []
            for index, row in df.iterrows():
                url = str(row[url_column]).strip()
                if url and url != 'nan' and (url.startswith('http://') or url.startswith('https://')):
                    valid_urls.append((index, url))
                    
            if not valid_urls:
                messagebox.showwarning("警告", "未找到有效的下载链接")
                self.is_downloading = False
                return
                
            self.status_label.config(text=f"找到 {len(valid_urls)} 个有效链接，开始下载...")
            self.progress['maximum'] = len(valid_urls)
            self.progress['value'] = 0
            
            # 开始下载
            for i, (index, url) in enumerate(valid_urls):
                try:
                    self.status_label.config(text=f"正在下载第 {i+1}/{len(valid_urls)} 个文件...")
                    
                    # 下载文件
                    response = requests.get(url, stream=True, timeout=30)
                    response.raise_for_status()
                    
                    # 获取文件扩展名
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        ext = '.jpg' if 'jpeg' in content_type else '.png'
                    elif 'pdf' in content_type:
                        ext = '.pdf'
                    elif 'zip' in content_type:
                        ext = '.zip'
                    elif 'excel' in content_type or 'spreadsheet' in content_type:
                        ext = '.xlsx'
                    else:
                        # 尝试从URL获取扩展名
                        parsed_url = urlparse(url)
                        path = parsed_url.path
                        if '.' in path:
                            ext = os.path.splitext(path)[1]
                        else:
                            ext = '.txt'
                    
                    # 生成新文件名
                    new_filename = f"{excel_filename}_{index:03d}{ext}"
                    file_path = os.path.join(self.download_folder.get(), new_filename)
                    
                    # 保存文件
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                
                    self.status_label.config(text=f"已下载: {new_filename}")
                    
                except Exception as e:
                    self.status_label.config(text=f"下载失败: {url} - {str(e)}")
                    
                # 更新进度条
                self.progress['value'] = i + 1
                self.root.update_idletasks()
                
                # 短暂延迟，避免过于频繁的请求
                time.sleep(0.5)
                
            self.status_label.config(text="下载完成！")
            messagebox.showinfo("完成", f"下载完成！共下载 {len(valid_urls)} 个文件到 {self.download_folder.get()}")
            
        except Exception as e:
            messagebox.showerror("错误", f"下载过程中出现错误: {str(e)}")
            self.status_label.config(text="下载失败")
            
        finally:
            self.is_downloading = False
            self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = DownloadRenameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 