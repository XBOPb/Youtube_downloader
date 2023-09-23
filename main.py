import os
from interface import Ui_Form
from pytube import YouTube
import requests
from PyQt6.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt6.QtGui import QPixmap, QImage


class Downloader(QWidget):
    def __init__(self):
        super(Downloader, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.temp = os.getenv('TEMP')
        self.temp_file_path = ''
        self.get_default_download_folder()
        self.get_latest_folder()
        self.ui.link_field.textChanged.connect(self.request_preview)
        self.ui.change_folder.clicked.connect(self.choose_folder)
        self.ui.audio_download.clicked.connect(self.get_audio)
        self.ui.video_download.clicked.connect(self.get_video)

    def get_default_download_folder(self):                
        user_folder = os.getenv("USERPROFILE")
        self.default_folder = os.path.join(user_folder, 'Downloads')
        self.set_download_folder(self.default_folder)

    def get_latest_folder(self):
        self.temp_file_path = os.path.join(self.temp, 'ytpath.txt')
        if os.path.isfile(self.temp_file_path):
            with open(self.temp_file_path, 'r') as file:
                download_path = file.read()
                if os.path.isdir(download_path):
                    self.set_download_folder(download_path)
                else:
                    self.set_download_folder(self.default_folder)


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

    def choose_folder(self):
        file_dialog = QFileDialog()
        folder_path = QFileDialog.getExistingDirectory(file_dialog)
        self.set_download_folder(folder_path)

    def set_download_folder(self, folder_path):
        self.ui.download_folder.setText(folder_path) 
        self.folder = folder_path
        if self.temp_file_path:
            with open(self.temp_file_path, 'w') as file:
                file.write(folder_path)
            
    def get_audio(self):
        link = self.ui.link_field.toPlainText()
        video = YouTube(link)
        streams = video.streams.filter(type="audio")
        stream = streams[-1]
        stream.download(self.folder)
    
    def get_video(self):
        link = self.ui.link_field.toPlainText()
        video = YouTube(link)
        stream = video.streams.filter(progressive=True).get_highest_resolution()
        stream.download(self.folder)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Downloader()
    Form.show()
    sys.exit(app.exec())

