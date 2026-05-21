#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXIF 信息可视化工具（完整版）
用于查看和修改图片的 EXIF 信息
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from datetime import datetime
from typing import Optional, Dict, Any
import struct


try:
    import piexif
    HAS_PIEXIF = True
except ImportError:
    HAS_PIEXIF = False


class ExifEditorFull:
    def __init__(self, root):
        self.root = root
        self.root.title("EXIF 编辑器 高级版")
        self.root.geometry("1000x750")
        
        # 检查 piexif 是否安装
        if not HAS_PIEXIF:
            messagebox.showwarning(
                "缺少依赖",
                "未检测到 piexif 库，部分功能将不可用。\n\n"
                "请运行以下命令安装:\npip install piexif"
            )
        
        self.current_image_path = None
        self.original_image = None
        self.exif_dict = None  # piexif 格式的 EXIF 数据
        self.exif_display_data = {}  # 用于显示的 EXIF 数据
        
        # EXIF 标签映射（用户友好名称 -> 技术名称）
        self.exif_tag_mapping = {
            # IFD0 标签
            "ImageWidth": ("图像宽度", "IFD0", 256),
            "ImageHeight": ("图像高度", "IFD0", 257),
            "Make": ("相机品牌", "IFD0", 271),
            "Model": ("相机型号", "IFD0", 272),
            "Orientation": ("方向", "IFD0", 274),
            "XResolution": ("X 分辨率", "IFD0", 282),
            "YResolution": ("Y 分辨率", "IFD0", 283),
            "ResolutionUnit": ("分辨率单位", "IFD0", 296),
            "Software": ("软件", "IFD0", 305),
            "DateTime": ("日期时间", "IFD0", 306),
            "Artist": ("作者", "IFD0", 315),
            "Copyright": ("版权", "IFD0", 33432),
            "ImageDescription": ("图像描述", "IFD0", 270),
            
            # ExifIFD 标签
            "ExposureTime": ("曝光时间", "ExifIFD", 33437),
            "FNumber": ("光圈值", "ExifIFD", 33437),
            "ExposureProgram": ("曝光程序", "ExifIFD", 34850),
            "ISOSpeedRatings": ("ISO 感光度", "ExifIFD", 34855),
            "ExifVersion": ("Exif 版本", "ExifIFD", 36864),
            "DateTimeOriginal": ("原始日期时间", "ExifIFD", 36867),
            "DateTimeDigitized": ("数字化日期时间", "ExifIFD", 36868),
            "ShutterSpeedValue": ("快门速度值", "ExifIFD", 37121),
            "ApertureValue": ("光圈值", "ExifIFD", 37122),
            "BrightnessValue": ("亮度值", "ExifIFD", 37124),
            "ExposureBiasValue": ("曝光补偿", "ExifIFD", 37125),
            "MaxApertureValue": ("最大光圈值", "ExifIFD", 37126),
            "MeteringMode": ("测光模式", "ExifIFD", 37127),
            "Flash": ("闪光灯", "ExifIFD", 37377),
            "FocalLength": ("焦距", "ExifIFD", 37386),
            "SubjectArea": ("主体区域", "ExifIFD", 37390),
            "MakerNote": ("制造商笔记", "ExifIFD", 37500),
            "UserComment": ("用户评论", "ExifIFD", 37510),
            "FlashpixVersion": ("Flashpix 版本", "ExifIFD", 40960),
            "ColorSpace": ("色彩空间", "ExifIFD", 40961),
            "PixelXDimension": ("像素 X 维度", "ExifIFD", 40962),
            "PixelYDimension": ("像素 Y 维度", "ExifIFD", 40963),
            "ComponentsConfiguration": ("组件配置", "ExifIFD", 40964),
            "CompressedBitsPerPixel": ("压缩比特每像素", "ExifIFD", 40965),
            "ShutterSpeedValue": ("快门速度", "ExifIFD", 37121),
            "LensMake": ("镜头制造商", "ExifIFD", 37500),
            "LensModel": ("镜头型号", "ExifIFD", 37501),
            
            # GPSIFD 标签
            "GPSLatitudeRef": ("GPS 纬度参考", "GPSIFD", 0),
            "GPSLatitude": ("GPS 纬度", "GPSIFD", 2),
            "GPSLongitudeRef": ("GPS 经度参考", "GPSIFD", 3),
            "GPSLongitude": ("GPS 经度", "GPSIFD", 4),
            "GPSAltitudeRef": ("GPS 海拔参考", "GPSIFD", 5),
            "GPSAltitude": ("GPS 海拔", "GPSIFD", 6),
            "GPSTimeStamp": ("GPS 时间戳", "GPSIFD", 7),
            "GPSStatus": ("GPS 状态", "GPSIFD", 9),
            "GPSSatellites": ("GPS 卫星", "GPSIFD", 8),
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 顶部工具栏
        self.create_toolbar(main_frame, 0)
        
        # 中间区域 - 左右分栏
        middle_frame = ttk.Frame(main_frame)
        middle_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        middle_frame.columnconfigure(1, weight=1)
        middle_frame.rowconfigure(0, weight=1)
        
        # 左侧 - 图片预览
        self.create_preview_area(middle_frame, 0)
        
        # 分隔符
        separator = ttk.Separator(middle_frame, orient=tk.VERTICAL)
        separator.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=(10, 10))
        
        # 右侧 - EXIF 编辑器
        self.create_exif_editor(middle_frame, 2)
        
        # 底部状态栏
        self.create_status_bar(main_frame, 3)
    
    def create_toolbar(self, parent, row):
        """创建工具栏"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.grid(row=row, column=0, sticky=(tk.W, tk.E))
        
        # 打开文件按钮
        self.open_btn = ttk.Button(toolbar_frame, text="📁 打开图片", command=self.open_image)
        self.open_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存按钮
        self.save_btn = ttk.Button(toolbar_frame, text="💾 保存", command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # 另存为按钮
        self.save_as_btn = ttk.Button(toolbar_frame, text="💾 另存为", command=self.save_as_image, state=tk.DISABLED)
        self.save_as_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # 删除时间信息按钮
        self.remove_time_btn = ttk.Button(toolbar_frame, text="⏰ 删除所有时间信息", command=self.remove_all_time_info, state=tk.DISABLED)
        self.remove_time_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除位置信息按钮
        self.remove_gps_btn = ttk.Button(toolbar_frame, text="📍 删除所有位置信息", command=self.remove_all_gps_info, state=tk.DISABLED)
        self.remove_gps_btn.pack(side=tk.LEFT, padx=5)
        
        # 清除 EXIF 按钮
        self.clear_btn = ttk.Button(toolbar_frame, text="🗑️ 清除所有 EXIF", command=self.clear_exif, state=tk.DISABLED)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 添加字段按钮
        self.add_btn = ttk.Button(toolbar_frame, text="➕ 添加字段", command=self.add_custom_field, state=tk.DISABLED)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧显示 piexif 状态
        self.piexif_status = ttk.Label(toolbar_frame, text="piexif: " + ("已安装" if HAS_PIEXIF else "未安装"))
        self.piexif_status.pack(side=tk.RIGHT, padx=10)
        if HAS_PIEXIF:
            self.piexif_status.config(foreground="green")
        else:
            self.piexif_status.config(foreground="red")
    
    def create_preview_area(self, parent, column):
        """创建图片预览区域"""
        preview_frame = ttk.LabelFrame(parent, text="图片预览", padding="10")
        preview_frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # 图片显示区域
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 图片信息标签
        self.info_label = ttk.Label(preview_frame, foreground="gray", wraplength=300)
        self.info_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    def create_exif_editor(self, parent, column):
        """创建 EXIF 编辑器区域"""
        editor_frame = ttk.LabelFrame(parent, text="EXIF 信息编辑", padding="10")
        editor_frame.grid(row=0, column=column, sticky=(tk.W, tk.E, tk.N, tk.S))
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(1, weight=1)
        
        # 搜索框
        search_frame = ttk.Frame(editor_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(search_frame, text="🔍 搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        self.search_var.trace_add("write", self.filter_exif_list)
        
        # EXIF 列表区域（带滚动条）
        list_frame = ttk.Frame(editor_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建 Treeview
        columns = ("friendly_name", "technical_name", "ifd", "value")
        self.exif_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        self.exif_tree.heading("friendly_name", text="名称")
        self.exif_tree.heading("technical_name", text="技术名称")
        self.exif_tree.heading("ifd", text="IFD")
        self.exif_tree.heading("value", text="值")
        
        self.exif_tree.column("friendly_name", width=120)
        self.exif_tree.column("technical_name", width=120)
        self.exif_tree.column("ifd", width=60)
        self.exif_tree.column("value", width=300)
        
        # 滚动条
        scrollbar_v = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.exif_tree.yview)
        scrollbar_h = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.exif_tree.xview)
        self.exif_tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        self.exif_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 双击编辑
        self.exif_tree.bind("<Double-1>", self.edit_exif_item)
        
        # 详情区域
        detail_frame = ttk.LabelFrame(editor_frame, text="详细信息", padding="5")
        detail_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        detail_frame.columnconfigure(0, weight=1)
        detail_frame.rowconfigure(0, weight=1)
        
        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=8, wrap=tk.WORD)
        self.detail_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 选择项时显示详情
        self.exif_tree.bind("<<TreeviewSelect>>", self.show_details)
    
    def create_status_bar(self, parent, row):
        """创建状态栏"""
        self.status_var = tk.StringVar(value="就绪 - 打开图片开始编辑")
        status_label = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def open_image(self):
        """打开图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[
                ("JPEG 图片", "*.jpg *.jpeg"),
                ("PNG 图片", "*.png"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """加载图片并读取 EXIF 信息"""
        try:
            self.current_image_path = file_path
            self.original_image = Image.open(file_path)
            
            # 获取图片尺寸
            width, height = self.original_image.size
            
            # 显示缩略图
            self.display_thumbnail(self.original_image)
            self.info_label.config(text=f"尺寸：{width} x {height} 像素\n格式：{self.original_image.format}\n模式：{self.original_image.mode}")
            
            # 读取 EXIF 数据
            self.read_exif_data()
            
            # 启用按钮
            self.save_btn.config(state=tk.NORMAL)
            self.save_as_btn.config(state=tk.NORMAL)
            self.remove_time_btn.config(state=tk.NORMAL)
            self.remove_gps_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.NORMAL)
            self.add_btn.config(state=tk.NORMAL)
            
            self.status_var.set(f"已加载：{os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片：{str(e)}")
            import traceback
            traceback.print_exc()
    
    def display_thumbnail(self, image):
        """显示图片缩略图"""
        max_width = 350
        max_height = 400
        
        thumbnail = image.copy()
        thumbnail.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(thumbnail)
        self.preview_label.config(image=photo)
        self.preview_label.image = photo  # 保持引用
    
    def read_exif_data(self):
        """读取 EXIF 数据"""
        self.exif_display_data = {}
        self.exif_tree.delete(*self.exif_tree.get_children())
        self.detail_text.delete(1.0, tk.END)
        
        try:
            # 使用 piexif 读取 EXIF 数据
            if HAS_PIEXIF:
                exif_bytes = self.original_image.info.get('exif')
                if exif_bytes:
                    try:
                        self.exif_dict = piexif.load(exif_bytes)
                    except Exception as e:
                        # 如果 piexif.load 失败，尝试使用 Pillow 的 _getexif
                        self.status_var.set(f"警告：piexif 解析失败，使用备用方法 - {str(e)}")
                        self._load_exif_with_pillow()
                        return
                else:
                    self.exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            else:
                # 降级方案：使用 Pillow 内置方法
                self.exif_dict = None
                exif = self.original_image._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag_info = self.get_tag_info(tag_id)
                        formatted_value = self.format_exif_value(value)
                        
                        self.exif_display_data[tag_id] = {
                            "friendly_name": tag_info["friendly"],
                            "technical_name": tag_info["technical"],
                            "ifd": "IFD0",
                            "value": value,
                            "formatted": formatted_value
                        }
                        
                        self.exif_tree.insert("", tk.END, values=(
                            tag_info["friendly"],
                            tag_info["technical"],
                            "IFD0",
                            formatted_value
                        ))
                return
            
            # 解析 piexif 数据
            self.parse_piexif_data()
            
        except Exception as e:
            self.status_var.set(f"警告：无法读取 EXIF 数据 - {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _load_exif_with_pillow(self):
        """使用 Pillow 的 _getexif 方法加载 EXIF 数据（备用方案）"""
        try:
            exif = self.original_image._getexif()
            if exif:
                # 构建 piexif 格式的字典
                self.exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                
                for tag_id, value in exif.items():
                    # 将常见的标签放入 0th IFD
                    self.exif_dict["0th"][tag_id] = value
                
                # 解析并显示
                self.parse_piexif_data()
            else:
                self.exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        except Exception as e:
            self.status_var.set(f"警告：备用方法也失败 - {str(e)}")
            self.exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    
    def get_tag_info(self, tag_id):
        """获取标签信息"""
        # 反向查找映射
        for tech_name, (friendly, ifd, tid) in self.exif_tag_mapping.items():
            if tid == tag_id:
                return {"friendly": friendly, "technical": tech_name, "ifd": ifd}
        return {"friendly": f"Tag_{tag_id}", "technical": f"Tag_{tag_id}", "ifd": "Unknown"}
    
    def parse_piexif_data(self):
        """解析 piexif 数据"""
        if not self.exif_dict:
            return
        
        # 解析 0th IFD (IFD0)
        if "0th" in self.exif_dict:
            for tag_id, value in self.exif_dict["0th"].items():
                self.add_exif_item("IFD0", tag_id, value)
        
        # 解析 Exif IFD
        if "Exif" in self.exif_dict:
            for tag_id, value in self.exif_dict["Exif"].items():
                self.add_exif_item("ExifIFD", tag_id, value)
        
        # 解析 GPS IFD
        if "GPS" in self.exif_dict:
            for tag_id, value in self.exif_dict["GPS"].items():
                self.add_exif_item("GPSIFD", tag_id, value)
        
        # 解析 1st IFD
        if "1st" in self.exif_dict:
            for tag_id, value in self.exif_dict["1st"].items():
                self.add_exif_item("IFD1", tag_id, value)
    
    def add_exif_item(self, ifd_name, tag_id, value):
        """添加 EXIF 项到显示列表"""
        # 获取标签名称
        technical_name = self.get_technical_name(ifd_name, tag_id)
        friendly_name = self.get_friendly_name(technical_name)
        
        # 格式化值
        formatted_value = self.format_exif_value(value)
        
        # 存储数据
        key = f"{ifd_name}_{tag_id}"
        self.exif_display_data[key] = {
            "friendly_name": friendly_name,
            "technical_name": technical_name,
            "ifd": ifd_name,
            "tag_id": tag_id,
            "value": value,
            "formatted": formatted_value
        }
        
        # 添加到树形视图
        self.exif_tree.insert("", tk.END, values=(
            friendly_name,
            technical_name,
            ifd_name,
            formatted_value
        ), tags=(key,))
    
    def get_technical_name(self, ifd_name, tag_id):
        """根据 IFD 和标签 ID 获取技术名称"""
        for tech_name, (friendly, ifd, tid) in self.exif_tag_mapping.items():
            if ifd == ifd_name and tid == tag_id:
                return tech_name
        return f"Tag_{tag_id}"
    
    def get_friendly_name(self, technical_name):
        """根据技术名称获取友好名称"""
        for tech_name, (friendly, ifd, tid) in self.exif_tag_mapping.items():
            if tech_name == technical_name:
                return friendly
        return technical_name
    
    def format_exif_value(self, value):
        """格式化 EXIF 值用于显示"""
        if value is None:
            return ""
        
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8', errors='ignore').strip('\x00')
            except:
                return str(value)
        elif isinstance(value, str):
            return value
        elif isinstance(value, tuple):
            # GPS 坐标等特殊格式
            if len(value) == 3:
                try:
                    degrees = float(value[0][0]) / float(value[0][1])
                    minutes = float(value[1][0]) / float(value[1][1])
                    seconds = float(value[2][0]) / float(value[2][1])
                    decimal = degrees + minutes / 60.0 + seconds / 3600.0
                    return f"{decimal:.6f}"
                except:
                    pass
            # 分数格式
            if len(value) == 2:
                try:
                    return f"{float(value[0])/float(value[1]):.4f}"
                except:
                    pass
            return ", ".join(str(v) for v in value)
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return str(value)
    
    def filter_exif_list(self, *args):
        """根据搜索关键词过滤 EXIF 列表"""
        search_term = self.search_var.get().lower()
        
        # 取消隐藏所有项目
        for item in self.exif_tree.get_children():
            self.exif_tree.item(item, tags=tuple(t for t in self.exif_tree.item(item, "tags") if t != "hidden"))
        
        if not search_term:
            return
        
        # 隐藏不匹配的项目
        for item in self.exif_tree.get_children():
            values = self.exif_tree.item(item, "values")
            if search_term not in str(values).lower():
                current_tags = list(self.exif_tree.item(item, "tags"))
                current_tags.append("hidden")
                self.exif_tree.item(item, tags=tuple(current_tags))
    
    def show_details(self, event):
        """显示选中项的详细信息"""
        selection = self.exif_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        tags = self.exif_tree.item(item_id, "tags")
        
        # 找到数据键
        data_key = None
        for tag in tags:
            if tag.startswith("IFD"):
                data_key = tag
                break
        
        if data_key and data_key in self.exif_display_data:
            data = self.exif_display_data[data_key]
            details = f"友好名称：{data['friendly_name']}\n"
            details += f"技术名称：{data['technical_name']}\n"
            details += f"IFD: {data['ifd']}\n"
            details += f"标签 ID: {data['tag_id']}\n"
            details += f"原始值：{data['value']}\n"
            details += f"格式化值：{data['formatted']}"
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, details)
    
    def edit_exif_item(self, event):
        """编辑 EXIF 项"""
        selection = self.exif_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        tags = self.exif_tree.item(item_id, "tags")
        values = self.exif_tree.item(item_id, "values")
        
        # 找到数据键
        data_key = None
        for tag in tags:
            if tag.startswith("IFD"):
                data_key = tag
                break
        
        if not data_key or data_key not in self.exif_display_data:
            return
        
        data = self.exif_display_data[data_key]
        
        # 创建编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑 {data['friendly_name']}")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 信息显示
        info_text = f"标签：{data['friendly_name']} ({data['technical_name']})\nIFD: {data['ifd']} (ID: {data['tag_id']})"
        ttk.Label(dialog, text=info_text, justify=tk.LEFT).pack(pady=(10, 5))
        
        # 输入框
        ttk.Label(dialog, text="新值:").pack(anchor=tk.W, padx=10)
        value_var = tk.StringVar(value=data['formatted'])
        entry = ttk.Entry(dialog, textvariable=value_var, width=50)
        entry.pack(fill=tk.X, padx=10, pady=5)
        entry.focus()
        
        # 类型提示
        type_label = ttk.Label(dialog, text=f"当前类型：{type(data['value']).__name__}", foreground="gray")
        type_label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # 按钮框架
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def save_edit():
            new_value = value_var.get()
            
            # 更新显示数据
            self.exif_display_data[data_key]["value"] = new_value
            self.exif_display_data[data_key]["formatted"] = new_value
            
            # 更新树形视图
            new_values = (
                data['friendly_name'],
                data['technical_name'],
                data['ifd'],
                new_value
            )
            self.exif_tree.item(item_id, values=new_values)
            
            # 更新 piexif 数据
            if HAS_PIEXIF and self.exif_dict:
                self.update_piexif_data(data['ifd'], data['tag_id'], new_value)
            
            dialog.destroy()
        
        def delete_edit():
            if messagebox.askyesno("确认删除", f"确定要删除 '{data['friendly_name']}' 吗？"):
                del self.exif_display_data[data_key]
                self.exif_tree.delete(item_id)
                
                # 从 piexif 数据中删除
                if HAS_PIEXIF and self.exif_dict:
                    self.delete_from_piexif(data['ifd'], data['tag_id'])
                
                dialog.destroy()
        
        ttk.Button(btn_frame, text="保存", command=save_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=delete_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def update_piexif_data(self, ifd_name, tag_id, new_value):
        """更新 piexif 数据"""
        ifd_map = {
            "IFD0": "0th",
            "IFD1": "1st",
            "ExifIFD": "Exif",
            "GPSIFD": "GPS"
        }
        
        piexif_ifd = ifd_map.get(ifd_name)
        if not piexif_ifd or piexif_ifd not in self.exif_dict:
            return
        
        # 尝试转换值类型
        converted_value = self.convert_value_for_piexif(new_value, tag_id)
        self.exif_dict[piexif_ifd][tag_id] = converted_value
    
    def convert_value_for_piexif(self, value_str, tag_id):
        """将字符串值转换为 piexif 需要的格式"""
        # 尝试作为整数解析
        try:
            return int(value_str)
        except ValueError:
            pass
        
        # 尝试作为浮点数解析
        try:
            return float(value_str)
        except ValueError:
            pass
        
        # 作为字符串返回
        return value_str
    
    def delete_from_piexif(self, ifd_name, tag_id):
        """从 piexif 数据中删除项"""
        ifd_map = {
            "IFD0": "0th",
            "IFD1": "1st",
            "ExifIFD": "Exif",
            "GPSIFD": "GPS"
        }
        
        piexif_ifd = ifd_map.get(ifd_name)
        if piexif_ifd and piexif_ifd in self.exif_dict and tag_id in self.exif_dict[piexif_ifd]:
            del self.exif_dict[piexif_ifd][tag_id]
    
    def add_custom_field(self):
        """添加自定义字段"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加自定义字段")
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 名称输入
        ttk.Label(dialog, text="字段名称:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        name_var = tk.StringVar()
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=40)
        name_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # 值输入
        ttk.Label(dialog, text="字段值:").pack(anchor=tk.W, padx=10, pady=(5, 0))
        value_var = tk.StringVar()
        value_entry = ttk.Entry(dialog, textvariable=value_var, width=40)
        value_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # IFD 选择
        ttk.Label(dialog, text="IFD 位置:").pack(anchor=tk.W, padx=10, pady=(5, 0))
        ifd_var = tk.StringVar(value="IFD0")
        ifd_combo = ttk.Combobox(dialog, textvariable=ifd_var, width=37, 
                                  values=["IFD0", "ExifIFD", "GPSIFD"])
        ifd_combo.pack(fill=tk.X, padx=10, pady=5)
        
        # 按钮框架
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def add_field():
            name = name_var.get().strip()
            value = value_var.get().strip()
            ifd = ifd_var.get()
            
            if name:
                # 添加到一个不太可能冲突的标签 ID
                custom_tag_id = 50000 + len(self.exif_display_data)
                
                # 添加到显示数据
                key = f"{ifd}_{custom_tag_id}"
                self.exif_display_data[key] = {
                    "friendly_name": name,
                    "technical_name": name,
                    "ifd": ifd,
                    "tag_id": custom_tag_id,
                    "value": value,
                    "formatted": value
                }
                
                # 添加到树形视图
                self.exif_tree.insert("", tk.END, values=(
                    name, name, ifd, value
                ), tags=(key,))
                
                # 添加到 piexif 数据
                if HAS_PIEXIF and self.exif_dict:
                    ifd_map = {"IFD0": "0th", "ExifIFD": "Exif", "GPSIFD": "GPS"}
                    piexif_ifd = ifd_map.get(ifd)
                    if piexif_ifd:
                        self.exif_dict[piexif_ifd][custom_tag_id] = value
                
                dialog.destroy()
            else:
                messagebox.showwarning("警告", "字段名称不能为空")
        
        ttk.Button(btn_frame, text="添加", command=add_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def remove_all_time_info(self):
        """删除所有时间相关的 EXIF 信息"""
        # 先检查是否存在时间信息
        time_tags = {
            "0th": [306],  # DateTime
            "Exif": [36867, 36868],  # DateTimeOriginal, DateTimeDigitized
            "GPS": [7],  # GPSTimeStamp
        }
        
        existing_tags = []
        for ifd_name, tag_ids in time_tags.items():
            if ifd_name in self.exif_dict:
                for tag_id in tag_ids:
                    if tag_id in self.exif_dict[ifd_name]:
                        existing_tags.append(self.get_technical_name(ifd_name.replace("0th", "IFD0"), tag_id))
        
        if not existing_tags:
            messagebox.showinfo("提示", "图片中不存在时间信息，无需删除。")
            self.status_var.set("图片中不存在时间信息")
            return
        
        if not messagebox.askyesno("确认删除",
            f"确定要删除所有时间信息吗？\n\n"
            f"当前存在的时间字段：{', '.join(existing_tags)}\n\n"
            "这将删除以下字段:\n"
            "- DateTime (日期时间)\n"
            "- DateTimeOriginal (原始日期时间)\n"
            "- DateTimeDigitized (数字化日期时间)\n"
            "- GPSTimeStamp (GPS 时间戳)"):
            return
        
        deleted_count = 0
        
        for ifd_name, tag_ids in time_tags.items():
            if ifd_name in self.exif_dict:
                for tag_id in tag_ids:
                    if tag_id in self.exif_dict[ifd_name]:
                        del self.exif_dict[ifd_name][tag_id]
                        deleted_count += 1
        
        # 刷新显示 - 使用 parse_piexif_data 而不是 read_exif_data
        # 因为 read_exif_data 会重新从原始图片读取 EXIF，覆盖我们的修改
        self.exif_display_data = {}
        self.exif_tree.delete(*self.exif_tree.get_children())
        self.detail_text.delete(1.0, tk.END)
        self.parse_piexif_data()
        
        self.status_var.set(f"已删除 {deleted_count} 个时间相关字段，请保存图片以应用更改")
        messagebox.showinfo("成功", f"已删除 {deleted_count} 个时间相关字段。\n\n请记得点击'保存'按钮以保存修改后的图片。")
    
    def remove_all_gps_info(self):
        """删除所有 GPS 位置相关的 EXIF 信息"""
        # 先检查是否存在 GPS 信息
        gps_tags = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        gps_tag_names = {
            0: "GPSVersionID", 1: "GPSLatitudeRef", 2: "GPSLatitude",
            3: "GPSLongitudeRef", 4: "GPSLongitude", 5: "GPSAltitudeRef",
            6: "GPSAltitude", 7: "GPSTimeStamp", 8: "GPSSatellites",
            9: "GPSStatus", 10: "GPSMeasureMode", 11: "GPSSpeedRef",
            12: "GPSSpeed", 13: "GPSTrackRef", 14: "GPSTrack",
            15: "GPSImgDirectionRef", 16: "GPSImgDirection", 17: "GPSMapDatum",
            18: "GPSDestLatitudeRef", 19: "GPSDestLatitude", 20: "GPSDestLongitudeRef",
            21: "GPSDestLongitude", 22: "GPSDestBearingRef", 23: "GPSDestBearing",
            24: "GPSDestDistanceRef", 25: "GPSDestDistance", 26: "GPSProcessingMethod"
        }
        
        existing_tags = []
        if "GPS" in self.exif_dict:
            for tag_id in gps_tags:
                if tag_id in self.exif_dict["GPS"]:
                    existing_tags.append(gps_tag_names.get(tag_id, f"Tag_{tag_id}"))
        
        if not existing_tags:
            messagebox.showinfo("提示", "图片中不存在 GPS 位置信息，无需删除。")
            self.status_var.set("图片中不存在 GPS 位置信息")
            return
        
        if not messagebox.askyesno("确认删除",
            f"确定要删除所有 GPS 位置信息吗？\n\n"
            f"当前存在的 GPS 字段：{', '.join(existing_tags)}\n\n"
            "这将删除以下字段:\n"
            "- GPSLatitudeRef (纬度参考)\n"
            "- GPSLatitude (纬度)\n"
            "- GPSLongitudeRef (经度参考)\n"
            "- GPSLongitude (经度)\n"
            "- GPSAltitudeRef (海拔参考)\n"
            "- GPSAltitude (海拔)\n"
            "- GPSTimeStamp (GPS 时间戳)\n"
            "- GPSStatus (GPS 状态)\n"
            "- GPSSatellites (GPS 卫星)\n"
            "- GPSMeasureMode (测量模式)\n"
            "- GPSSpeedRef (速度参考)\n"
            "- GPSSpeed (速度)\n"
            "- GPSTrackRef (航向参考)\n"
            "- GPSTrack (航向)\n"
            "- GPSImgDirectionRef (图像方向参考)\n"
            "- GPSImgDirection (图像方向)\n"
            "- GPSMapDatum (地图基准)\n"
            "- GPSDestLatitudeRef (目的地纬度参考)\n"
            "- GPSDestLatitude (目的地纬度)\n"
            "- GPSDestLongitudeRef (目的地经度参考)\n"
            "- GPSDestLongitude (目的地经度)\n"
            "- GPSDestBearingRef (目的地方位参考)\n"
            "- GPSDestBearing (目的地方位)\n"
            "- GPSDestDistanceRef (目的地距离参考)\n"
            "- GPSDestDistance (目的地距离)\n"
            "- GPSVersionID (GPS 版本 ID)"):
            return
        
        deleted_count = 0
        
        if "GPS" in self.exif_dict:
            for tag_id in gps_tags:
                if tag_id in self.exif_dict["GPS"]:
                    del self.exif_dict["GPS"][tag_id]
                    deleted_count += 1
        
        # 刷新显示 - 使用 parse_piexif_data 而不是 read_exif_data
        self.exif_display_data = {}
        self.exif_tree.delete(*self.exif_tree.get_children())
        self.detail_text.delete(1.0, tk.END)
        self.parse_piexif_data()
        
        self.status_var.set(f"已删除 {deleted_count} 个 GPS 相关字段，请保存图片以应用更改")
        messagebox.showinfo("成功", f"已删除 {deleted_count} 个 GPS 相关字段。\n\n请记得点击'保存'按钮以保存修改后的图片。")
    
    def clear_exif(self):
        """清除所有 EXIF 数据"""
        if messagebox.askyesno("确认清除", "确定要清除所有 EXIF 信息吗？此操作不可撤销。"):
            self.exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            self.exif_display_data = {}
            self.exif_tree.delete(*self.exif_tree.get_children())
            self.detail_text.delete(1.0, tk.END)
            self.status_var.set("已清除所有 EXIF 信息")
    
    def save_image(self):
        """保存图片到原路径"""
        if self.current_image_path:
            self.save_image_to_path(self.current_image_path)
    
    def save_as_image(self):
        """另存为"""
        file_path = filedialog.asksaveasfilename(
            title="保存图片",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG 图片", "*.jpg *.jpeg"),
                ("所有文件", "*.*")
            ],
            initialfile=os.path.basename(self.current_image_path or "image.jpg")
        )
        
        if file_path:
            self.save_image_to_path(file_path)
    
    def save_image_to_path(self, file_path):
        """保存图片到指定路径"""
        try:
            # 创建新的图片对象 - 清除原始 EXIF
            output_image = self.original_image.copy()
            output_image.info.pop('exif', None)  # 清除原始 EXIF
            
            # 如果图片是 RGB 模式外的模式，转换为 RGB（JPEG 只支持 RGB）
            if output_image.mode not in ('RGB', 'L'):
                output_image = output_image.convert('RGB')
            
            # 使用 piexif 保存 EXIF 数据
            if HAS_PIEXIF and self.exif_dict:
                try:
                    # 确保所有必需的 IFD 都存在且格式正确
                    self._prepare_exif_dict_for_save()
                    
                    # 检查是否有任何有效的 EXIF 数据
                    has_data = False
                    for ifd_name in ["0th", "Exif", "GPS", "1st"]:
                        if ifd_name in self.exif_dict and self.exif_dict[ifd_name]:
                            has_data = True
                            break
                    
                    exif_bytes = None
                    if has_data:
                        exif_bytes = piexif.dump(self.exif_dict)
                    else:
                        # 如果没有 EXIF 数据，清除 info 中的 exif
                        output_image.info.pop('exif', None)
                        
                except Exception as e:
                    messagebox.showwarning("警告", f"保存 EXIF 数据时出错：{str(e)}\n将继续保存但不包含 EXIF 信息。")
                    exif_bytes = None
            
            # 保存图片 - 使用 exif 参数而不是 info['exif']
            if file_path.lower().endswith('.png'):
                output_image.save(file_path)
            else:
                if exif_bytes:
                    output_image.save(file_path, "JPEG", quality=95, exif=exif_bytes)
                else:
                    output_image.save(file_path, "JPEG", quality=95)
            
            self.status_var.set(f"已保存到：{file_path}")
            messagebox.showinfo("成功", f"图片已成功保存到:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            import traceback
            traceback.print_exc()
    
    def _prepare_exif_dict_for_save(self):
        """准备 EXIF 字典用于保存，确保格式正确"""
        # 确保所有必需的 IFD 都存在
        required_ifds = ["0th", "Exif", "GPS", "1st", "thumbnail"]
        for ifd in required_ifds:
            if ifd not in self.exif_dict:
                if ifd == "thumbnail":
                    self.exif_dict[ifd] = None
                else:
                    self.exif_dict[ifd] = {}
        
        # 清理空的 IFD（除了至少保留一个非空的）
        has_non_empty = False
        for ifd_name in ["0th", "Exif", "GPS", "1st"]:
            if self.exif_dict.get(ifd_name):
                has_non_empty = True
                break
        
        # 如果所有 IFD 都为空，至少保留一个空的 0th IFD
        if not has_non_empty:
            self.exif_dict["0th"] = {}


def main():
    root = tk.Tk()
    app = ExifEditorFull(root)
    root.mainloop()


if __name__ == "__main__":
    main()
