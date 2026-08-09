
import os
import sys

# Must be BEFORE importing PySide6
os.environ["QT_OPENGL"] = "software"

os.environ["QT_MEDIA_BACKEND"] = "windows"

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineCore import QWebEngineSettings

# Force software OpenGL
QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)

from ui.main_window import MainWindow

app = QApplication(sys.argv)

#with open("/ui/styles/styles.qss", "r") as f:
  #  app.setStyleSheet(f.read())

window = MainWindow()
window.show()

sys.exit(app.exec())