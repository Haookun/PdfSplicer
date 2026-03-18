import sys
import os
import subprocess
import io
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter


class PDFMerger(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        self.title('PdfSplicer')
        self.geometry('520x480')
        self.minsize(480, 440)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.front_path = ctk.StringVar()
        self.back_path = ctk.StringVar()
        self.output_dir = ctk.StringVar()
        self.skip_blank = ctk.BooleanVar(value=False)

        self.poppler_path = None
        self.poppler_available = self.check_poppler()

        self.init_ui()

    # ── Poppler 检测 ──────────────────────────────────────────────

    def check_poppler(self):
        import shutil
        app_bin = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'pdftoppm')
        if os.path.isfile(app_bin) and os.access(app_bin, os.X_OK):
            self.poppler_path = os.path.dirname(app_bin)
            return True
        poppler_bin = shutil.which('pdftoppm')
        if poppler_bin:
            self.poppler_path = os.path.dirname(poppler_bin)
            return True
        return False

    # ── UI 构建 ───────────────────────────────────────────────────

    def init_ui(self):
        # 主容器
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # ── 标题栏 ──
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            header, text="PdfSplicer",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#1a1a1a"
        ).pack(side="left")

        # ── 文件选择区 ──
        file_frame = ctk.CTkFrame(main, fg_color="transparent")
        file_frame.pack(fill="both", expand=True, pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)

        self.front_card, self.front_label = self._create_drop_card(
            file_frame, "正面 PDF", "拖放文件至此\n或点击选择",
            self._on_front_drop, self._on_front_click, row=0, col=0
        )
        self.back_card, self.back_label = self._create_drop_card(
            file_frame, "反面 PDF", "拖放文件至此\n或点击选择",
            self._on_back_drop, self._on_back_click, row=0, col=1
        )

        # ── 输出路径 ──
        output_frame = ctk.CTkFrame(main, fg_color="transparent")
        output_frame.pack(fill="x", pady=(0, 8))

        self.output_entry = ctk.CTkEntry(
            output_frame, textvariable=self.output_dir,
            placeholder_text="选择输出文件夹...", state="readonly",
            height=36
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            output_frame, text="选择", width=70, height=36,
            command=self.select_output
        ).pack(side="right")

        # ── 选项 ──
        option_frame = ctk.CTkFrame(main, fg_color="transparent")
        option_frame.pack(fill="x", pady=(0, 12))

        self.skip_check = ctk.CTkCheckBox(
            option_frame, text="跳过空白页",
            variable=self.skip_blank,
            font=ctk.CTkFont(size=13),
            text_color="#333333"
        )
        self.skip_check.pack(side="left")

        if not self.poppler_available:
            self.skip_check.configure(state="disabled")
            self.after(500, lambda: messagebox.showwarning(
                "依赖缺失", "未检测到 poppler (pdftoppm)，空白页识别功能不可用。"
            ))

        # ── 操作按钮 ──
        action_frame = ctk.CTkFrame(main, fg_color="transparent")
        action_frame.pack(fill="x")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        ctk.CTkButton(
            action_frame, text="打开输出文件夹", height=40,
            fg_color="transparent", border_width=1,
            font=ctk.CTkFont(size=14),
            command=self.open_output_folder
        ).grid(row=0, column=0, padx=(0, 5), sticky="ew")

        ctk.CTkButton(
            action_frame, text="开始拼接", height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.merge_pdfs
        ).grid(row=0, column=1, padx=(5, 0), sticky="ew")

    # ── 拖放卡片 ─────────────────────────────────────────────────

    def _create_drop_card(self, parent, title, hint, drop_cmd, click_cmd, row, col):
        """创建一个可拖放/可点击的文件选择卡片"""
        outer = ctk.CTkFrame(parent, corner_radius=10)
        outer.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        parent.rowconfigure(row, weight=1)

        # 标题
        ctk.CTkLabel(
            outer, text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1a1a1a"
        ).pack(pady=(10, 0))

        # 拖放区域 — 使用原生 tk.Frame 以支持 tkinterdnd2
        drop_zone = tk.Frame(outer, bg="#e8e8e8", relief="flat", bd=0)
        drop_zone.pack(fill="both", expand=True, padx=12, pady=8)

        hint_label = tk.Label(
            drop_zone, text=hint,
            fg="#555555", bg="#e8e8e8",
            font=("Helvetica", 12), justify="center"
        )
        hint_label.pack(expand=True)

        # 注册拖放
        drop_zone.drop_target_register(DND_FILES)
        drop_zone.dnd_bind('<<Drop>>', drop_cmd)

        # 点击选择
        drop_zone.bind("<Button-1>", click_cmd)
        hint_label.bind("<Button-1>", click_cmd)

        # 悬停效果
        def on_enter(e):
            drop_zone.config(bg="#d0d0d0")
            hint_label.config(bg="#d0d0d0")

        def on_leave(e):
            drop_zone.config(bg="#e8e8e8")
            hint_label.config(bg="#e8e8e8")

        drop_zone.bind("<Enter>", on_enter)
        drop_zone.bind("<Leave>", on_leave)

        # 文件名标签
        file_label = ctk.CTkLabel(
            outer, text="未选择文件",
            font=ctk.CTkFont(size=11),
            text_color="#999999"
        )
        file_label.pack(pady=(0, 10))

        return drop_zone, file_label

    # ── 文件选择处理 ──────────────────────────────────────────────

    def _on_front_drop(self, event):
        self._set_front(event.data.strip('{}'))

    def _on_back_drop(self, event):
        self._set_back(event.data.strip('{}'))

    def _on_front_click(self, event=None):
        path = filedialog.askopenfilename(title="选择正面PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self._set_front(path)

    def _on_back_click(self, event=None):
        path = filedialog.askopenfilename(title="选择反面PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self._set_back(path)

    def _set_front(self, path):
        if path:
            self.front_path.set(path)
            self.front_label.configure(text=os.path.basename(path), text_color="#0066cc")

    def _set_back(self, path):
        if path:
            self.back_path.set(path)
            self.back_label.configure(text=os.path.basename(path), text_color="#0066cc")

    def select_output(self):
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path:
            self.output_dir.set(path)

    def open_output_folder(self):
        path = self.output_dir.get()
        if path and os.path.isdir(path):
            if sys.platform == 'darwin':
                subprocess.run(['open', path])
            elif sys.platform == 'win32':
                os.startfile(path)
            else:
                subprocess.run(['xdg-open', path])
        else:
            messagebox.showwarning("提示", "请先选择一个有效的输出文件夹")

    # ── 主题切换 ──────────────────────────────────────────────────

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="Dark")
            self._update_drop_zone_colors("#e8e8e8", "#666666", "#d0d0d0")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="Light")
            self._update_drop_zone_colors("#2b2b2b", "#888888", "#3a3a3a")

    def _update_drop_zone_colors(self, bg, fg, hover_bg):
        """更新拖放区域颜色以匹配主题"""
        for zone in [self.front_card, self.back_card]:
            zone.config(bg=bg)
            for child in zone.winfo_children():
                child.config(bg=bg, fg=fg)
            zone.bind("<Enter>", lambda e, z=zone, h=hover_bg: self._hover_enter(z, h))
            zone.bind("<Leave>", lambda e, z=zone, b=bg: self._hover_leave(z, b))

    def _hover_enter(self, zone, hover_bg):
        zone.config(bg=hover_bg)
        for child in zone.winfo_children():
            child.config(bg=hover_bg)

    def _hover_leave(self, zone, bg):
        zone.config(bg=bg)
        for child in zone.winfo_children():
            child.config(bg=bg)

    # ── 空白页检测 ────────────────────────────────────────────────

    def is_blank_page(self, page):
        if not self.poppler_available:
            return False
        try:
            from pdf2image import convert_from_bytes
            writer = PdfWriter()
            writer.add_page(page)
            with io.BytesIO() as pdf_bytes:
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)
                images = convert_from_bytes(
                    pdf_bytes.read(), first_page=1, last_page=1,
                    poppler_path=self.poppler_path
                )
                if images:
                    img = images[0].convert('L')
                    pixels = list(img.getdata())
                    avg_gray = sum(pixels) / len(pixels) if pixels else 255
                    var_gray = sum((p - avg_gray) ** 2 for p in pixels) / len(pixels) if pixels else 0
                    return avg_gray >= 250 and var_gray <= 10
        except Exception:
            return False
        return False

    # ── PDF 拼接 ──────────────────────────────────────────────────

    def merge_pdfs(self):
        front_path = self.front_path.get()
        back_path = self.back_path.get()
        output_dir = self.output_dir.get()

        if not all([front_path, back_path, output_dir]):
            messagebox.showwarning('提示', '请先选择所有文件路径和输出文件夹')
            return

        output_path = os.path.join(output_dir, 'output.pdf')

        try:
            front_reader = PdfReader(front_path)
            back_reader = PdfReader(back_path)
            ordered_pages = []

            front_pages_count = len(front_reader.pages)
            back_pages_count = len(back_reader.pages)

            if front_pages_count == back_pages_count > 0:
                for i in range(front_pages_count):
                    ordered_pages.append(front_reader.pages[i])
                    ordered_pages.append(back_reader.pages[back_pages_count - 1 - i])
            else:
                ordered_pages.extend(front_reader.pages)
                ordered_pages.extend(back_reader.pages)

            final_pages = []
            has_blank = False

            if self.skip_blank.get():
                for page in ordered_pages:
                    if not self.is_blank_page(page):
                        final_pages.append(page)
                    else:
                        has_blank = True
            else:
                final_pages = ordered_pages

            writer = PdfWriter()
            for page in final_pages:
                writer.add_page(page)

            with open(output_path, 'wb') as f:
                writer.write(f)

            messagebox.showinfo(
                '成功',
                f'PDF拼接完成！\n'
                f'保存至: {output_path}\n'
                f'跳过空白页: {"是" if self.skip_blank.get() else "否"}\n'
                f'检测到空白页: {"是" if has_blank else "否"}\n'
                f'拼接后总页数: {len(final_pages)}'
            )
        except Exception as e:
            messagebox.showerror('错误', f'拼接失败: {e}')


if __name__ == '__main__':
    app = PDFMerger()
    app.mainloop()
