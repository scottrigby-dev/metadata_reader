import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QTextBrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class ImageMetadataViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Metadata Viewer')
        self.setGeometry(100, 100, 600, 400)

        # Widgets
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_path = None

        self.select_button = QPushButton('Select Image', self)
        self.select_button.clicked.connect(self.show_file_dialog)

        self.metadata_browser = QTextBrowser(self)

        # Layout
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.image_label)
        v_layout.addWidget(self.select_button)
        v_layout.addWidget(self.metadata_browser)

        self.setLayout(v_layout)

    def show_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.image_path = selected_files[0]
                self.show_image()
                self.show_metadata()

    def show_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))

    def show_metadata(self):
        if self.image_path:
            metadata_text = self.get_metadata_text()
            self.metadata_browser.setPlainText(metadata_text)

    def get_metadata_text(self):
        metadata_text = "Metadata:\n"
        try:
            image = Image.open(self.image_path)

            # Extract image info
            info = image.info
            for key, value in info.items():
                metadata_text += f"{key}: {value}\n"

            return metadata_text

        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageMetadataViewer()
    window.show()
    sys.exit(app.exec_())
