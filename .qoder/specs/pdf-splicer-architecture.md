# PdfSplicer 项目代码架构分析文档

## Context

用户需要对 PdfSplicer 项目进行全面的代码分析，理解其功能、架构、实现逻辑、依赖关系和部署配置，并输出一份清晰的架构文档。

---

## 1. 项目概述

**PdfSplicer** 是一个 macOS 桌面应用，用于将正反面分别扫描的 PDF 文件按正确页码顺序拼接为一个完整文档。采用 Python + Tkinter 构建 GUI，使用 pypdf 进行 PDF 处理，支持空白页自动检测与跳过。

---

## 2. 项目目录结构

```
SplicPdfing/
├── main.py                  # 主程序入口，包含全部业务逻辑和 UI
├── requirements.txt         # Python 依赖清单
├── dmg_settings.py          # macOS DMG 安装包配置
├── PdfSplicer.spec          # PyInstaller 打包配置
├── build_app.sh             # 一键自动构建脚本
├── run.sh                   # 开发环境运行脚本
├── app_icon.icns            # macOS 应用图标
├── app_icon.png             # PNG 格式应用图标
├── bin/                     # 内置 Poppler 二进制工具
│   ├── pdftoppm             # PDF 转图片（用于空白页检测）
│   └── pdftops              # PDF 转 PostScript
├── LICENSE                  # MIT 许可证
├── README.md                # 中文文档
├── README.en/jp/ko/fr/de/es/ru/pt.md  # 多语言文档（9种语言）
├── build/                   # PyInstaller 构建临时目录
├── dist/                    # PyInstaller 输出目录
└── .venv/                   # Python 虚拟环境
```

---

## 3. 技术栈与依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| `pypdf` | 未锁定 | PDF 读写、页面操作（PdfReader/PdfWriter） |
| `pdf2image` | 未锁定 | PDF 页面转图片（依赖 Poppler） |
| `Pillow` | 未锁定 | 图像处理（灰度转换、像素分析） |
| `tkinterdnd2-universal` | 未锁定 | Tkinter 拖放功能扩展 |
| **Poppler** (bin/pdftoppm) | 系统/内置 | PDF 渲染引擎，供 pdf2image 调用 |
| **PyInstaller** | 构建依赖 | 打包为 macOS .app |
| **dmgbuild** | 构建依赖 | 生成 .dmg 安装包 |

---

## 4. 核心架构：PDFMerger 类

整个应用由单一类 `PDFMerger` 承载（继承自 `TkinterDnD.Tk`），所有 UI 和业务逻辑集中在 `main.py` 中。

### 4.1 类结构与方法职责

```
PDFMerger(TkinterDnD.Tk)
│
├── __init__()              # L11-24  初始化窗口、状态变量、检查依赖、构建 UI
│
├── check_poppler()         # L26-36  检测 Poppler 可用性（本地 bin → 系统 PATH）
├── init_ui()               # L38-112 构建完整 GUI 布局
├── create_drop_target()    # L114-129 创建拖放目标区域
│
├── open_front_file_dialog() # L131-134 弹出文件选择对话框（正面）
├── open_back_file_dialog()  # L136-139 弹出文件选择对话框（反面）
├── select_front()           # L141-145 处理正面文件路径（对话框/拖放统一入口）
├── select_back()            # L147-151 处理反面文件路径
├── select_output()          # L153-156 选择输出文件夹
├── open_output_folder()     # L158-168 跨平台打开输出文件夹
│
├── is_blank_page()          # L170-188 空白页检测算法
└── merge_pdfs()             # L190-239 PDF 拼接核心逻辑
```

> **注意**: L242-350 存在上述方法的完整重复定义（代码重复问题），Python 会使用后定义的版本。

### 4.2 实例变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `self.front_path` | `StringVar` | 正面 PDF 文件路径 |
| `self.back_path` | `StringVar` | 反面 PDF 文件路径 |
| `self.output_dir` | `StringVar` | 输出文件夹路径 |
| `self.skip_blank` | `BooleanVar` | 是否跳过空白页（默认 False） |
| `self.poppler_path` | `str/None` | Poppler 工具目录路径 |
| `self.poppler_available` | `bool` | Poppler 是否可用 |

---

## 5. 核心功能详解

### 5.1 PDF 拼接算法 (`merge_pdfs`, L190-239)

**数据流**: 用户选择文件 → 读取 PDF → 页面排序 → 空白页过滤 → 写入输出文件

```
输入验证 → PdfReader 读取正/反面 PDF
                ↓
        页数是否相等？
       /              \
     是                否
     ↓                 ↓
交错合并（反面倒序）   简单追加
     ↓                 ↓
     └──── ordered_pages ────┘
                ↓
        启用跳过空白页？
       /              \
     是                否
     ↓                 ↓
逐页检测并过滤      保留全部页面
     ↓                 ↓
     └──── final_pages ─────┘
                ↓
        PdfWriter 写入 output.pdf
                ↓
        messagebox 显示结果摘要
```

**交错合并逻辑** (页数相等时):
- 正面页按原序: `front[0], front[1], ..., front[n-1]`
- 反面页倒序穿插: `back[n-1], back[n-2], ..., back[0]`
- 最终顺序: `front[0], back[n-1], front[1], back[n-2], ...`
- 这符合实际场景：正面扫描顺序为 1,3,5,7，反面扫描顺序为 8,6,4,2

### 5.2 空白页检测算法 (`is_blank_page`, L170-188)

```
page → PdfWriter 写入内存 (BytesIO)
     → pdf2image.convert_from_bytes() 转为 PIL Image
     → .convert('L') 转灰度图
     → 获取所有像素值
     → 计算: avg_gray = 像素平均值
     → 计算: var_gray = 像素方差
     → 判定: avg_gray >= 250 AND var_gray <= 10 → 空白页
```

**阈值含义**:
- `avg_gray >= 250`: 平均灰度接近 255（纯白），页面整体极亮
- `var_gray <= 10`: 灰度方差极低，像素值分布均匀（无文字/图案）

**容错**: 若 Poppler 不可用或转换异常，返回 `False`（不视为空白页）

### 5.3 Poppler 检测策略 (`check_poppler`, L26-36)

优先级：`项目内置 bin/pdftoppm` → `系统 PATH 中的 pdftoppm`
- 打包后的 .app 会包含 bin 目录，确保独立运行
- 若均不可用，禁用"跳过空白页"复选框并弹出警告

---

## 6. 用户界面交互流程

### 6.1 UI 布局（自上而下）

```
┌─────────────────────────────────────┐
│  说明文字（4步操作步骤）              │
│  "请选择正面和反面PDF文件"            │
├─────────────────┬───────────────────┤
│  [正面 PDF]      │  [反面 PDF]       │
│  ┌─选择按钮─┐   │  ┌─选择按钮─┐    │
│  │拖拽区域  │   │  │拖拽区域  │    │
│  └─────────┘   │  └─────────┘    │
│  文件名显示     │  文件名显示      │
├─────────────────┴───────────────────┤
│         ☐ 跳过空白页                  │
├─────────────────────────────────────┤
│  [输出路径] [选择输出文件夹]          │
├─────────────────────────────────────┤
│  [打开输出文件夹]  [开始拼接]         │
└─────────────────────────────────────┘
```

### 6.2 文件选择机制

支持两种方式，统一通过 `select_front`/`select_back` 处理:
- **按钮选择**: `filedialog.askopenfilename()` → 传入路径字符串
- **拖放选择**: `TkinterDnD` 事件 → 传入 event 对象（通过 `event.data.strip('{}')` 提取路径）

### 6.3 消息提示机制

| 场景 | 类型 | 触发位置 |
|------|------|----------|
| Poppler 缺失 | `showwarning` | init_ui (L94) |
| 输出文件夹无效 | `showwarning` | open_output_folder (L168) |
| 未选择完整路径 | `showwarning` | merge_pdfs (L196) |
| 拼接成功 | `showinfo` | merge_pdfs (L237)，含输出路径/空白页信息/总页数 |
| 拼接失败 | `showerror` | merge_pdfs (L239)，显示异常信息 |

---

## 7. 构建与分发配置

### 7.1 PyInstaller 配置 (`PdfSplicer.spec`)

- 入口: `main.py`
- 数据捆绑: `bin` 目录（Poppler 工具）
- 输出: `PdfSplicer.app` (macOS 应用包)
- 无控制台窗口 (`console=False`)
- 启用 UPX 压缩

### 7.2 DMG 配置 (`dmg_settings.py`)

- 格式: `UDBZ`（bzip2 压缩）
- 包含: `dist/PdfSplicer` 和 `dist/PdfSplicer.app`
- Applications 快捷方式: 方便用户拖入应用程序文件夹
- 图标位置: 应用 (140, 120)，Applications (500, 120)

### 7.3 构建流程 (`build_app.sh`)

```
安装 requirements.txt 依赖
  → 检查/安装 pyinstaller + dmgbuild
  → 清理旧 build/ dist/
  → PyInstaller 打包 (含 bin 目录和 PyQt6 隐藏导入)
  → dmgbuild 生成 DMG
  → 启动检测（后台运行 App，检查日志中的错误）
```

### 7.4 开发运行 (`run.sh`)

配置 PyQt6 插件路径环境变量后，从虚拟环境执行 `main.py`。

---

## 8. 数据流总览

```
用户操作
  │
  ├─ 选择/拖放正面PDF ──→ self.front_path (StringVar)
  ├─ 选择/拖放反面PDF ──→ self.back_path (StringVar)
  ├─ 选择输出文件夹 ────→ self.output_dir (StringVar)
  └─ 勾选跳过空白页 ────→ self.skip_blank (BooleanVar)
  │
  ▼ 点击"开始拼接"
  │
  merge_pdfs()
  │
  ├─ PdfReader(front_path) ──→ front_reader.pages[]
  ├─ PdfReader(back_path) ───→ back_reader.pages[]
  │
  ├─ 页面排序算法 ──→ ordered_pages[]
  │
  ├─ [可选] is_blank_page() 过滤 ──→ final_pages[]
  │   └─ PdfWriter → BytesIO → pdf2image → PIL → 灰度分析
  │
  ├─ PdfWriter.add_page() → open(output.pdf, 'wb')
  │
  └─ messagebox.showinfo() 显示结果
```

---

## 9. 已识别的代码问题

### 9.1 方法重复定义 (L242-350)

`main.py` 第 242-350 行完整重复了以下 8 个方法:
- `open_front_file_dialog`, `open_back_file_dialog`
- `select_front`, `select_back`, `select_output`
- `open_output_folder`, `is_blank_page`, `merge_pdfs`

Python 中后定义的方法会覆盖前者，实际运行的是 L242-350 的版本。由于两份代码完全一致，功能不受影响，但应删除重复代码（建议保留 L131-239，删除 L242-350）。

### 9.2 未启用跳过时仍检测空白页

`merge_pdfs` 中 L228/L339:
```python
has_blank = any(self.is_blank_page(p) for p in ordered_pages if self.poppler_available)
```
即使用户未勾选"跳过空白页"，仍会遍历所有页面进行空白页检测（仅用于在结果弹窗中显示）。对大文件会造成不必要的性能开销。

### 9.3 依赖版本未锁定

`requirements.txt` 中所有依赖均未指定版本号，可能导致不同环境下行为不一致。

---

## 10. 总结

PdfSplicer 是一个功能完整、架构简洁的单文件 macOS 桌面应用：
- **单一类设计**: 所有逻辑集中在 `PDFMerger` 类中，适合小型工具应用
- **核心价值**: 正反面扫描件的智能交错合并（反面倒序处理）
- **可选增强**: 基于灰度统计的空白页检测与跳过
- **完整工具链**: 从开发运行到 PyInstaller 打包再到 DMG 分发，全流程覆盖
- **多语言文档**: 覆盖 9 种语言的 README
