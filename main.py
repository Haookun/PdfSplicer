import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from pypdf import PdfReader, PdfWriter
import os

class PDFMerger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PdfSplicer')
        self.setGeometry(300, 300, 500, 400)
        self.front_path = ''
        self.back_path = ''
        self.output_path = ''
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

        from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy

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

    def merge_pdfs(self):
        if not self.front_path or not self.back_path or not self.output_path:
            QMessageBox.warning(self, '提示', '请先选择所有文件路径')
            return
        try:
            front_reader = PdfReader(self.front_path)
            back_reader = PdfReader(self.back_path)
            front_pages = len(front_reader.pages)
            back_pages = len(back_reader.pages)
            total_pages = front_pages + back_pages
            # 假设正面页码为1,3,5,7...，反面为8,6,4,2...，按实际页码顺序拼接
            ordered_pages = []
            # 正面页码索引：0,1,2,3...，实际页码：1,3,5,7...（偶数页数时）
            # 反面页码索引：0,1,2,3...，实际页码：8,6,4,2...（偶数页数时）
            # 先计算总页数
            if front_pages == back_pages and front_pages > 0:
                for i in range(front_pages):
                    # 正面页码
                    ordered_pages.append(front_reader.pages[i])
                    # 反面页码（倒序）
                    ordered_pages.append(back_reader.pages[back_pages - 1 - i])
            else:
                # 页数不一致时，直接顺序拼接
                for i in range(front_pages):
                    ordered_pages.append(front_reader.pages[i])
                for i in range(back_pages):
                    ordered_pages.append(back_reader.pages[i])
            writer = PdfWriter()
            for page in ordered_pages:
                writer.add_page(page)
            with open(self.output_path, 'wb') as f:
                writer.write(f)
            QMessageBox.information(self, '成功', 'PDF拼接完成！')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'拼接失败: {e}')

def main():
    app = QApplication(sys.argv)
    window = PDFMerger()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
