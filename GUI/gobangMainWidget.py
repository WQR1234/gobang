from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton

from GUI.ui_gobangMainWidget import Ui_gobangMainWidget


class GobangMainWidget(QWidget, Ui_gobangMainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setFixedSize(600, 400)
        self.clearBtn.clicked.connect(self._clear)

    # slot
    def _clear(self):
        self.boardWidget.m_pixmap = QPixmap()
        self.boardWidget.m_circle_center = QPoint(0, 0)
        self.boardWidget.m_circle_radius = 0
        self.boardWidget.update()






