from interface import Ui_Form
from pytube import YouTube
import requests
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPixmap, QImage


class Downloader(QWidget):
    def __init__(self):
        super(Downloader, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.link_field.textChanged.connect(self.request_preview)

    def request_preview(self):
        text = self.ui.link_field.toPlainText()
        if not ('?v=') in text:
            self.ui.preview_label.clear()
            return
        link = text.split('?v=')[1]
        preview_request = f'http://img.youtube.com/vi/{link}/hqdefault.jpg'
        image = QImage()
        image.loadFromData(requests.get(preview_request).content)
        pixmap = QPixmap(image)
        self.ui.preview_label.setPixmap(pixmap)

    def sample(self):
        yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
        yd = yt.streams.filter(only_audio=True)
        print(yd)
        yd.download(r'C:\Users\XBOPb\Desktop\New folder')

    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Downloader()
    Form.show()
    sys.exit(app.exec())
