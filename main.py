import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QHBoxLayout, QCheckBox, QSizePolicy
from PyQt6.QtCore import Qt
from pypdf import PdfReader, PdfWriter
import os

class PDFMerger(QWidget):
    def check_poppler(self):
        import shutil, os
        # 优先检测App内置bin目录
        app_bin = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'pdftoppm')
        if os.path.isfile(app_bin) and os.access(app_bin, os.X_OK):
            self.poppler_path = os.path.dirname(app_bin)
            self.poppler_available = True
            return True
        # 其次检测系统环境变量
        poppler_bin = shutil.which('pdftoppm')
        if poppler_bin:
            self.poppler_path = os.path.dirname(poppler_bin)
            self.poppler_available = True
        else:
            self.poppler_path = None
            self.poppler_available = False
        return self.poppler_available
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PdfSplicer')
        self.setGeometry(300, 300, 500, 400)
        self.front_path = ''
        self.back_path = ''
        self.output_path = ''
        self.poppler_available = False
        self.poppler_path = None
        self.check_poppler()
        self.init_ui()

    def keyPressEvent(self, event):
        # 支持 Cmd+W 或 Ctrl+W 关闭窗口
        if (event.modifiers() & Qt.KeyboardModifier.MetaModifier and event.key() == Qt.Key.Key_W) or \
           (event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_W):
            self.close()

    def init_ui(self):
        layout = QVBoxLayout()
        # 操作步骤说明
        steps = (
            '说明：\n'
            '此工具用于拼接PDF正反扫描件\n'
            '操作步骤：\n'
            '1. 点击“选择正面PDF”，选择正面扫描件（如页码1,3,5,7...）。\n'
            '2. 点击“选择反面PDF”，选择反面扫描件（如页码8,6,4,2...）。\n'
            '3. 点击“选择输出文件”，设置合并后PDF的保存位置。\n'
            '4. 点击“开始拼接”，自动按正确顺序生成完整PDF，文件名“output.pdf”'
        )
        self.steps_label = QLabel(steps)
        self.steps_label.setWordWrap(True)
        layout.addWidget(self.steps_label)

        self.label = QLabel('请选择正面和反面PDF文件')
        layout.addWidget(self.label)

        # 跳过空白页开关（居中显示，放在选择按钮上方）
        hbox_blank = QHBoxLayout()
        hbox_blank.addStretch(1)
        self.skip_blank_checkbox = QCheckBox('跳过空白页')
        self.skip_blank_checkbox.setChecked(False)
        hbox_blank.addWidget(self.skip_blank_checkbox)
        hbox_blank.addStretch(1)
        layout.addLayout(hbox_blank)

        # 如果poppler不可用，禁用空白页识别并弹窗提示
        if not self.poppler_available:
            self.skip_blank_checkbox.setEnabled(False)
            QMessageBox.warning(self, '依赖缺失', '未检测到poppler（pdftoppm），空白页识别功能不可用。请参考README安装poppler。')

        # 第一行：正面和反面选择
        hbox1 = QHBoxLayout()
        self.btn_front = QPushButton('选择正面PDF')
        self.btn_front.setFixedWidth(180)
        self.btn_front.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_front.clicked.connect(self.select_front)
        hbox1.addStretch(1)
        hbox1.addWidget(self.btn_front)
        hbox1.addSpacing(10)
        self.btn_back = QPushButton('选择反面PDF')
        self.btn_back.setFixedWidth(180)
        self.btn_back.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_back.clicked.connect(self.select_back)
        hbox1.addWidget(self.btn_back)
        hbox1.addStretch(1)
        layout.addLayout(hbox1)

        # 第二行：选择输出文件夹和打开输出路径
        hbox2 = QHBoxLayout()
        self.btn_output = QPushButton('选择输出文件夹')
        self.btn_output.setFixedWidth(180)
        self.btn_output.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_output.clicked.connect(self.select_output)
        hbox2.addStretch(1)
        hbox2.addWidget(self.btn_output)
        hbox2.addSpacing(10)
        self.btn_open_output = QPushButton('打开输出文件夹')
        self.btn_open_output.setFixedWidth(180)
        self.btn_open_output.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_open_output.clicked.connect(self.open_output_folder)
        hbox2.addWidget(self.btn_open_output)
        hbox2.addStretch(1)
        layout.addLayout(hbox2)

        # 第三行：开始拼接
        hbox3 = QHBoxLayout()
        self.btn_merge = QPushButton('开始拼接')
        self.btn_merge.setFixedWidth(380)
        self.btn_merge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_merge.clicked.connect(self.merge_pdfs)
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn_merge)
        hbox3.addStretch(1)
        layout.addLayout(hbox3)

        self.setLayout(layout)

    def open_output_folder(self):
        if self.output_path:
            folder = os.path.dirname(self.output_path)
            import subprocess
            if sys.platform == 'darwin':
                subprocess.run(['open', folder])
            elif sys.platform == 'win32':
                subprocess.run(['explorer', folder])
            else:
                subprocess.run(['xdg-open', folder])

    def select_front(self):
        path, _ = QFileDialog.getOpenFileName(self, '选择正面PDF', '', 'PDF Files (*.pdf)')
        if path:
            self.front_path = path
            self.label.setText(f'正面PDF: {os.path.basename(path)}')

    def select_back(self):
        path, _ = QFileDialog.getOpenFileName(self, '选择反面PDF', '', 'PDF Files (*.pdf)')
        if path:
            self.back_path = path
            self.label.setText(f'反面PDF: {os.path.basename(path)}')

    def select_output(self):
        path = QFileDialog.getExistingDirectory(self, '选择输出文件夹', '')
        if path:
            # 默认输出文件名
            self.output_path = os.path.join(path, 'output.pdf')
            self.label.setText(f'输出文件: {os.path.basename(self.output_path)}')

    def is_blank_page(self, page):
        if not self.poppler_available:
            return False
        """
        扫描件空白页识别：内容流+灰度均值+灰度方差。
        1. 内容流检测（文本/图片）。
        2. 灰度均值高且方差低，视为空白页（适应底纹/灰尘）。
        """
        # # 内容流检测
        # text = ''
        # try:
        #     text = page.extract_text()
        # except Exception:
        #     pass
        # if text and text.strip():
        #     return False
        # if '/XObject' in page.get('/Resources', {}):
        #     xobj = page['/Resources']['/XObject']
        #     if len(xobj) > 0:
        #         return False
        # 灰度均值+方差检测
        try:
            from pdf2image import convert_from_bytes
            from PIL import Image
            import io
            writer = PdfWriter()
            writer.add_page(page)
            pdf_bytes = io.BytesIO()
            writer.write(pdf_bytes)
            pdf_bytes.seek(0)
            images = convert_from_bytes(pdf_bytes.read(), first_page=1, last_page=1, poppler_path=self.poppler_path)
            if images:
                img = images[0].convert('L')  # 灰度
                pixels = list(img.getdata())
                avg_gray = sum(pixels) / len(pixels) if len(pixels) > 0 else 255
                var_gray = sum((p - avg_gray) ** 2 for p in pixels) / len(pixels) if len(pixels) > 0 else 0
            # 判定逻辑：均值高于250且方差低于10，视为空白页（根据实际参数调整）
            return avg_gray >= 250 and var_gray <= 10
        except Exception:
            pass
        return False
    def merge_pdfs(self):
        if not self.front_path or not self.back_path or not self.output_path:
            QMessageBox.warning(self, '提示', '请先选择所有文件路径')
            return
        try:
            front_reader = PdfReader(self.front_path)
            back_reader = PdfReader(self.back_path)
            front_pages = len(front_reader.pages)
            back_pages = len(back_reader.pages)
            ordered_pages = []
            has_blank = False
            skip_blank = self.skip_blank_checkbox.isChecked()
            # 拼接逻辑
            if front_pages == back_pages and front_pages > 0:
                for i in range(front_pages):
                    page_f = front_reader.pages[i]
                    blank_f = self.is_blank_page(page_f)
                    if blank_f:
                        has_blank = True
                    if not (skip_blank and blank_f):
                        ordered_pages.append(page_f)
                    page_b = back_reader.pages[back_pages - 1 - i]
                    blank_b = self.is_blank_page(page_b)
                    if blank_b:
                        has_blank = True
                    if not (skip_blank and blank_b):
                        ordered_pages.append(page_b)
            else:
                for i in range(front_pages):
                    page_f = front_reader.pages[i]
                    blank_f = self.is_blank_page(page_f)
                    if blank_f:
                        has_blank = True
                    if not (skip_blank and blank_f):
                        ordered_pages.append(page_f)
                for i in range(back_pages):
                    page_b = back_reader.pages[i]
                    blank_b = self.is_blank_page(page_b)
                    if blank_b:
                        has_blank = True
                    if not (skip_blank and blank_b):
                        ordered_pages.append(page_b)
            writer = PdfWriter()
            for page in ordered_pages:
                writer.add_page(page)
            with open(self.output_path, 'wb') as f:
                writer.write(f)
            QMessageBox.information(self, '成功', f'PDF拼接完成！\n跳过空白页: {skip_blank}\n检测到空白页: {has_blank}\n拼接后总页数: {len(ordered_pages)}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'拼接失败: {e}')

def main():
    app = QApplication(sys.argv)
    window = PDFMerger()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
