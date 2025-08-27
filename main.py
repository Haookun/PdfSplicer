import sys
import os
import subprocess
import io
from tkinter import Tk, Frame, Label, Checkbutton, Entry, StringVar, BooleanVar, filedialog, messagebox
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter

class PDFMerger(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title('PdfSplicer')
        self.geometry('500x580+300+300') # 调整窗口高度

        self.front_path = StringVar()
        self.back_path = StringVar()
        self.output_dir = StringVar()
        self.skip_blank = BooleanVar(value=False)

        self.poppler_path = None
        self.poppler_available = self.check_poppler()

        self.init_ui()

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

    def init_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --- 说明 ---
        steps_text = (
            '说明：\n此工具用于拼接PDF正反扫描件\n\n'
            '操作步骤：\n'
            '1. 点击“选择正面PDF”，选择正面扫描件（如页码1,3,5,7...）。\n'
            '2. 点击“选择反面PDF”，选择反面扫描件（如页码8,6,4,2...）。\n'
            '3. 点击“选择输出文件夹”，设置合并后PDF的保存位置。\n'
            '4. 点击“开始拼接”，自动按正确顺序生成完整PDF，文件名“output.pdf”'
        )
        steps_label = ttk.Label(main_frame, text=steps_text, wraplength=480)
        steps_label.pack(pady=5, anchor="w")

        info_label = ttk.Label(main_frame, text="请选择正面和反面PDF文件")
        info_label.pack(pady=(5, 10))


        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill="x", expand=True, pady=10)
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.columnconfigure(1, weight=1)

        # --- 正面区域 ---
        front_frame = ttk.LabelFrame(selection_frame, text="正面 PDF")
        front_frame.grid(row=0, column=0, padx=5, sticky="nsew")
        btn_front = ttk.Button(front_frame, text="选择正面PDF文件", command=self.open_front_file_dialog)
        btn_front.pack(fill="x", padx=10, pady=5)
        
        drop_front = self.create_drop_target(front_frame, "或将正面PDF拖拽至此", self.select_front)
        drop_front.pack(fill="both", expand=True, padx=10, pady=10, ipady=25)
        
        self.label_front = ttk.Label(front_frame, text="未选择文件", anchor="center", wraplength=200)
        self.label_front.pack(fill="x", pady=5)

        # --- 反面区域 ---
        back_frame = ttk.LabelFrame(selection_frame, text="反面 PDF")
        back_frame.grid(row=0, column=1, padx=5, sticky="nsew")
        btn_back = ttk.Button(back_frame, text="选择反面PDF文件", command=self.open_back_file_dialog)
        btn_back.pack(fill="x", padx=10, pady=5)

        drop_back = self.create_drop_target(back_frame, "或将反面PDF拖拽至此", self.select_back)
        drop_back.pack(fill="both", expand=True, padx=10, pady=10, ipady=25)

        self.label_back = ttk.Label(back_frame, text="未选择文件", anchor="center", wraplength=200)
        self.label_back.pack(fill="x", pady=5)
        
        # --- 选项 ---
        check_frame = ttk.Frame(main_frame)
        check_frame.pack(fill="x", pady=5)
        skip_check = ttk.Checkbutton(check_frame, text="跳过空白页", variable=self.skip_blank)
        skip_check.pack()
        if not self.poppler_available:
            skip_check.config(state="disabled")
            messagebox.showwarning("依赖缺失", "未检测到poppler (pdftoppm)，空白页识别功能不可用。")

        # --- 输出 ---
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill="x", pady=10)
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, state="readonly")
        output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        btn_output = ttk.Button(output_frame, text="选择输出文件夹", command=self.select_output)
        btn_output.pack(side="right")

        # --- 操作 ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=10)
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        btn_open = ttk.Button(action_frame, text="打开输出文件夹", command=self.open_output_folder)
        btn_open.grid(row=0, column=0, padx=5, sticky="ew")
        btn_merge = ttk.Button(action_frame, text="开始拼接", command=self.merge_pdfs)
        btn_merge.grid(row=0, column=1, padx=5, sticky="ew")
    
    def create_drop_target(self, parent, text, drop_cmd):
        frame = Frame(parent, relief="groove", borderwidth=2, bg="#f0f0f0")
        frame.pack_propagate(False) # 防止label挤压frame
        label = Label(frame, text=text, bg="#f0f0f0", fg="gray")
        label.pack(expand=True)
        
        frame.drop_target_register(DND_FILES)
        frame.dnd_bind('<<Drop>>', drop_cmd)
        
        # 添加悬停效果
        def on_enter(e): label.config(bg="#e0e0e0")
        def on_leave(e): label.config(bg="#f0f0f0")
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        return frame

    def open_front_file_dialog(self):
        path = filedialog.askopenfilename(title="选择正面PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.select_front(path)

    def open_back_file_dialog(self):
        path = filedialog.askopenfilename(title="选择反面PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.select_back(path)

    def select_front(self, event_or_path):
        path = event_or_path.data.strip('{}') if hasattr(event_or_path, 'data') else event_or_path
        if path:
            self.front_path.set(path)
            self.label_front.config(text=f".../{os.path.basename(path)}")

    def select_back(self, event_or_path):
        path = event_or_path.data.strip('{}') if hasattr(event_or_path, 'data') else event_or_path
        if path:
            self.back_path.set(path)
            self.label_back.config(text=f".../{os.path.basename(path)}")

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

    def is_blank_page(self, page):
        if not self.poppler_available: return False
        try:
            from pdf2image import convert_from_bytes
            writer = PdfWriter()
            writer.add_page(page)
            with io.BytesIO() as pdf_bytes:
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)
                images = convert_from_bytes(pdf_bytes.read(), first_page=1, last_page=1, poppler_path=self.poppler_path)
                if images:
                    img = images[0].convert('L')
                    pixels = list(img.getdata())
                    avg_gray = sum(pixels) / len(pixels) if pixels else 255
                    var_gray = sum((p - avg_gray) ** 2 for p in pixels) / len(pixels) if pixels else 0
                    return avg_gray >= 250 and var_gray <= 10
        except Exception:
            return False
        return False

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
            if self.skip_blank.get():
                has_blank = False
                for page in ordered_pages:
                    if not self.is_blank_page(page):
                        final_pages.append(page)
                    else:
                        has_blank = True
            else:
                final_pages = ordered_pages
                # Inefficient to check for blanks if not skipping, but keep logic simple
                has_blank = any(self.is_blank_page(p) for p in ordered_pages if self.poppler_available)

            writer = PdfWriter()
            for page in final_pages:
                writer.add_page(page)

            with open(output_path, 'wb') as f:
                writer.write(f)
            
            messagebox.showinfo('成功', f'PDF拼接完成！\n保存至: {output_path}\n跳过空白页: {"是" if self.skip_blank.get() else "否"}\n检测到空白页: {"是" if has_blank else "否"}\n拼接后总页数: {len(final_pages)}')
        except Exception as e:
            messagebox.showerror('错误', f'拼接失败: {e}')


    def open_front_file_dialog(self):
        path = filedialog.askopenfilename(title="选择正面PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.select_front(path)

    def open_back_file_dialog(self):
        path = filedialog.askopenfilename(title="选择反面PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.select_back(path)

    def select_front(self, event_or_path):
        path = event_or_path.data.strip('{}') if hasattr(event_or_path, 'data') else event_or_path
        if path:
            self.front_path.set(path)
            self.label_front.config(text=f".../{os.path.basename(path)}")

    def select_back(self, event_or_path):
        path = event_or_path.data.strip('{}') if hasattr(event_or_path, 'data') else event_or_path
        if path:
            self.back_path.set(path)
            self.label_back.config(text=f".../{os.path.basename(path)}")

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

    def is_blank_page(self, page):
        if not self.poppler_available: return False
        try:
            from pdf2image import convert_from_bytes
            writer = PdfWriter()
            writer.add_page(page)
            with io.BytesIO() as pdf_bytes:
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)
                images = convert_from_bytes(pdf_bytes.read(), first_page=1, last_page=1, poppler_path=self.poppler_path)
                if images:
                    img = images[0].convert('L')
                    pixels = list(img.getdata())
                    avg_gray = sum(pixels) / len(pixels) if pixels else 255
                    var_gray = sum((p - avg_gray) ** 2 for p in pixels) / len(pixels) if pixels else 0
                    return avg_gray >= 250 and var_gray <= 10
        except Exception:
            return False
        return False

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
            if self.skip_blank.get():
                has_blank = False
                for page in ordered_pages:
                    if not self.is_blank_page(page):
                        final_pages.append(page)
                    else:
                        has_blank = True
            else:
                final_pages = ordered_pages
                # Inefficient to check for blanks if not skipping, but keep logic simple
                has_blank = any(self.is_blank_page(p) for p in ordered_pages if self.poppler_available)

            writer = PdfWriter()
            for page in final_pages:
                writer.add_page(page)

            with open(output_path, 'wb') as f:
                writer.write(f)
            
            messagebox.showinfo('成功', f'PDF拼接完成！\n保存至: {output_path}\n跳过空白页: {"是" if self.skip_blank.get() else "否"}\n检测到空白页: {"是" if has_blank else "否"}\n拼接后总页数: {len(final_pages)}')
        except Exception as e:
            messagebox.showerror('错误', f'拼接失败: {e}')

if __name__ == '__main__':
    app = PDFMerger()
    app.mainloop()
