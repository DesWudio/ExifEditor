# EXIF 编辑器

一个功能完整的可视化图片 EXIF 信息编辑工具，使用 Python、Tkinter 和 piexif 开发。

## 功能特性

- 📁 **打开图片**：支持 JPEG/JPG 格式图片
- 👀 **图片预览**：显示缩略图和基本信息（尺寸、格式、模式）
- 📋 **EXIF 浏览**：查看所有 EXIF 元数据，按 IFD 分类显示
- 🔍 **搜索过滤**：快速查找特定 EXIF 字段
- ✏️ **编辑字段**：双击任意字段即可编辑其值
- ➕ **添加字段**：添加自定义 EXIF 字段
- ⏰ **删除时间信息**：一键删除所有时间相关字段（DateTime、DateTimeOriginal、DateTimeDigitized、GPSTimeStamp）
- 📍 **删除位置信息**：一键删除所有 GPS 位置相关字段（27 个 GPS 标签）
- 🗑️ **清除 EXIF**：清除所有 EXIF 信息
- 💾 **保存/另存为**：保存修改后的图片，保留其他 EXIF 数据
- ℹ️ **用户反馈**：删除操作前检查数据存在性，提供明确提示

## 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install Pillow>=10.0.0 piexif>=1.1.3
```

## 使用方法

```bash
python exif_editor_full.py
```

## 界面说明

### 工具栏

| 按钮 | 功能 |
|------|------|
| 📁 打开图片 | 选择并打开 JPEG 图片文件 |
| 💾 保存 | 保存修改到当前文件 |
| 💾 另存为 | 将修改后的图片保存到新文件 |
| ⏰ 删除所有时间信息 | 删除所有时间相关 EXIF 字段 |
| 📍 删除所有位置信息 | 删除所有 GPS 位置相关 EXIF 字段 |
| 🗑️ 清除所有 EXIF | 清除全部 EXIF 数据 |
| ➕ 添加字段 | 添加自定义 EXIF 字段 |

### 图片预览区

- 显示图片缩略图（自动缩放适配）
- 显示图片基本信息：文件名、尺寸、格式、颜色模式

### EXIF 编辑器

- **搜索框**：输入关键词过滤 EXIF 字段列表
- **EXIF 列表**：树形视图显示所有 EXIF 信息
  - 按 IFD 分组：IFD0、ExifIFD、GPSIFD
  - 双击行可编辑字段值
  - 右键菜单可删除字段
- **详细信息**：显示选中字段的详细数据（技术名称、IFD、Tag ID、值）

## 支持的 EXIF 标签

### IFD0 标签

| 中文名称 | 技术名称 | Tag ID |
|----------|----------|--------|
| 图像宽度 | ImageWidth | 256 |
| 图像高度 | ImageHeight | 257 |
| 相机品牌 | Make | 271 |
| 相机型号 | Model | 272 |
| 方向 | Orientation | 274 |
| X 分辨率 | XResolution | 282 |
| Y 分辨率 | YResolution | 283 |
| 分辨率单位 | ResolutionUnit | 296 |
| 软件 | Software | 305 |
| 日期时间 | DateTime | 306 |
| 作者 | Artist | 315 |
| 版权 | Copyright | 33432 |
| 图像描述 | ImageDescription | 270 |

### ExifIFD 标签

| 中文名称 | 技术名称 | Tag ID |
|----------|----------|--------|
| 曝光时间 | ExposureTime | 33437 |
| 光圈值 | FNumber | 33437 |
| ISO 感光度 | ISOSpeedRatings | 34855 |
| Exif 版本 | ExifVersion | 36864 |
| 原始日期时间 | DateTimeOriginal | 36867 |
| 数字化日期时间 | DateTimeDigitized | 36868 |
| 快门速度值 | ShutterSpeedValue | 37121 |
| 光圈值 | ApertureValue | 37122 |
| 亮度值 | BrightnessValue | 37124 |
| 曝光补偿 | ExposureBiasValue | 37125 |
| 最大光圈值 | MaxApertureValue | 37126 |
| 测光模式 | MeteringMode | 37127 |
| 闪光灯 | Flash | 37377 |
| 焦距 | FocalLength | 37386 |
| 主体区域 | SubjectArea | 37390 |
| 制造商笔记 | MakerNote | 37500 |
| 用户评论 | UserComment | 37510 |
| Flashpix 版本 | FlashpixVersion | 40960 |
| 色彩空间 | ColorSpace | 40961 |
| 像素 X 维度 | PixelXDimension | 40962 |
| 像素 Y 维度 | PixelYDimension | 40963 |
| 组件配置 | ComponentsConfiguration | 40964 |
| 压缩比特每像素 | CompressedBitsPerPixel | 40965 |

### GPSIFD 标签

| 中文名称 | 技术名称 | Tag ID |
|----------|----------|--------|
| GPS 纬度参考 | GPSLatitudeRef | 1 |
| GPS 纬度 | GPSLatitude | 2 |
| GPS 经度参考 | GPSLongitudeRef | 3 |
| GPS 经度 | GPSLongitude | 4 |
| GPS 海拔参考 | GPSAltitudeRef | 5 |
| GPS 海拔 | GPSAltitude | 6 |
| GPS 时间戳 | GPSTimeStamp | 7 |
| GPS 卫星 | GPSSatellites | 8 |
| GPS 状态 | GPSStatus | 9 |
| GPS 测量模式 | GPSMeasureMode | 10 |
| GPS 速度参考 | GPSSpeedRef | 11 |
| GPS 速度 | GPSSpeed | 12 |
| GPS 航向参考 | GPSTrackRef | 13 |
| GPS 航向 | GPSTrack | 14 |
| GPS 图像方向参考 | GPSImgDirectionRef | 15 |
| GPS 图像方向 | GPSImgDirection | 16 |
| GPS 地图基准 | GPSMapDatum | 17 |
| GPS 目的地纬度参考 | GPSDestLatitudeRef | 18 |
| GPS 目的地纬度 | GPSDestLatitude | 19 |
| GPS 目的地经度参考 | GPSDestLongitudeRef | 20 |
| GPS 目的地经度 | GPSDestLongitude | 21 |
| GPS 目的地方位参考 | GPSDestBearingRef | 22 |
| GPS 目的地方位 | GPSDestBearing | 23 |
| GPS 目的地距离参考 | GPSDestDistanceRef | 24 |
| GPS 目的地距离 | GPSDestDistance | 25 |
| GPS 处理方法 | GPSProcessingMethod | 26 |
| GPS 版本 ID | GPSVersionID | 0 |

## 删除时间信息功能

点击"⏰ 删除所有时间信息"按钮会：

1. **检查是否存在时间信息**：扫描以下字段
   - DateTime (IFD0, Tag 306)
   - DateTimeOriginal (ExifIFD, Tag 36867)
   - DateTimeDigitized (ExifIFD, Tag 36868)
   - GPSTimeStamp (GPSIFD, Tag 7)

2. **无时间信息时**：显示提示"图片中不存在时间信息，无需删除。"

3. **有时间信息时**：
   - 弹出确认对话框，列出当前存在的时间字段
   - 确认后删除所有找到的时间字段
   - 显示成功消息，告知删除的字段数量
   - 刷新 EXIF 列表显示

## 删除位置信息功能

点击"📍 删除所有位置信息"按钮会：

1. **检查是否存在 GPS 信息**：扫描所有 27 个 GPS 标签（Tag 0-26）

2. **无 GPS 信息时**：显示提示"图片中不存在 GPS 位置信息，无需删除。"

3. **有 GPS 信息时**：
   - 弹出确认对话框，列出当前存在的 GPS 字段
   - 确认后删除所有找到的 GPS 字段
   - 显示成功消息，告知删除的字段数量
   - 刷新 EXIF 列表显示

## 注意事项

1. **依赖要求**：需要安装 `piexif` 库才能正确读写 EXIF 数据
2. **文件格式**：仅支持 JPEG/JPG 格式（EXIF 标准格式）
3. **兼容性**：某些相机特定的 EXIF 标签可能无法完全保留
4. **备份建议**：重要图片建议先备份再进行修改
5. **删除操作**：删除时间或位置信息后，必须点击"保存"按钮才会生效

## 文件结构

```
exif_editor/
├── exif_editor_full.py    # 主程序（高级版）
├── requirements.txt       # 依赖列表
└── README.md             # 本文件
```

## 许可证

MIT License

---

# EXIF Editor

A full-featured visual image EXIF metadata editing tool, developed with Python, Tkinter, and piexif.

## Features

- 📁 **Open Images**: Supports JPEG/JPG format images
- 👀 **Image Preview**: Displays thumbnail and basic information (dimensions, format, mode)
- 📋 **EXIF Browser**: View all EXIF metadata, organized by IFD
- 🔍 **Search Filter**: Quickly find specific EXIF fields
- ✏️ **Edit Fields**: Double-click any field to edit its value
- ➕ **Add Fields**: Add custom EXIF fields
- ⏰ **Delete Time Info**: One-click removal of all time-related fields (DateTime, DateTimeOriginal, DateTimeDigitized, GPSTimeStamp)
- 📍 **Delete Location Info**: One-click removal of all GPS location fields (27 GPS tags)
- 🗑️ **Clear EXIF**: Remove all EXIF data
- 💾 **Save/Save As**: Save modified images while preserving other EXIF data
- ℹ️ **User Feedback**: Checks for data existence before deletion operations with clear prompts

## Installation

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Pillow>=10.0.0 piexif>=1.1.3
```

## Usage

```bash
python exif_editor_full.py
```

## Interface Guide

### Toolbar

| Button | Function |
|--------|----------|
| 📁 Open Image | Select and open a JPEG image file |
| 💾 Save | Save modifications to the current file |
| 💾 Save As | Save the modified image to a new file |
| ⏰ Delete All Time Info | Remove all time-related EXIF fields |
| 📍 Delete All Location Info | Remove all GPS location-related EXIF fields |
| 🗑️ Clear All EXIF | Remove all EXIF data |
| ➕ Add Field | Add a custom EXIF field |

### Image Preview Area

- Displays image thumbnail (auto-scaled to fit)
- Shows basic image information: filename, dimensions, format, color mode

### EXIF Editor

- **Search Box**: Enter keywords to filter the EXIF field list
- **EXIF List**: Tree view displaying all EXIF information
  - Grouped by IFD: IFD0, ExifIFD, GPSIFD
  - Double-click a row to edit field values
  - Right-click menu to delete fields
- **Details Panel**: Shows detailed data for selected fields (technical name, IFD, Tag ID, value)

## Supported EXIF Tags

### IFD0 Tags

| Name | Technical Name | Tag ID |
|------|----------------|--------|
| Image Width | ImageWidth | 256 |
| Image Height | ImageHeight | 257 |
| Camera Make | Make | 271 |
| Camera Model | Model | 272 |
| Orientation | Orientation | 274 |
| X Resolution | XResolution | 282 |
| Y Resolution | YResolution | 283 |
| Resolution Unit | ResolutionUnit | 296 |
| Software | Software | 305 |
| Date Time | DateTime | 306 |
| Artist | Artist | 315 |
| Copyright | Copyright | 33432 |
| Image Description | ImageDescription | 270 |

### ExifIFD Tags

| Name | Technical Name | Tag ID |
|------|----------------|--------|
| Exposure Time | ExposureTime | 33437 |
| F-Number | FNumber | 33437 |
| ISO Speed Ratings | ISOSpeedRatings | 34855 |
| Exif Version | ExifVersion | 36864 |
| Date Time Original | DateTimeOriginal | 36867 |
| Date Time Digitized | DateTimeDigitized | 36868 |
| Shutter Speed Value | ShutterSpeedValue | 37121 |
| Aperture Value | ApertureValue | 37122 |
| Brightness Value | BrightnessValue | 37124 |
| Exposure Bias Value | ExposureBiasValue | 37125 |
| Max Aperture Value | MaxApertureValue | 37126 |
| Metering Mode | MeteringMode | 37127 |
| Flash | Flash | 37377 |
| Focal Length | FocalLength | 37386 |
| Subject Area | SubjectArea | 37390 |
| Maker Note | MakerNote | 37500 |
| User Comment | UserComment | 37510 |
| Flashpix Version | FlashpixVersion | 40960 |
| Color Space | ColorSpace | 40961 |
| Pixel X Dimension | PixelXDimension | 40962 |
| Pixel Y Dimension | PixelYDimension | 40963 |
| Components Configuration | ComponentsConfiguration | 40964 |
| Compressed Bits Per Pixel | CompressedBitsPerPixel | 40965 |

### GPSIFD Tags

| Name | Technical Name | Tag ID |
|------|----------------|--------|
| GPS Latitude Ref | GPSLatitudeRef | 1 |
| GPS Latitude | GPSLatitude | 2 |
| GPS Longitude Ref | GPSLongitudeRef | 3 |
| GPS Longitude | GPSLongitude | 4 |
| GPS Altitude Ref | GPSAltitudeRef | 5 |
| GPS Altitude | GPSAltitude | 6 |
| GPS Time Stamp | GPSTimeStamp | 7 |
| GPS Satellites | GPSSatellites | 8 |
| GPS Status | GPSStatus | 9 |
| GPS Measure Mode | GPSMeasureMode | 10 |
| GPS Speed Ref | GPSSpeedRef | 11 |
| GPS Speed | GPSSpeed | 12 |
| GPS Track Ref | GPSTrackRef | 13 |
| GPS Track | GPSTrack | 14 |
| GPS Img Direction Ref | GPSImgDirectionRef | 15 |
| GPS Img Direction | GPSImgDirection | 16 |
| GPS Map Datum | GPSMapDatum | 17 |
| GPS Dest Latitude Ref | GPSDestLatitudeRef | 18 |
| GPS Dest Latitude | GPSDestLatitude | 19 |
| GPS Dest Longitude Ref | GPSDestLongitudeRef | 20 |
| GPS Dest Longitude | GPSDestLongitude | 21 |
| GPS Dest Bearing Ref | GPSDestBearingRef | 22 |
| GPS Dest Bearing | GPSDestBearing | 23 |
| GPS Dest Distance Ref | GPSDestDistanceRef | 24 |
| GPS Dest Distance | GPSDestDistance | 25 |
| GPS Processing Method | GPSProcessingMethod | 26 |
| GPS Version ID | GPSVersionID | 0 |

## Delete Time Information Feature

Clicking the "⏰ Delete All Time Info" button will:

1. **Check for existing time information**: Scans the following fields
   - DateTime (IFD0, Tag 306)
   - DateTimeOriginal (ExifIFD, Tag 36867)
   - DateTimeDigitized (ExifIFD, Tag 36868)
   - GPSTimeStamp (GPSIFD, Tag 7)

2. **If no time info exists**: Shows message "No time information found in the image."

3. **If time info exists**:
   - Displays confirmation dialog listing current time fields
   - Deletes all found time fields upon confirmation
   - Shows success message with count of deleted fields
   - Refreshes EXIF list display

## Delete Location Information Feature

Clicking the "📍 Delete All Location Info" button will:

1. **Check for existing GPS information**: Scans all 27 GPS tags (Tag 0-26)

2. **If no GPS info exists**: Shows message "No GPS location information found in the image."

3. **If GPS info exists**:
   - Displays confirmation dialog listing current GPS fields
   - Deletes all found GPS fields upon confirmation
   - Shows success message with count of deleted fields
   - Refreshes EXIF list display

## Notes

1. **Dependency Requirement**: The `piexif` library must be installed for proper EXIF read/write operations
2. **File Format**: Only supports JPEG/JPG format (EXIF standard format)
3. **Compatibility**: Some camera-specific EXIF tags may not be fully preserved
4. **Backup Recommendation**: Important images should be backed up before modification
5. **Deletion Operations**: After deleting time or location information, you must click the "Save" button for changes to take effect

## File Structure

```
exif_editor/
├── exif_editor_full.py    # Main program (advanced version)
├── requirements.txt       # Dependencies list
└── README.md             # This file
```

## License

MIT License
